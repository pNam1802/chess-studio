# %% [markdown]
# # Chess Live: train the board and piece models
#
# Trains the two YOLO11 models of the studio's Camera mode on ChessReD2K (2,078 phone photos of a real board,
# taken from the side, with the board's corners and every piece's box; CC BY-NC-SA 4.0, Masouris & van Gemert 2023):
#
# - `board`: YOLO11n-pose, one class, 4 keypoints = the board's outer corners a1, h1, h8, a8
# - `pieces`: YOLO11s, 12 classes, trained on the board's crop the way the server cuts it
#
# Kaggle settings: **Accelerator GPU T4 x2** (the two models train side by side; P100 works too, one after the
# other) and **Internet on**. Run all: about 5 minutes of download, then 1 to 1.5 hours of training. At the end,
# download `chess-live-weights.zip` from the Output panel and unzip it into `live/weights/`.
#
# This notebook is made from `live/train_kaggle.py` by `live/make_notebook.py`; the first cell writes
# `chessvision.py`, the same code the server runs.

# %%
import collections
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'ultralytics>=8.3,<9'], check=True)

import cv2
import numpy as np
import torch

import chessvision as cvn

WORK = Path('/kaggle/working') if Path('/kaggle/working').exists() else Path('work')
RAW, DS = Path('/tmp/chessred'), Path('/tmp/ds')
GPUS = torch.cuda.device_count()
print('GPUs:', [torch.cuda.get_device_name(i) for i in range(GPUS)])

# %% [markdown]
# ## 1. Download ChessReD2K (4.7 GB) and its annotations

# %%
BASE = 'https://data.4tu.nl/file/99b5c721-280b-450b-b058-b2900b69a90f/'
FILES = {   # name: (url, md5)
    'annotations.json': (BASE + '3cae6364-daca-4967-b426-1e4b68cdb64c', 'd34bca5ad46ec7a8df96a1d3c36784f3'),
    'chessred2k.zip': (BASE + '410e41c7-dde5-413f-8722-3e112363a1a2', '4e55e299b6b2973e0d8659bd241c7975'),
}


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 24), b''):
            h.update(block)
    return h.hexdigest()


RAW.mkdir(parents=True, exist_ok=True)
for name, (url, sum_) in FILES.items():
    path = RAW / name
    if path.exists() and md5(path) == sum_:
        continue
    subprocess.run(['wget', '-c', '--tries=20', '--progress=dot:giga', '-O', str(path), url], check=True)
    assert md5(path) == sum_, name + ': download damaged, run this cell again'
print('downloaded')

# %% [markdown]
# ## 2. Build the two datasets
#
# `board`: whole photos (long side 1024), one box around the board with its 4 corners as keypoints.
# `pieces`: the board's crop (`cvn.board_crop` of the true corners), with the piece boxes inside it.
# The test photos are also kept whole at 1280 px with their true boards, for the end-to-end check in step 5.

# %%
A = json.loads((RAW / 'annotations.json').read_text())
SPLITS = A['splits']['chessred2k']
images = {im['id']: im for im in A['images']}
corners = {c['image_id']: c['corners'] for c in A['annotations']['corners']}
pieces = collections.defaultdict(list)
for p in A['annotations']['pieces']:
    if 'bbox' in p:
        pieces[p['image_id']].append(p)
split_of = {i: s for s in ('train', 'val', 'test') for i in SPLITS[s]['image_ids']}
by_name = {images[i]['file_name']: i for i in split_of}
ORDER = ['bottom_left', 'bottom_right', 'top_right', 'top_left']   # a1, h1, h8, a8 seen from White
NAMES = [c['name'] for c in sorted(A['categories'], key=lambda c: c['id'])][:12]
assert ''.join(n.split('-')[0][0] for n in NAMES) == 'wwwwwwbbbbbb' and cvn.LETTERS == 'PRNBQKprnbqk'


def sq_index(name):   # 'a8' -> 0 ... 'h1' -> 63, FEN order
    return (8 - int(name[1])) * 8 + 'abcdefgh'.index(name[0])


def save(path, img, side):
    k = side / max(img.shape[:2])
    if k < 1:
        img = cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(path), img, [cv2.IMWRITE_JPEG_QUALITY, 92])


shutil.rmtree(DS, ignore_errors=True)
for kind in ('board', 'pieces'):
    for s in ('train', 'val', 'test'):
        (DS / kind / 'images' / s).mkdir(parents=True)
        (DS / kind / 'labels' / s).mkdir(parents=True)
(DS / 'frames').mkdir()
truth = {}   # test photo id -> its true 64-character board

with zipfile.ZipFile(RAW / 'chessred2k.zip') as z:
    members = [n for n in z.namelist() if os.path.basename(n) in by_name]
    print(len(members), 'photos of', len(split_of))
    for k, member in enumerate(members):
        i = by_name[os.path.basename(member)]
        s = split_of[i]
        img = cv2.imdecode(np.frombuffer(z.read(member), np.uint8), cv2.IMREAD_COLOR)
        h, w = img.shape[:2]
        sc = w / images[i]['width']   # the zip's photos may be smaller than the annotated ones
        cr = np.float32([corners[i][o] for o in ORDER]) * sc
        boxes = np.float32([[x, y, x + bw, y + bh] for x, y, bw, bh in (p['bbox'] for p in pieces[i])]) * sc

        # board: a box around the corners (2% margin) and the corners, those outside the photo marked unseen
        (x0, y0), (x1, y1) = cr.min(0), cr.max(0)
        m = 0.02 * max(x1 - x0, y1 - y0)
        x0, y0, x1, y1 = max(0, x0 - m), max(0, y0 - m), min(w, x1 + m), min(h, y1 + m)
        kp = ' '.join(f'{x / w:.5f} {y / h:.5f} 2' if 0 <= x < w and 0 <= y < h else '0 0 0' for x, y in cr)
        (DS / 'board/labels' / s / f'{i}.txt').write_text(
            f'0 {(x0 + x1) / 2 / w:.5f} {(y0 + y1) / 2 / h:.5f} {(x1 - x0) / w:.5f} {(y1 - y0) / h:.5f} {kp}\n')
        save(DS / 'board/images' / s / f'{i}.jpg', img, 1024)

        # pieces: the crop, and each box at least half inside it
        X0, Y0, X1, Y1 = cvn.board_crop(cr, w, h)
        cw, ch = X1 - X0, Y1 - Y0
        lines = []
        for (bx0, by0, bx1, by1), p in zip(boxes, pieces[i]):
            cx0, cy0, cx1, cy1 = max(bx0, X0), max(by0, Y0), min(bx1, X1), min(by1, Y1)
            if cx1 <= cx0 or cy1 <= cy0 or (cx1 - cx0) * (cy1 - cy0) < 0.5 * (bx1 - bx0) * (by1 - by0):
                continue
            lines.append(f"{p['category_id']} {((cx0 + cx1) / 2 - X0) / cw:.5f} {((cy0 + cy1) / 2 - Y0) / ch:.5f} "
                         f'{(cx1 - cx0) / cw:.5f} {(cy1 - cy0) / ch:.5f}')
        (DS / 'pieces/labels' / s / f'{i}.txt').write_text('\n'.join(lines) + '\n' if lines else '')
        save(DS / 'pieces/images' / s / f'{i}.jpg', img[Y0:Y1, X0:X1], 1024)

        if s == 'test':
            save(DS / 'frames' / f'{i}.jpg', img, 1280)
            b = ['.'] * 64
            for p in pieces[i]:
                b[sq_index(p['chessboard_position'])] = cvn.LETTERS[p['category_id']]
            truth[i] = ''.join(b)
        if k % 200 == 0:
            print(k, '/', len(members))

(DS / 'board/data.yaml').write_text(
    f'path: {DS / "board"}\ntrain: images/train\nval: images/val\ntest: images/test\n'
    'kpt_shape: [4, 3]\nflip_idx: [1, 0, 3, 2]\nnames:\n  0: board\n')
(DS / 'pieces/data.yaml').write_text(
    f'path: {DS / "pieces"}\ntrain: images/train\nval: images/val\ntest: images/test\nnames:\n'
    + ''.join(f'  {k}: {n}\n' for k, n in enumerate(NAMES)))
print('datasets ready:', {s: len(SPLITS[s]['image_ids']) for s in ('train', 'val', 'test')})

# %% [markdown]
# ## 3. Calibrate the foot
#
# With the true corners and boxes, which `FOOT` puts every piece on its own square? The middle of the best range
# leaves the most room for the detector's boxes being a little off.

# %%
cal = [i for i in split_of if split_of[i] != 'test']
scores = {}
for foot in np.round(np.arange(0, 0.61, 0.05), 2):
    ok = n = 0
    for i in cal:
        cr = np.float32([corners[i][o] for o in ORDER])
        boxes = np.float32([[x, y, x + bw, y + bh] for x, y, bw, bh in (p['bbox'] for p in pieces[i])])
        got = cvn.squares(cr, boxes, foot)
        ok += int((got == np.array([sq_index(p['chessboard_position']) for p in pieces[i]])).sum())
        n += len(pieces[i])
    scores[float(foot)] = ok / n
top = max(scores.values())
best = [f for f, v in scores.items() if v >= top - 1e-4]
FOOT = round(float(np.median(best)), 2)
print({f: f'{v:.2%}' for f, v in scores.items()})
print('FOOT =', FOOT)

# %% [markdown]
# ## 4. Train
#
# Both at 640 px, the size the server runs. No left-right flips for the board: a mirrored board has its corners'
# names wrong (h1 is always a light square on White's right).

# %%
RUNS = WORK / 'runs'
JOBS = {
    'board': f'yolo pose train model=yolo11n-pose.pt data={DS}/board/data.yaml imgsz=640 epochs=100 batch=32 '
             f'fliplr=0 degrees=8 patience=30 cache=ram workers=2 plots=False project={RUNS} name=board exist_ok=True',
    'pieces': f'yolo detect train model=yolo11s.pt data={DS}/pieces/data.yaml imgsz=640 epochs=120 batch=16 '
              f'degrees=5 patience=30 cache=ram workers=2 plots=False project={RUNS} name=pieces exist_ok=True',
}


def tail(path):
    try:
        return path.read_text(errors='ignore').replace('\r', '\n').strip().splitlines()[-1][:160]
    except (OSError, IndexError):
        return ''


def train(names):
    """Train these side by side, one GPU each; print each one's progress every two minutes."""
    procs = {}
    for gpu, name in enumerate(names):
        log = WORK / f'{name}.log'
        procs[name] = (subprocess.Popen(f'{JOBS[name]} device={gpu}', shell=True, stdout=open(log, 'w'),
                                        stderr=subprocess.STDOUT), log)
    while any(p.poll() is None for p, _ in procs.values()):
        time.sleep(120)
        for name, (p, log) in procs.items():
            print(f'[{name}]', 'done' if p.poll() is not None else tail(log))
    for name, (p, log) in procs.items():
        assert p.returncode == 0, f'{name} failed, see {log}:\n' + tail(log)


WORK.mkdir(exist_ok=True)
for group in ([['board', 'pieces']] if GPUS >= 2 else [['pieces'], ['board']]):
    train(group)
print('trained')

# %% [markdown]
# ## 5. Check the whole pipeline on the test games
#
# Each whole test photo goes through what the server does (corners, crop, pieces, squares) and its board is
# compared with the true one.

# %%
pipe = cvn.Pipeline(str(RUNS / 'board/weights/best.pt'), str(RUNS / 'pieces/weights/best.pt'), {'foot': FOOT})
found = right = squares_right = 0
for i, want in truth.items():
    out = pipe(cv2.imread(str(DS / 'frames' / f'{i}.jpg')))
    if not out['board']:
        continue
    found += 1
    got = out['board']
    if got != want:   # the corners may be named from another side, as the page fixes by turning the board
        turns = [got]
        for _ in range(3):
            turns.append(cvn.turn(turns[-1]))
        got = max(turns, key=lambda t: sum(a == b for a, b in zip(t, want)))
    n = sum(a == b for a, b in zip(got, want))
    squares_right += n
    right += n == 64
total = len(truth)
TEST = {'photos': total, 'board_found': found / total, 'square_accuracy': squares_right / max(1, found * 64),
        'boards_perfect': right / total}
print({k: f'{v:.1%}' if isinstance(v, float) else v for k, v in TEST.items()})

# %% [markdown]
# ## 6. Package the weights
#
# Download `chess-live-weights.zip` (Output panel, right) and unzip it into `live/weights/`, then
# `modal deploy live/modal_app.py`.

# %%
out = WORK / 'weights'
out.mkdir(exist_ok=True)
shutil.copy(RUNS / 'board/weights/best.pt', out / 'board.pt')
shutil.copy(RUNS / 'pieces/weights/best.pt', out / 'pieces.pt')
(out / 'meta.json').write_text(json.dumps({'foot': FOOT, 'pad': cvn.PAD, 'test': TEST}, indent=1))
shutil.make_archive(str(WORK / 'chess-live-weights'), 'zip', out)
print(sorted(p.name for p in out.iterdir()), '->', WORK / 'chess-live-weights.zip')
