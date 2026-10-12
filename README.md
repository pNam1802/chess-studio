# Chess Move Studio

Dựng video nước cờ kiểu TikTok ngay trong trình duyệt: camera bám quân, quân nảy và xoay, ô đích phát sáng, huy hiệu đánh giá (`!!`, `!`, `?!`, `??`…), cảnh "BRILLIANT MOVE", vua đổ khi chiếu hết, và khớp nước đi theo nhịp nhạc.

Toàn bộ là một file `chess-move-studio.html`, không cần cài đặt hay server.

## Cách dùng

1. Mở `chess-move-studio.html` bằng Chrome hoặc Edge trên máy tính.
2. Gõ nước đi, ví dụ `e4 e5 Nf3 Nc6 Bc4 | Nd4?! Nxe5?? Qg5!! Nxf7`.
   Phần trước dấu `|` được xếp sẵn lên bàn, phần sau mới được dựng chuyển động. Thêm `!!`, `!`, `!?`, `?!`, `?`, `??` sau nước để gắn huy hiệu.
3. Chọn tỉ lệ khung hình: 9:16 (TikTok, Reels, Shorts), 4:5 (Instagram), 1:1, 16:9 (YouTube).
4. Chọn file nhạc, bấm **Tự tìm cao trào** để quân Brilliant đập xuống đúng lúc nhạc dồn.
5. Bấm **Phát xem trước**, rồi **Xuất video** để tải file `.mp4`.

Cài đặt được tự lưu trong trình duyệt; nút **Về mặc định** đưa mọi thứ về ban đầu.

## Xuất video

Video được dựng từng khung hình (60fps) bằng WebCodecs và ghép thành `.mp4` (H.264 + AAC) với [mp4-muxer](https://github.com/Vanilagy/mp4-muxer) (MIT, nhúng sẵn trong file), nên máy chậm cũng không bị giật hay lệch tiếng. Trình duyệt không có WebCodecs sẽ tự chuyển sang ghi theo thời gian thực.

## Nhạc

Bản trên GitHub không nhúng sẵn bài hát nào vì lý do bản quyền: hãy chọn file nhạc của bạn trong trang, hoặc xuất video **Không nhạc** rồi gắn sound trên TikTok.

## Thư viện

- [chess.js](https://github.com/jhlywa/chess.js) (BSD-2-Clause), nhúng sẵn
- [mp4-muxer](https://github.com/Vanilagy/mp4-muxer) 5.1.3 (MIT), nhúng sẵn
