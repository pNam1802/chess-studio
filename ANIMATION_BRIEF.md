# Chess Move Studio — Bản tóm tắt cho giám khảo animation

Tài liệu này mô tả **hiện trạng** của dự án để một AI Agent giám khảo hiểu hệ thống đang làm gì, rồi đề xuất cách làm animation hay hơn và mượt hơn. Mọi con số dưới đây lấy từ code hiện tại.

- Repo: https://github.com/pNam1802/chess-studio (bản phát hành `v1.0`; bản làm việc đã có thêm Dải tấn công và Ván mẫu)
- File chính: `chess-move-studio.html`, khoảng 3.300 dòng. Tất cả trong một file: HTML, CSS, JS, ảnh quân cờ SVG và âm thanh nhúng base64.

---

## 1. Sản phẩm là gì

Một trang web chạy cục bộ: người dùng gõ nước cờ, trang dựng thành **video ngắn kiểu TikTok** (mặc định 9:16, 1080×1920, 60fps), rồi xuất ra `.mp4`. Phong cách hướng tới các video "chess edit" trên TikTok:
- Camera bám sát quân.
- Quân nảy, nghiêng, xoay.
- Huy hiệu đánh giá kiểu Chess.com (`!!`, `!`, `!?`, `?!`, `?`, `??`, `#`).
- Cảnh "BRILLIANT MOVE" hoành tráng.
- Chuyển động khớp nhịp nhạc (beat), cú đập của nước `!!` rơi đúng điểm cao trào (drop) của bài.

**Người dùng:** người làm nội dung cờ vua trên TikTok, không phải lập trình viên.

**Ví dụ đầu vào:**
```
e4 e5 Nf3 Nc6 Bc4 | Nd4?! Nxe5?? Qg5!! Nxf7{g5,h8}
```
- Phần trước `|` được xếp sẵn lên bàn, phần sau được dựng chuyển động.
- Ký hiệu sau nước (`!!`, `??`…) gắn huy hiệu.
- `{ô,ô}` dính liền sau nước khai báo mục tiêu cho "dải tấn công".

---

## 2. Ràng buộc kỹ thuật (giải pháp đề xuất cần tôn trọng)

1. **Một file HTML, không có bước build.** Thư viện ngoài phải nhúng sẵn hoặc lấy từ CDN có ghim phiên bản. Hiện đã nhúng chess.js và mp4-muxer.
2. **Canvas 2D**, không WebGL. Mỗi khung hình được vẽ lại toàn bộ.
3. **`render(t)` phải tất định (deterministic):** cùng `t` thì ra cùng một hình, không phụ thuộc thời gian thực, không dùng `Math.random()` hay trạng thái tích luỹ giữa các frame. Bắt buộc, vì xuất video **offline**: vẽ lần lượt từng khung `t = i/60` rồi mã hoá bằng WebCodecs (H.264 + AAC) và ghép mp4. Hiệu ứng mô phỏng vật lý theo từng bước (particles có trạng thái, spring tích phân dần) **không dùng được**, trừ khi viết lại thành dạng hàm đóng theo `t`, hoặc mô phỏng lại từ đầu mỗi lần một cách tất định.
4. **Âm thanh** (tiếng quân, whoosh, boom, nhạc) được lên lịch theo cùng timeline và dựng offline bằng `OfflineAudioContext`. Mọi hiệu ứng có âm thanh phải có thời điểm xác định trước.
5. **Khớp nhạc:** timeline được "snap" lên lưới beat (BPM + giây cao trào). Thay đổi thời lượng một hiệu ứng có thể làm lệch nhịp, xem mục 6.
6. **Hiệu năng:** xem trước chạy realtime trên laptop phổ thông bằng Chrome/Edge.
7. **4 tỉ lệ khung hình:** 9:16, 4:5, 1:1, 16:9. Toạ độ overlay được tính tương đối theo khung.

---

## 3. Kiến trúc animation

```
parse()        đọc nước đi → danh sách ply {mv, badge, targets} + thế cờ sau mỗi ply
layout()       dựng TIMELINE: gán cho mỗi ply các mốc thời gian và tham số hiệu ứng
buildClip()    nếu ván dài: tìm nhị phân hệ số tăng tốc để cú !! rơi đúng drop của nhạc
camera(t)      hàm thuần: t → {cx, cy, s (px/ô), roll}
render(t)      vẽ một khung: renderBoard → drawImpact (Brilliant) → drawCard (thẻ Brilliant)
soundEvents()  danh sách [thời điểm, phát âm] lấy từ cùng timeline
```

**Mốc thời gian của mỗi ply `p`:**
- `p.start`: camera bắt đầu chuyển sang nước này.
- `p.moveStart = start + pan`: quân nhấc lên.
- `p.arrive`: quân chạm ô đích.
- `p.end`: hết thời gian giữ, bắt đầu nước sau.

**Toạ độ:** "board space" tính theo đơn vị ô (0..8), lật bàn khi người chơi cầm Đen. `boardTf(cam)` chuyển sang pixel; `toScreen()` dùng cho overlay.

**Hàm easing đang dùng:**
- `eio`: easeInOutCubic.
- `eout`: easeOutCubic.
- `eback`: easeOutBack, hệ số 1.9.
- Spring "giả" dạng đóng: `exp(-6s)·cos(14s)` cho cú nén khi quân đáp.

---

## 4. Danh mục hiệu ứng hiện có (kèm thông số)

`sp` là thanh "Tốc độ" (mặc định 1). Mọi thời gian chia cho `sp`.

### 4.1 Nhịp chung của một nước
| Pha | Thời lượng |
|---|---|
| Mở đầu: giữ toàn bàn | 1.5s (chỉnh được 0–4s), rồi đẩy camera vào nước đầu trong 0.9s |
| Camera chuyển sang nước (pan) | 0.3s |
| Quân bay | 0.72s; nước "spin" 1.6×; nước `!!` 2.6× (slow-motion) |
| Giữ sau khi đáp | 1.0s; có huy hiệu thì 1.35s |
| Kết: camera lùi ra thêm 1.4 ô | 2.0s |

**Tăng tốc ván dài** (`ACCEL = {from: 6, calm: 3, max: 3}`): nếu trước `!!` có hơn 6 nước, phần đầu chạy nhanh tới 3× (nhân thêm hệ số khớp nhạc, tối đa 8×) và chậm dần về bình thường ở 3 nước cuối trước `!!`.

### 4.2 Quân di chuyển
- **Nước thường:**
  - Quân đi theo `eio`, bay vòng cung `sin(πu)`.
  - Phóng to 1 + 0.2·cung, nghiêng ±0.26 rad theo hướng đi, nhấc 0.22 ô, có bóng đổ khi bay.
  - Khi đáp: nén lò xo `sx = 1 + 0.1·wob`, `sy = 1 − 0.12·wob` trong 0.32s.
- **Ăn quân:** quân bị ăn mờ và co lại trong 0.22s sau khi quân kia đáp.
- **Nhập thành:** Xe trượt cùng lúc (`eio`, trễ 15%).
- **Nước "spin"** (nước của mình sau nước `!!`) và nước `!!`:
  - Quân bốc lên, to dần (tới 1.4× hoặc 1.75×), xoay đúng một vòng 360° trên không.
  - Rồi đập mạnh xuống ở 82–86% thời gian bay.
  - Nén khi đáp mạnh gấp 1.8 lần nước thường.
- **Chiếu hết:**
  - Ô Vua đỏ dần.
  - Vua đổ nghiêng 90° với gia tốc `k²` trong 0.42s, nảy lại nhỏ.

### 4.3 Ô sáng và huy hiệu
- Ô đi và ô đến sáng theo màu huy hiệu (mặc định vàng `#F5CD3A`), kèm quầng sáng gradient tròn khi đáp.
- Ô sáng của nước trước mờ đi trong 0.3s.
- Huy hiệu tròn ở góc trên phải ô đích, bật lên bằng `eback` trong 0.38s.

### 4.4 Camera
- Zoom tính theo **số ô thấy được trên cạnh ngắn** của khung, mặc định 5 ô.
- **Bám quân:** tâm camera đặt ở 62% quãng từ ô đi tới ô đến. Khi quân đáp có cú "punch-in" 4.5% trong 0.5s.
- **Nước của bên kia** (tuỳ chọn):
  - `fit` (mặc định): lùi hoặc trượt vừa đủ thấy ô đi và ô đến, xê dịch ít nhất có thể. Camera tới nơi xong rồi quân mới đi.
  - `wide`: lùi ra toàn bàn.
  - `still`: đứng yên, chỉ trượt ngang.
  - Số đo trên ván 18 nước: `still` để quân bên kia bị khuất **36%** thời gian di chuyển; `fit` 0%, không thêm zoom; `wide` 0% nhưng tổng lượng zoom ra vào gấp **6 lần** (camera dập dềnh).
- **Cảnh toàn bàn** (mở đầu, trước `!!`): ở khung thấp (1:1, 16:9), bàn tự thu nhỏ để không bị tiêu đề đè.
- **Rung màn hình:** biên độ 22px, giảm theo bình phương trong 0.3s, khi `!!` đập xuống và khi chữ BRILLIANT xuất hiện.

### 4.5 Cảnh BRILLIANT (nước `!!`), hiệu ứng "đinh" của sản phẩm
1. **Reveal:** camera lùi ra toàn bàn trong 0.7s, giữ 0.6s cho người xem đọc thế cờ.
2. **Thẻ teaser:**
   - Bàn tối và xám đi.
   - Quân sắp đi hiện to giữa màn hình, kèm huy hiệu `!!` bật lên.
   - Chữ "BRILLIANT MOVE" trượt vào, khoảng cách chữ co lại, có motion-blur giả bằng cách vẽ chồng nhiều lớp mờ.
   - Chữ phụ trượt vào từ phía ngược lại.
   - Thời lượng: vào 0.45s, giữ 1.6s, ra 0.35s.
   - Lúc chữ đập vào có chớp trắng 0.08s. Khoảnh khắc này được khớp với **drop của nhạc**.
3. **Bay:** quân thu nhỏ về ô của nó, rồi bay spin slow-motion (2.6× thời gian), bàn xám, ô đích sáng màu teal.
4. **Impact** (1.7s):
   - Chớp trắng 0.07s.
   - Pha "x-ray" 0.9s: lưới trắng phồng kiểu fisheye, các quân khác thành bóng tối viền trắng.
   - Quân `!!` phát sáng trên ô màu teal.
   - Các vòng tròn lan ra quanh huy hiệu.
   - Camera zoom vào 22% rồi nhả dần; rung màn hình.
   - Thoát ra trong 0.25s bằng một chớp sáng.

### 4.6 Dải tấn công (mới nhất, bản làm việc)
- **Dải** là các ô cờ thật nằm trên đường từ quân tấn công tới mục tiêu:
  - Xe/Tượng/Hậu: cả hàng, cột hoặc đường chéo.
  - Mã/Tốt/Vua: chỉ 2 ô.
- **Màu và nhịp:**
  - Đỏ `#E24B4A`, vẽ dưới quân cờ.
  - Bắt đầu 0.1s sau khi quân đáp. Nước ăn quân thì 0.25s, đợi quân bị ăn biến mất.
  - Các ô sáng lần lượt, mỗi ô trễ 0.1s, hiện trong 0.18s.
  - Độ đậm 0.3 ở ô đầu, 0.5 ở các ô giữa, 0.85 ở ô mục tiêu, ô mục tiêu nhấp nháy.
  - Mờ đi trong 0.25s khi sang nước sau.
- **Chọn mục tiêu:**
  - Ô ghi tay `{…}`.
  - Không ghi thì: nếu là nước chiếu, tự vẽ dải tới Vua (tính cả chiếu mở và chiếu đôi).
  - Tối đa 2 dải, ưu tiên Vua > Hậu > Xe > quân nhẹ > Tốt.
  - Không áp dụng cho nước `!!`.
- **Quân mục tiêu nảy:** lên 0.12 ô rồi nén khi chạm bàn (0.35s), thêm một cú nảy 0.05 ô.
- **Fork** (từ 2 dải trở lên):
  - Các dải lan đồng bộ (dải ngắn kéo dài bước nhảy) để mọi mục tiêu nảy cùng lúc.
  - Chữ "FORK!" đỏ phát sáng, viền tối, bật lên bằng `eback`.
- **Camera:** lùi ra thấy mọi dải cộng lề 1 ô, `eio` trong 0.8s, chạy song song với dải.
- **Chiếu hết:** dải chạy trước, Vua nảy, rồi mới đổ.

### 4.7 Âm thanh gắn với animation
- Tiếng đi quân, ăn quân, nhập thành, chiếu: clip thu sẵn. Không có clip thì dùng tiếng "knock" tổng hợp.
- Nước `!!`: whoosh lúc thẻ teaser vào và lúc quân bay, "boom" trầm lúc đập.
- Âm chiếu hết khi Vua đổ.

---

## 5. Thứ đã thử và bị loại (để giám khảo không đề xuất lại)

- **"Target lock" kiểu ống ngắm:** tia đỏ có mũi tên (đường cong với Mã), vòng tâm ngắm thu nhỏ, quân mục tiêu run ngang, quân tấn công lao về phía mục tiêu.
  - Người dùng **không thích**.
  - Muốn hình ảnh "các ô cờ thật sáng lên" thay vì tia hay mũi tên. Đó là lý do có Dải tấn công.
- **Camera `wide` làm mặc định cho nước của bên kia:** đã chuyển thành tuỳ chọn phụ vì camera dập dềnh (số đo ở mục 4.4).

---

## 6. Hạn chế và điểm yếu đã biết

1. **Tiêu đề và tên kênh đè lên bàn:** khi zoom vào, hàng quân trên cùng hoặc dưới cùng có thể nằm dưới thanh tiêu đề hay tên kênh. Camera chưa "né" vùng UI.
2. **Ô xuất phát của dải Mã gần như không thấy đỏ:** màu cam của ô vừa đi đè lên lớp đỏ 0.3.
3. **Cú nảy của quân mục tiêu khó thấy** ở zoom mặc định trên khung 9:16 (0.12 ô ≈ 26px).
4. **Chiếu đôi cũng hiện "FORK!"** vì quy tắc "từ 2 dải trở lên".
5. **Cấu trúc easing chưa thống nhất:** mỗi hiệu ứng tự viết đường cong và thời lượng riêng, chưa có hệ thống motion chung (bảng thời lượng, bảng easing, quy tắc chồng lớp hiệu ứng).
6. **Ít hiệu ứng nối giữa các nước:** chuyển cảnh chủ yếu dựa vào camera lerp, chưa có anticipation hay follow-through cho camera; mọi chuyển động camera đều là `eio`.
7. **Khung 16:9:** cảnh toàn bàn khá nhỏ vì tiêu đề nằm phía trên bàn chứ không ở bên cạnh.
8. **Chưa có:** đánh giá nước bằng engine (Stockfish, dự kiến phần 2, để tự gợi ý `!!`, `??` và mục tiêu tấn công), hiệu ứng riêng cho `??` hay `?`, chữ nổi cho thuật ngữ khác (PIN, SKEWER, DISCOVERED…), chuyển cảnh giữa các ván.

---

## 7. Câu hỏi mong giám khảo trả lời

1. Làm sao để toàn bộ chuyển động có **một ngôn ngữ motion thống nhất** (timing, easing, overshoot) mà vẫn khớp lưới beat của nhạc?
2. Camera: nên dùng đường cong hay mô hình gì (ví dụ critically-damped spring viết dạng đóng theo `t`, look-ahead, dead-zone) để bám quân **mượt và có chủ đích** hơn, tránh dập dềnh, và né vùng tiêu đề và tên kênh?
3. Dải tấn công và cảnh Brilliant: cần thêm hoặc bớt gì (anticipation, impact frame, hold, màu, độ tương phản) để **đọc được trong 1 giây trên điện thoại**?
4. Nên ưu tiên hiệu ứng nào cho phần tiếp theo (`??` / blunder, PIN, SKEWER, phong cấp, chiếu mở), và mỗi cái nên trông thế nào để không đè lên các hiệu ứng hiện có?
5. Có kỹ thuật nào trên **Canvas 2D, tất định theo `t`** cho cảm giác "đắt tiền" hơn mà không làm chậm xem trước (motion blur, bloom giả, particles tất định, chromatic aberration…)?

---

## 8. Cách giám khảo tự xem và đo

- **Xem:** mở `chess-move-studio.html` bằng Chrome, chọn **Ván mẫu → Kasparov – Topalov 1999** (có `!!` và 3 nước chiếu liên tiếp), hoặc ván Blackburne Shilling (có `!!` và fork). Bấm vào video hoặc nhấn Space để phát; kéo thanh để tua; phím ← → tua 1 giây.
- **Dựng khung hình bằng script** (Puppeteer…):
  - `await window.__ready` rồi `window.__render(t)` vẽ khung tại giây `t` lên `<canvas id="cv">`.
  - Biến toàn cục `clip` chứa timeline: `clip.plies[i].start / moveStart / arrive / end`, `clip.plies[i].lane`, `clip.from`, `clip.to`.
- **Tên hàm đáng đọc:** `layout`, `camera`, `renderBoard`, `drawCard`, `drawImpact`, `drawLane`, `laneHop`, `drawFork`, `spinPose`, `fullView`, `pickLanes`, `attackedSquares`, `lineBetween`, `lanePath`.
