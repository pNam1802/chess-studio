"""A chess board and its pieces from one camera frame: the vision half of the studio's Camera mode.

Shared by the Modal server (modal_app.py) and the Kaggle notebook (train_kaggle.py, which calibrates FOOT and
checks the whole pipeline on the test games), so training and serving see the board the same way.

Two YOLO models: `board` (pose, one class, 4 keypoints) finds the board's outer corners in the whole frame; the
corners give the homography from the image to the board, and `pieces` (detect, 12 classes) looks only at the
board's crop. A piece belongs to the square under its foot.

Board coordinates: a1's outer corner is (0, 0), h1's (8, 0), h8's (8, 8), a8's (0, 8); file f (0 = a) and rank r
(0 = rank 1) span [f, f+1] x [r, r+1]. Corners always come in that order: a1, h1, h8, a8 (ChessReD's bottom_left,
bottom_right, top_right, top_left, seen from White). A board is 64 characters in FEN order (a8..h8 down to a1..h1),
'PNBRQK' White, 'pnbrqk' Black, '.' empty.
"""
import cv2
import numpy as np

BOARD_PTS = np.float32([[0, 0], [8, 0], [8, 8], [0, 8]])
# ChessReD's category ids 0..11, as FEN letters
LETTERS = 'PRNBQKprnbqk'
# the piece detector sees the corners' bounding box widened by these fractions of its size (more on top, where
# the far pieces stand up past the board's edge)
PAD = {'side': 0.06, 'top': 0.22, 'bottom': 0.05}
# a piece stands on the square under its foot: the middle of its box's bottom edge, raised by FOOT box widths (the
# camera looks down at an angle, so the base sits above the box's bottom). the notebook calibrates it
FOOT = 0.25
# corners further than this (mean, in frame sizes) from the steadied ones mean the camera or the board moved
JUMP = 0.06
# side of the top-down board image that motion is measured on
WARP = 96


def board_crop(corners, w, h, pad=PAD):
    """The part of a w x h frame the piece detector looks at: x0, y0, x1, y1 (ints, inside the frame)."""
    (x0, y0), (x1, y1) = corners.min(0), corners.max(0)
    bw, bh = x1 - x0, y1 - y0
    return (max(0, int(x0 - pad['side'] * bw)), max(0, int(y0 - pad['top'] * bh)),
            min(w, int(np.ceil(x1 + pad['side'] * bw))), min(h, int(np.ceil(y1 + pad['bottom'] * bh))))


def to_board(corners, pts):
    """Image points (n, 2) -> board coordinates (n, 2)."""
    H = cv2.getPerspectiveTransform(np.float32(corners), BOARD_PTS)
    return cv2.perspectiveTransform(np.float32(pts).reshape(-1, 1, 2), H).reshape(-1, 2)


def feet(boxes, foot=FOOT):
    """Where pieces with these boxes (n, 4: x0 y0 x1 y1) stand, in the image."""
    b = np.asarray(boxes, np.float32).reshape(-1, 4)
    return np.stack([(b[:, 0] + b[:, 2]) / 2, b[:, 3] - foot * (b[:, 2] - b[:, 0])], 1)


def squares(corners, boxes, foot=FOOT):
    """The square index (FEN order, 0 = a8) each box stands on, -1 off the board."""
    if not len(boxes):
        return np.zeros(0, int)
    uv = np.floor(to_board(corners, feet(boxes, foot))).astype(int)
    f, r = uv[:, 0], uv[:, 1]
    return np.where((f >= 0) & (f < 8) & (r >= 0) & (r < 8), (7 - r) * 8 + f, -1)


def place(corners, boxes, cls, conf, foot=FOOT):
    """The board the pieces make: the surest piece on each square. -> (64-char board, confidences (64,))"""
    board, best = ['.'] * 64, np.zeros(64, np.float32)
    for i, c, p in zip(squares(corners, boxes, foot), cls, conf):
        if i >= 0 and p > best[i]:
            board[i], best[i] = LETTERS[int(c)], p
    return ''.join(board), best


def turn(board):
    """The board with its corners named one step on (a1 <- h1's corner, ...): square (f, r) moves to (r, 7 - f)."""
    out = [''] * 64
    for i, ch in enumerate(board):
        f, r = i % 8, 7 - (i >> 3)
        out[f * 8 + r] = ch
    return ''.join(out)


def plausible(corners, w, h):
    """Four corners of a real board: a convex quadrilateral covering at least 2% of the frame."""
    q = np.float32(corners).reshape(4, 1, 2)
    return cv2.isContourConvex(q.astype(np.int32)) and cv2.contourArea(q) > 0.02 * w * h


def align(prev, new):
    """new turned so its corners lie nearest prev's (the model may name the corners from another side)."""
    return min((np.roll(new, -s, axis=0) for s in range(4)), key=lambda c: np.linalg.norm(c - prev, axis=1).sum())


class Track:
    """One camera's corners, steadied over frames and kept for a few frames the model misses, and how much the
    board changed since the last frame."""

    def __init__(self, keep=15):
        self.corners, self.miss, self.keep, self.prev = None, 0, keep, None

    def update(self, found, w, h):
        if found is None:
            self.miss += 1
            if self.miss > self.keep:
                self.corners = self.prev = None
            return self.corners
        self.miss = 0
        if self.corners is not None:
            found = align(self.corners, found)
            if np.linalg.norm(found - self.corners, axis=1).mean() < JUMP * max(w, h):
                found = 0.5 * self.corners + 0.5 * found
            else:
                self.prev = None   # a different view: nothing to compare the next frame with
        self.corners = found
        return found

    def motion(self, gray, corners):
        """Mean change per pixel (0..1) of the top-down board since the last frame; None for the first one."""
        H = cv2.getPerspectiveTransform(np.float32(corners), BOARD_PTS * (WARP / 8))
        top = cv2.GaussianBlur(cv2.warpPerspective(gray, H, (WARP, WARP)), (5, 5), 0).astype(np.float32)
        m = None if self.prev is None else float(np.abs(top - self.prev).mean() / 255)
        self.prev = top
        return m


class Pipeline:
    """Both models and the settings they were trained with (meta.json from the notebook)."""

    def __init__(self, board_weights, pieces_weights, meta=None, half=True, imgsz=640):
        from ultralytics import YOLO
        meta = meta or {}
        self.board, self.pieces = YOLO(board_weights), YOLO(pieces_weights)
        self.foot, self.pad = meta.get('foot', FOOT), meta.get('pad', PAD)
        self.half, self.imgsz = half, imgsz

    def find_corners(self, img):
        """The surest board's corners (4, 2) in the image, or None."""
        r = self.board.predict(img, imgsz=self.imgsz, conf=0.4, half=self.half, verbose=False)[0]
        if r.keypoints is None or not len(r.boxes):
            return None
        c = r.keypoints.xy[int(r.boxes.conf.argmax())].cpu().numpy().astype(np.float32)
        return c if plausible(c, img.shape[1], img.shape[0]) else None

    def find_pieces(self, img, corners):
        """Pieces in the board's crop, in image coordinates: boxes (n, 4), classes (n,), confidences (n,)."""
        x0, y0, x1, y1 = board_crop(corners, img.shape[1], img.shape[0], self.pad)
        r = self.pieces.predict(img[y0:y1, x0:x1], imgsz=self.imgsz, conf=0.3, iou=0.5, agnostic_nms=True,
                                half=self.half, verbose=False)[0]
        b = r.boxes
        return (b.xyxy.cpu().numpy() + np.float32([x0, y0, x0, y0]), b.cls.cpu().numpy().astype(int),
                b.conf.cpu().numpy())

    def __call__(self, img, track=None):
        """A BGR frame -> what the client draws and reads moves from (coordinates as fractions of the frame)."""
        h, w = img.shape[:2]
        corners = self.find_corners(img)
        if track is not None:
            corners = track.update(corners, w, h)
        if corners is None:
            return {'corners': None, 'board': None, 'conf': None, 'boxes': [], 'motion': None}
        boxes, cls, conf = self.find_pieces(img, corners)
        board, best = place(corners, boxes, cls, conf, self.foot)
        motion = track.motion(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), corners) if track is not None else None
        s = np.float32([w, h, w, h])
        return {
            'corners': np.round(corners / s[:2], 4).tolist(),
            'board': board,
            'conf': np.round(best, 2).tolist(),
            'boxes': [[*np.round(bx / s, 4).tolist(), LETTERS[c], round(float(p), 2)] for bx, c, p in zip(boxes, cls, conf)],
            'motion': None if motion is None else round(motion, 4),
        }
