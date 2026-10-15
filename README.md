# Chess Move Studio

Dựng video nước cờ kiểu TikTok ngay trong trình duyệt: camera bám quân, quân nảy và xoay, ô đích phát sáng, huy hiệu đánh giá (`!!`, `!`, `?!`, `??`…), cảnh "BRILLIANT MOVE", dải chiếu đỏ khi chiếu Vua, vua đổ khi chiếu hết, và khớp nước đi theo nhịp nhạc.

Toàn bộ là một file `chess-move-studio.html`, không cần cài đặt hay server.

## Cách dùng

1. Mở `chess-move-studio.html` bằng Chrome hoặc Edge trên máy tính.
2. Gõ nước đi, ví dụ `e4 e5 Nf3 Nc6 Bc4 | Nd4?! Nxe5?? Qg5!! Nxf7`.
   Phần trước dấu `|` được xếp sẵn lên bàn, phần sau mới được dựng chuyển động. Thêm `!!`, `!`, `!?`, `?!`, `?`, `??` sau nước để gắn huy hiệu.
   Hoặc lấy cả ván có sẵn: dán link ván / chương nghiên cứu Lichess vào ô **Lấy ván từ Lichess**, hay dán PGN (ví dụ từ Chess.com: Share → PGN) vào ô Nước đi. Header, bình luận, biến thể được bỏ qua, `[FEN]` thành thế bắt đầu, ký hiệu `$1`…`$6` thành huy hiệu.
   Bấm vào một nước trong danh sách nước dưới ô nhập để gắn huy hiệu, chọn **Bắt đầu dựng từ nước này**, hoặc bấm ô trên bàn cờ nhỏ để vẽ dải tấn công. Trang tự ghi lại vào ô Nước đi theo đúng cú pháp trên.
3. Chọn tỉ lệ khung hình: 9:16 (TikTok, Reels, Shorts), 4:5 (Instagram), 1:1, 16:9 (YouTube).
4. Chọn file nhạc, bấm **Tự tìm cao trào** để quân Brilliant đập xuống đúng lúc nhạc dồn. Nếu máy chọn sai đoạn: bấm **Nghe cả bài**, nghe tới chỗ nhạc dồn thì bấm **Đặt cao trào ở đây** (trong lúc nghe, bấm lên dải sóng nhạc để tua). Cũng có thể bấm / kéo thẳng trên dải hoặc chọn một mốc gợi ý, chỉnh bằng **‹ 1 nhịp / 1 nhịp ›**, rồi **Nghe quanh cao trào** để kiểm tra. Mặc định chỉ nước `!!` khớp nhạc, các nước khác đi theo tốc độ đã chỉnh; bật **Các nước khác cũng rơi theo nhịp** nếu muốn mọi nước chạm bàn đúng nhịp.
5. Bấm **Phát xem trước**, rồi **Xuất video** để tải file `.mp4`.

Cài đặt được tự lưu trong trình duyệt; nút **Về mặc định** đưa mọi thứ về ban đầu.

Khung xem trước dùng như trình phát video: bấm vào video hoặc phím Space để phát/dừng, kéo thanh để tua, phím ← → tua 1 giây.

## Phong cách

Thẻ giao diện có mục **Phong cách**: chọn một bộ (*Studio*, *Bàn online*, *Đêm*, *Gỗ*, *TikTok*) rồi đổi riêng từng phần nếu muốn: ô vừa đi (sáng, phẳng, viền), dải tấn công (ô bật đỏ, mũi tên, hoặc *lộ trình*: đường đỏ phát sáng theo đúng đường quân đi, chữ L cho mã), loé màn hình khi đáp (đỏ khi chiếu, xanh khi ăn quân), huy hiệu (tròn hoặc sticker), cùng màu bàn cờ và kiểu cảnh Brilliant (Aura, Cổ điển, *Lật đồng xu*: quân dày lật 3D trên nền mờ, có vòng đánh dấu ô đích).

Huy hiệu ghi sau nước: `!!` `!` `*` (★ tốt nhất) `=` (📖 lý thuyết) `!?` `?!` `?` `??`.

Trong code, mỗi phần là một "khe" có nhiều biến thể cùng giao diện hàm: `BADGE_STYLES`, `HIGHLIGHT_STYLES`, `LANE_STYLES`, `BRILLIANT_STYLES`, `BLUNDER_STYLES`; màu và font nằm ở `PALETTE`, `FONT`, `THEMES`, `BADGES`. Thêm một kiểu mới là thêm một mục vào khe đó (và một nút trong ô chọn), bộ phong cách nằm ở `PRESETS`.

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

## Thư viện

- [chess.js](https://github.com/jhlywa/chess.js) (BSD-2-Clause), nhúng sẵn
- [mp4-muxer](https://github.com/Vanilagy/mp4-muxer) 5.1.3 (MIT), nhúng sẵn
