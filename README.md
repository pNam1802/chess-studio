# Chess Move Studio

Dựng video nước cờ kiểu TikTok ngay trong trình duyệt: camera bám quân, quân nảy và xoay, ô đích phát sáng, huy hiệu đánh giá (`!!`, `!`, `?!`, `??`…), cảnh "BRILLIANT MOVE", dải chiếu đỏ khi chiếu Vua, vua đổ khi chiếu hết, và khớp nước đi theo nhịp nhạc.

Toàn bộ là một file `chess-move-studio.html`, không cần cài đặt hay server. Riêng chế độ **Camera** (đọc ván cờ thật qua camera) cần một máy chủ nhận diện chạy trên GPU, xem [Camera ván thật](#camera-ván-thật).

## Chế độ Nhanh

Lần đầu mở trang sẽ vào chế độ **Nhanh**: 3 bước thay cho 3 thẻ cài đặt.

1. **Ván cờ:** dán link Lichess, PGN (kể cả từ Chess.com) hoặc chuỗi nước đi vào một ô, hoặc thử ván mẫu. Trang tự nhận loại, hiện tóm tắt (*"42 nước · Trắng thắng · 1 nước !!, 2 nước ??"*), tự tìm nước hay và nước hỏng (xem dưới), rồi tự chọn đoạn dựng: bắt đầu 2 nước trước nước hay nhất (`!!`, nếu không có thì `??`) đến hết ván, dài gần nhất với lựa chọn **Ngắn / Vừa / Dài** (khoảng 20 / 35 / 60 giây).
2. **Phong cách:** chọn một bộ phong cách theo ảnh xem trước, sửa chữ phía trên, tên kênh và tỉ lệ khung hình.
3. **Nhạc & xuất:** chọn file nhạc (không bắt buộc, cao trào được tự tìm), rồi bấm **Xuất video**.

Chế độ Nhanh chỉ ghi vào các cài đặt của chế độ **Tùy chỉnh**, nên chuyển qua lại không mất gì và video ra giống hệt nhau. Mục nào chỉnh riêng ở Tùy chỉnh mà Nhanh không hiện sẽ được ghi chú ở cuối.

## Tự tìm nước hay

Nút **Tự tìm nước hay** (tự chạy khi nạp ván ở chế độ Nhanh) gắn huy hiệu cho các nước **chưa có ký hiệu**, theo mức một nước làm mất cơ hội thắng (Win%, cùng công thức với Lichess):

| Ký hiệu | Khi nào |
|---|---|
| `??` / `?` / `?!` | mất ≥ 30 / ≥ 20 / ≥ 10 điểm Win% |
| `!!` | tốt như nước tốt nhất, có thí quân, ván chưa ngã ngũ, nước tốt thứ hai kém hơn rõ |
| `!` | nước duy nhất giữ thế (nước thứ hai mất ≥ 15), không thí quân |

Ván Lichess đã được phân tích thì dùng luôn đánh giá của Lichess (`[%eval]`), ra `?!` `?` `??` ngay lập tức. Còn lại dùng Stockfish chạy trong trình duyệt (khoảng 0,3 giây mỗi thế cờ, ván 40 nước chừng 20–25 giây, có thanh tiến độ và nút Huỷ). Stockfish được tải từ CDN ở lần dùng đầu nên cần mạng; không có mạng thì các phần khác vẫn chạy bình thường. Nút **Xoá đánh giá tự động** chỉ xoá các ký hiệu do máy gắn.

Máy chấm theo đúng thực lực của nước đi, nên vài nước nổi tiếng được gắn khác sách vở: trong bẫy Blackburne Shilling, `4.Nxe5` và `4...Qg5` thực ra gần cân bằng (Trắng có `5.Bxf7+`), chỉ `5.Nxf7??` mới thua; `24.Rxd4` của Kasparov bị Stockfish đánh giá là không chính xác. Muốn giữ `!!` cho những nước này thì gắn tay, máy không ghi đè.

## Cách dùng (chế độ Tùy chỉnh)

1. Mở `chess-move-studio.html` bằng Chrome hoặc Edge trên máy tính.
2. Gõ nước đi, ví dụ `e4 e5 Nf3 Nc6 Bc4 | Nd4?! Nxe5?? Qg5!! Nxf7`.
   Phần trước dấu `|` được xếp sẵn lên bàn, phần sau mới được dựng chuyển động. Thêm `!!`, `!`, `!?`, `?!`, `?`, `??` sau nước để gắn huy hiệu.
   Hoặc lấy cả ván có sẵn: dán link ván / chương nghiên cứu Lichess vào ô **Lấy ván từ Lichess**, hay dán PGN (ví dụ từ Chess.com: Share → PGN) vào ô Nước đi. Header, bình luận, biến thể được bỏ qua, `[FEN]` thành thế bắt đầu, ký hiệu `$1`…`$6` thành huy hiệu.
   Bấm vào một nước trong danh sách nước dưới ô nhập để gắn huy hiệu, chọn **Bắt đầu dựng từ nước này**, hoặc bấm ô trên bàn cờ nhỏ để vẽ dải tấn công. Trang tự ghi lại vào ô Nước đi theo đúng cú pháp trên.
3. Chọn tỉ lệ khung hình: 9:16 (TikTok, Reels, Shorts), 4:5 (Instagram), 1:1, 16:9 (YouTube).
4. Chọn file nhạc, bấm **Tự tìm cao trào** để quân Brilliant đập xuống đúng lúc nhạc dồn. Nếu máy chọn sai đoạn: bấm **Nghe cả bài**, nghe tới chỗ nhạc dồn thì bấm **Đặt cao trào ở đây** (trong lúc nghe, bấm lên dải sóng nhạc để tua). Cũng có thể bấm / kéo thẳng trên dải hoặc chọn một mốc gợi ý, chỉnh bằng **‹ 1 nhịp / 1 nhịp ›**, rồi **Nghe quanh cao trào** để kiểm tra. Mặc định chỉ nước `!!` khớp nhạc, các nước khác đi theo tốc độ đã chỉnh; bật **Các nước khác cũng rơi theo nhịp** nếu muốn mọi nước chạm bàn đúng nhịp. **Lặng trước cao trào** (bật sẵn): 2 nhịp trước nước `!!` nhạc tối dần, một tiếng riser dâng lên, rồi im hẳn khoảng 0,16 giây trước khi quân đập xuống cùng cao trào. **Bám beat thật của bài** (bật sẵn) dò từng beat trong nhạc, lần ra từ cao trào, nên các nước vẫn rơi đúng beat khi bài nhanh chậm dần hoặc BPM đo hơi lệch; tắt đi thì dùng lưới nhịp đều theo BPM.
5. Bấm **Phát xem trước**, rồi **Xuất video** để tải file `.mp4`.

Cài đặt được tự lưu trong trình duyệt; nút **Về mặc định** đưa mọi thứ về ban đầu.

Khung xem trước dùng như trình phát video: bấm vào video hoặc phím Space để phát/dừng, kéo thanh để tua, phím ← → tua 1 giây.

## Phong cách

**Nước sai (`?`, `??`):** bàn cờ giữ nguyên màu, ô đến chỉ tô nhạt màu cam / đỏ, huy hiệu rơi xuống và nảy. Kiểu cũ (bàn xám, phủ đỏ, quân giật hình, chữ BLUNDER) vẫn còn trong code là `BLUNDER_STYLES.glitch`.

Thẻ giao diện có mục **Phong cách**: chọn một bộ (*Studio*, *Bàn online*, *Đêm*, *Gỗ*, *TikTok*) rồi đổi riêng từng phần nếu muốn: ô vừa đi (sáng, phẳng, viền), dải tấn công (ô bật đỏ, mũi tên, hoặc *lộ trình*: đường đỏ phát sáng theo đúng đường quân đi, chữ L cho mã), loé màn hình khi đáp (đỏ khi chiếu, xanh khi ăn quân), huy hiệu (tròn hoặc sticker), cùng màu bàn cờ và kiểu cảnh Brilliant (Aura, Cổ điển, *Lật đồng xu*: quân dày lật 3D trên nền mờ, có vòng đánh dấu ô đích).

**Cảnh chiếu hết:** *Vua đổ* (vua ngã xuống) hoặc *Chém kiểu anime*: quân chiếu hết bay lên, một vòng quay vũ khí (kiếm, thương, liềm, rìu) quay quanh nó càng lúc càng nhanh rồi khựng lại chốt một món, vua bị khoá mục tiêu; quân giơ vũ khí lao xuống và chém đôi vua ngay lúc chạm bàn (khung hình đảo màu, vệt chém, tia lửa, chữ 斬, rung màn hình). Mỗi vũ khí có đường chém riêng. Chọn *Ngẫu nhiên* (cố định theo nước chiếu hết) hoặc một vũ khí cụ thể.

Huy hiệu ghi sau nước: `!!` `!` `*` (★ tốt nhất) `=` (📖 lý thuyết) `!?` `?!` `?` `??`.

Trong code, mỗi phần là một "khe" có nhiều biến thể cùng giao diện hàm: `BADGE_STYLES`, `HIGHLIGHT_STYLES`, `LANE_STYLES`, `BRILLIANT_STYLES`, `BLUNDER_STYLES`; màu và font nằm ở `PALETTE`, `FONT`, `THEMES`, `BADGES`. Thêm một kiểu mới là thêm một mục vào khe đó (và một nút trong ô chọn), bộ phong cách nằm ở `PRESETS`.

## Kể chuyện

- **Thanh đánh giá:** dưới chữ phía trên, cho thấy cơ hội thắng của Trắng (Win%) và điểm số; trượt sang giá trị mới khi quân đáp, loé theo màu huy hiệu khi thế cờ đổi mạnh. Chỉ hiện khi mọi thế cờ trong đoạn dựng đã được đánh giá (bấm **Tự tìm nước hay**, hoặc ván Lichess có `[%eval]`).
- **Chữ chiến thuật:** ngoài FORK! và DOUBLE CHECK, trang tự ghi **SKEWER** (xiên) và **PIN** (ghim) khi quân Tượng / Xe / Hậu vừa đi nhắm qua một quân vào quân phía sau. Chữ PIN / SKEWER đi kèm dải tấn công, nên hiện khi nước đi chiếu Vua hoặc có ghi mục tiêu `{…}`.

## Chuyển động

Trong Phong cách → **Chuyển động**, mỗi mục bật/tắt riêng:

- **Tiêu điểm:** khi một quân bắt đầu đi, khung hình chìm vào bóng tối (ánh sáng kiểu phim, low-key), chỉ còn ô đi và ô đến sáng lên thành hai ô vuông, ánh sáng hắt mềm ra xung quanh mỗi ô (trắng khi quân đang bay; lúc quân đáp, ô đến đổi sang màu của nước đi: xanh lá cho nước tốt `!` / `★`, xanh lam cho nước thiên tài `!!`, nước sai `?!` / `?` / `??` chỉ tô nhạt màu vàng / cam / đỏ trong ô, không hắt sáng); khi quân bay, ánh sáng chuyển dần từ ô đi sang ô đến và loé lên lúc quân đáp. Đi kèm viền tối quanh khung hình và hạt phim. Quân đáp xong thì bàn sáng lại. Không áp dụng ở cảnh `!!` và cảnh chiếu hết kiểu anime (chúng có cảnh riêng).
- **Vệt sáng theo quân:** một dải sáng bám sau quân đang bay, đuôi mảnh và mờ dần.
- **Quân bị ăn:** *Văng ra*: quân bị hất bay theo hướng nước đi, xoay, rơi rồi mờ đi, kèm vòng sóng và mảnh vụn ở ô đó; *Mờ dần*: như cũ.
- **Kết video:** *Tua ngược*: sau nước cuối, cả video chạy ngược về khung đầu trong 1,4 giây (lệch màu, vạch nhiễu như băng từ, nhạc chậm dần rồi tắt như băng dừng, có tiếng tua), khung cuối trùng khung đầu nên video lặp lại liền mạch trên TikTok / Shorts.

Vệt sáng dùng màu huy hiệu của nước đó, trừ nước `?` / `??` dùng màu vàng thường để không lộ trước khi quân đáp.

## Hiệu ứng và camera

- **Dải chiếu:** khi chiếu Vua, các ô từ quân chiếu tới Vua lần lượt bật đỏ, camera lùi ra cho thấy cả dải (có tính chiếu mở và chiếu đôi). Bật/tắt bằng ô tick "Dải chiếu".
- **Camera khi bên kia đi:**
  - *Lùi vừa đủ* (mặc định): trượt hoặc lùi vừa đủ để thấy nước của bên kia.
  - *Lùi ra toàn bàn*: lùi ra toàn bàn rồi bên kia mới đi.
  - *Đứng yên*: giữ camera như cũ.

## Xuất video

Video được dựng từng khung hình (60fps) bằng WebCodecs và ghép thành `.mp4` (H.264 + AAC) với [mp4-muxer](https://github.com/Vanilagy/mp4-muxer) (MIT, nhúng sẵn trong file), nên máy chậm cũng không bị giật hay lệch tiếng. Trình duyệt không có WebCodecs sẽ tự chuyển sang ghi theo thời gian thực.

## Nhạc

Bản trên GitHub không nhúng sẵn bài hát nào vì lý do bản quyền: hãy chọn file nhạc của bạn trong trang, hoặc xuất video **Không nhạc** rồi gắn sound trên TikTok.

## Camera ván thật

Chế độ **Camera** đọc một ván cờ thật qua webcam hoặc điện thoại theo thời gian thực: tìm bàn cờ, nhận quân, ghi lại từng nước đi, và vẽ nước tốt nhất của Stockfish thành mũi tên nằm trên bàn cờ ngay trong video. Chơi xong, bấm **Dựng video từ ván này** để chuyển ván sang chế độ Nhanh.

Cách hoạt động:

1. Trang gửi khung hình (JPEG, cạnh dài 960 px, tối đa 15 khung/giây) qua WebSocket tới máy chủ trên GPU của Modal. Mỗi lúc có tối đa 3 khung chờ trả lời, nên máy chủ ở xa vẫn nhận đủ hình.
2. Máy chủ (`live/modal_app.py`, `live/chessvision.py`) chạy hai model YOLO11: model **pose** tìm 4 góc bàn cờ, rồi từ đó tính homography; model **detect** nhận 12 loại quân trong vùng cắt quanh bàn. Mỗi quân thuộc về ô dưới chân nó (đáy khung nhận diện, nâng lên một chút vì camera nhìn chéo). Máy chủ còn làm mượt các góc qua nhiều khung và đo mức thay đổi của bàn so với khung trước.
3. Trang theo dõi ván: khi bàn đứng yên (không có tay) đủ 4 khung, các khung bỏ phiếu theo từng ô ra một thế cờ. Trang tìm nước đi hợp lệ (hoặc hai nước, hoặc một nước lùi) biến thế của ván thành thế vừa thấy, nên nhận nhầm 1–2 quân không làm hỏng ván. Ván bắt đầu khi camera thấy thế ban đầu, nhìn từ phía nào cũng được. Bàn đang chơi dở thì chọn bên đi rồi bấm **Dùng thế đang thấy**.
4. Mỗi thế mới được đưa vào Stockfish (chính bản chạy trong trình duyệt của Tự tìm nước hay) để tìm nước tốt nhất.

**Hiện khung nhận diện** vẽ lưới ô, khung từng quân kèm độ tin cậy, và tô đỏ những ô mà máy thấy khác với ván. Nếu bàn bị nhận lệch hướng (a1 sai góc), bấm **Xoay bàn 90°**.

Đặt camera nhìn chéo xuống bàn sao cho thấy đủ 4 góc bàn, đủ sáng, quân không che nhau quá nhiều.

### Cài đặt

**1. Train model trên Kaggle** (GPU miễn phí). Trên Kaggle: *Create → New Notebook → File → Import Notebook*, chọn `live/train_kaggle.ipynb`. Ở *Settings* chọn **Accelerator: GPU T4 x2** và bật **Internet**, rồi *Run All*. Notebook tải bộ dữ liệu [ChessReD](https://data.4tu.nl/datasets/99b5c721-280b-450b-b058-b2900b69a90f) (bản 2K: 2.078 ảnh bàn cờ thật chụp chéo bằng điện thoại, 4,7 GB), train hai model song song (khoảng 1–1,5 giờ), chạy thử cả quy trình trên các ván test (in ra độ chính xác theo ô), rồi đóng gói `chess-live-weights.zip`. Tải file đó ở khung *Output* và giải nén vào `live/weights/` (`board.pt`, `pieces.pt`, `meta.json`).

**2. Đưa máy chủ lên Modal:**

```
pip install modal
modal token new                     # nếu máy chưa đăng nhập Modal
modal secret create chess-live LIVE_KEY=<một chuỗi ngẫu nhiên dài>
modal deploy live/modal_app.py
modal run live/modal_app.py --image anh-ban-co.jpg   # thử một ảnh: in ra thế cờ đọc được
```

`modal deploy` in ra địa chỉ dạng `https://<tên>--chess-live-vision-web.modal.run`. Dán địa chỉ đó và `LIVE_KEY` vào bước 1 của chế độ Camera (trang chỉ lưu chúng trong trình duyệt này).

Máy chủ dùng GPU T4 (rẻ nhất trên Modal); đổi bằng biến môi trường `CHESS_LIVE_GPU=L4` khi deploy. Máy chủ tự tắt sau 2 phút không nhận hình nên chỉ tốn tiền lúc dùng; lần bật đầu tiên mất khoảng nửa phút. Độ trễ chủ yếu là đường mạng tới máy chủ của Modal (ở Mỹ), số khung/giây và độ trễ hiện ngay dưới nút Bật camera.

Sửa `live/chessvision.py` hoặc `live/train_kaggle.py` thì chạy `python live/make_notebook.py` để tạo lại notebook.

Bộ dữ liệu ChessReD dùng giấy phép CC BY-NC-SA 4.0 (không thương mại), nên model train từ nó cũng chỉ nên dùng phi thương mại.

## Thư viện

- [chess.js](https://github.com/jhlywa/chess.js) (BSD-2-Clause), nhúng sẵn
- [mp4-muxer](https://github.com/Vanilagy/mp4-muxer) 5.1.3 (MIT), nhúng sẵn
- [stockfish.js](https://github.com/niklasf/stockfish.js) 10.0.2 (GPLv3), không nhúng: tải từ jsDelivr khi bấm Tự tìm nước hay
- Chế độ Camera (máy chủ, không nằm trong trang): [Ultralytics YOLO11](https://github.com/ultralytics/ultralytics) (AGPL-3.0), OpenCV, FastAPI, [Modal](https://modal.com); dữ liệu train [ChessReD](https://data.4tu.nl/datasets/99b5c721-280b-450b-b058-b2900b69a90f) (CC BY-NC-SA 4.0, Masouris & van Gemert 2023)
