"""The vision server for the studio's Camera mode, on a Modal GPU.

    modal secret create chess-live LIVE_KEY=<a long random key>
    modal deploy live/modal_app.py              # prints the https://…modal.run address to paste into the page
    modal run live/modal_app.py --image a.jpg   # one photo through the pipeline, to check the weights

The page opens a WebSocket to /ws?key=LIVE_KEY and sends frames: 4 bytes of frame id (uint32, little endian), then
a JPEG. Each answer is the JSON of chessvision.Pipeline plus "id" and "ms" (the server's time for the frame).
Frames are answered in order; the text message "reset" forgets the camera's steadied corners.
The weights (board.pt, pieces.pt, meta.json from the Kaggle notebook) go in live/weights/ before deploying.
"""
import asyncio
import hmac
import json
import os
import pathlib
import threading
import time

import modal

HERE = pathlib.Path(__file__).parent
GPU = os.environ.get('CHESS_LIVE_GPU', 'T4')

image = (
    modal.Image.debian_slim(python_version='3.11')
    .apt_install('libgl1', 'libglib2.0-0')
    .pip_install('ultralytics>=8.3,<9', 'fastapi[standard]')
    .add_local_file(HERE / 'chessvision.py', '/root/chessvision.py')
    .add_local_dir(HERE / 'weights', '/weights')
)
app = modal.App('chess-live', image=image)

with image.imports():
    import cv2
    import numpy as np
    import chessvision


# one container at most (one camera is one user) that sleeps two minutes after the last frame
@app.cls(gpu=GPU, secrets=[modal.Secret.from_name('chess-live')], scaledown_window=120, timeout=3600, max_containers=1)
@modal.concurrent(max_inputs=4)
class Vision:
    @modal.enter()
    def load(self):
        meta = json.loads(pathlib.Path('/weights/meta.json').read_text())
        self.pipe = chessvision.Pipeline('/weights/board.pt', '/weights/pieces.pt', meta)
        self.lock = threading.Lock()   # the models run one frame at a time
        blank = np.zeros((540, 960, 3), np.uint8)   # warm up: the first predict builds the CUDA kernels
        for model in (self.pipe.board, self.pipe.pieces):
            model.predict(blank, imgsz=self.pipe.imgsz, half=self.pipe.half, verbose=False)

    def run(self, jpeg, track=None):
        t = time.perf_counter()
        img = cv2.imdecode(np.frombuffer(jpeg, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return {'error': 'not a JPEG'}
        with self.lock:
            out = self.pipe(img, track)
        out['ms'] = round((time.perf_counter() - t) * 1000, 1)
        return out

    @modal.method()
    def detect(self, jpeg: bytes) -> dict:
        return self.run(jpeg)

    @modal.asgi_app()
    def web(self):
        from fastapi import FastAPI, WebSocket, WebSocketDisconnect
        api, key = FastAPI(), os.environ['LIVE_KEY']

        @api.get('/')
        def health():
            return {'ok': True}

        @api.websocket('/ws')
        async def frames(sock: WebSocket):
            await sock.accept()
            if not hmac.compare_digest(sock.query_params.get('key', ''), key):
                await sock.close(code=4401)
                return
            track = chessvision.Track()
            try:
                while True:
                    msg = await sock.receive()
                    if msg['type'] == 'websocket.disconnect':
                        break
                    if msg.get('text') == 'reset':
                        track = chessvision.Track()
                        continue
                    data = msg.get('bytes')
                    if not data or len(data) < 5:
                        continue
                    out = await asyncio.to_thread(self.run, data[4:], track)
                    out['id'] = int.from_bytes(data[:4], 'little')
                    await sock.send_json(out)
            except WebSocketDisconnect:
                pass

        return api


@app.local_entrypoint()
def main(image: str):
    out = Vision().detect.remote(pathlib.Path(image).read_bytes())
    b = out.get('board')
    if b:   # the board as a FEN placement, rank 8 first
        rows = [b[i:i + 8] for i in range(0, 64, 8)]
        print('/'.join(''.join(str(len(run)) if run[0] == '.' else run for run in _runs(r)) for r in rows))
    print(json.dumps({k: v for k, v in out.items() if k not in ('boxes', 'conf')}, indent=1))


def _runs(row):
    """'..pP...k' -> ['..', 'p', 'P', '...', 'k']: empty squares grouped, pieces one by one."""
    out = []
    for ch in row:
        if ch == '.' and out and out[-1][0] == '.':
            out[-1] += ch
        else:
            out.append(ch)
    return out
