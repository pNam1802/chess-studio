# Chess Move Studio

Dựng video nước cờ kiểu TikTok ngay trong trình duyệt: camera bám quân, quân nảy và xoay, ô đích phát sáng, huy hiệu đánh giá (`!!`, `!`, `?!`, `??`…), cảnh "BRILLIANT MOVE", dải chiếu đỏ khi chiếu Vua, vua đổ khi chiếu hết, và khớp nước đi theo nhịp nhạc.

Toàn bộ là một file `chess-move-studio.html`, không cần cài đặt hay server.

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
4. Chọn file nhạc, bấm **Tự tìm cao trào** để quân Brilliant đập xuống đúng lúc nhạc dồn. Nếu máy chọn sai đoạn: bấm **Nghe cả bài**, nghe tới chỗ nhạc dồn thì bấm **Đặt cao trào ở đây** (trong lúc nghe, bấm lên dải sóng nhạc để tua). Cũng có thể bấm / kéo thẳng trên dải hoặc chọn một mốc gợi ý, chỉnh bằng **‹ 1 nhịp / 1 nhịp ›**, rồi **Nghe quanh cao trào** để kiểm tra. Mặc định chỉ nước `!!` khớp nhạc, các nước khác đi theo tốc độ đã chỉnh; bật **Các nước khác cũng rơi theo nhịp** nếu muốn mọi nước chạm bàn đúng nhịp. **Lặng trước cao trào** (bật sẵn): 2 nhịp trước nước `!!` nhạc tối dần, một tiếng riser dâng lên, rồi im hẳn khoảng 0,16 giây trước khi quân đập xuống cùng cao trào; ở nước `??` nhạc tắt một nhịp rồi vào lại. **Bám beat thật của bài** (bật sẵn) dò từng beat trong nhạc, lần ra từ cao trào, nên các nước vẫn rơi đúng beat khi bài nhanh chậm dần hoặc BPM đo hơi lệch; tắt đi thì dùng lưới nhịp đều theo BPM.
5. Bấm **Phát xem trước**, rồi **Xuất video** để tải file `.mp4`.

Cài đặt được tự lưu trong trình duyệt; nút **Về mặc định** đưa mọi thứ về ban đầu.

Khung xem trước dùng như trình phát video: bấm vào video hoặc phím Space để phát/dừng, kéo thanh để tua, phím ← → tua 1 giây.

## Phong cách

Thẻ giao diện có mục **Phong cách**: chọn một bộ (*Studio*, *Bàn online*, *Đêm*, *Gỗ*, *TikTok*) rồi đổi riêng từng phần nếu muốn: ô vừa đi (sáng, phẳng, viền), dải tấn công (ô bật đỏ, mũi tên, hoặc *lộ trình*: đường đỏ phát sáng theo đúng đường quân đi, chữ L cho mã), loé màn hình khi đáp (đỏ khi chiếu, xanh khi ăn quân), huy hiệu (tròn hoặc sticker), cùng màu bàn cờ và kiểu cảnh Brilliant (Aura, Cổ điển, *Lật đồng xu*: quân dày lật 3D trên nền mờ, có vòng đánh dấu ô đích).

**Cảnh chiếu hết:** *Vua đổ* (vua ngã xuống) hoặc *Chém kiểu anime*: quân chiếu hết bay lên, một vòng quay vũ khí (kiếm, thương, liềm, rìu) quay quanh nó càng lúc càng nhanh rồi khựng lại chốt một món, vua bị khoá mục tiêu; quân giơ vũ khí lao xuống và chém đôi vua ngay lúc chạm bàn (khung hình đảo màu, vệt chém, tia lửa, chữ 斬, rung màn hình). Mỗi vũ khí có đường chém riêng. Chọn *Ngẫu nhiên* (cố định theo nước chiếu hết) hoặc một vũ khí cụ thể.

Huy hiệu ghi sau nước: `!!` `!` `*` (★ tốt nhất) `=` (📖 lý thuyết) `!?` `?!` `?` `??`.

Trong code, mỗi phần là một "khe" có nhiều biến thể cùng giao diện hàm: `BADGE_STYLES`, `HIGHLIGHT_STYLES`, `LANE_STYLES`, `BRILLIANT_STYLES`, `BLUNDER_STYLES`; màu và font nằm ở `PALETTE`, `FONT`, `THEMES`, `BADGES`. Thêm một kiểu mới là thêm một mục vào khe đó (và một nút trong ô chọn), bộ phong cách nằm ở `PRESETS`.

## Kể chuyện

- **Thanh đánh giá:** dưới chữ phía trên, cho thấy cơ hội thắng của Trắng (Win%) và điểm số; trượt sang giá trị mới khi quân đáp, loé theo màu huy hiệu khi thế cờ đổi mạnh. Chỉ hiện khi mọi thế cờ trong đoạn dựng đã được đánh giá (bấm **Tự tìm nước hay**, hoặc ván Lichess có `[%eval]`).
- **Chữ chiến thuật:** ngoài FORK! và DOUBLE CHECK, trang tự ghi **SKEWER** (xiên) và **PIN** (ghim) khi quân Tượng / Xe / Hậu vừa đi nhắm qua một quân vào quân phía sau, và **BLUNDER** trên nước `??`. Chữ PIN / SKEWER đi kèm dải tấn công, nên hiện khi nước đi chiếu Vua hoặc có ghi mục tiêu `{…}`.

## Chuyển động

Trong Phong cách → **Chuyển động**, mỗi mục bật/tắt riêng:

- **Tiêu điểm:** khi một quân bắt đầu đi, khung hình chìm vào bóng tối (ánh sáng kiểu phim, low-key), chỉ còn hai vùng sáng ấm, mềm mép ở ô đi và ô đến, có bụi lơ lửng trong ánh đèn; khi quân bay, ánh sáng chuyển dần từ ô đi sang ô đến và loé lên lúc quân đáp. Đi kèm viền tối quanh khung hình và hạt phim. Quân đáp xong thì bàn sáng lại. Không áp dụng ở cảnh `!!` và cảnh chiếu hết kiểu anime (chúng có cảnh riêng).
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

## Thư viện

- [chess.js](https://github.com/jhlywa/chess.js) (BSD-2-Clause), nhúng sẵn
- [mp4-muxer](https://github.com/Vanilagy/mp4-muxer) 5.1.3 (MIT), nhúng sẵn
- [stockfish.js](https://github.com/niklasf/stockfish.js) 10.0.2 (GPLv3), không nhúng: tải từ jsDelivr khi bấm Tự tìm nước hay
