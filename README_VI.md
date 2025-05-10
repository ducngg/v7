[**English**](README.md) | [**Tiếng Việt**](README_VI.md)
[[IJCAI 2025 Accepted Paper Preprint]](assets/v7_preprint.pdf) 

# Bộ gõ Tiếng Việt `v7`

Dự án này phân tích tiếng Việt để phát triển một phương pháp gõ nhanh hơn bằng cách dự đoán từ dựa trên một phần từ muốn nhập. Ví dụ, chỉ cần nhập `x0ch2` sẽ có thể dự đoán ra `xin chào`.

*Độ toàn diện:* Nói ngắn gọn, `v7` có thể xem như là một VNI phiên bản nhanh hơn, vì vậy bạn hoàn toàn có thể nhập tất cả mọi từ tiếng Việt có thể nhập.

Chạy các lệnh ở phần dưới để sử dụng `v7`.

[![Introduction to v7: Toward a Faster Vietnamese Typing Toolkit](https://img.youtube.com/vi/8oCy65ZKvzc/maxresdefault.jpg)](https://www.youtube.com/watch?v=8oCy65ZKvzc)

<!-- ![Demo](assets/v7ai.gif) -->

## Động Lực Phát Triển
- Tiếng Việt là ngôn ngữ có nhiều dấu và thanh điệu, để nhập tất cả các dấu rất tốn thời gian.
- `v7` là giải pháp để đơn giản hóa việc nhập bằng cách chỉ sử dụng phụ âm đầu và thanh điệu để dự đoán từ muốn nhập. Ví dụ: Để có chữ `tưởng tượng` cần phải nhập `tuong73 tuong75` (`VNI`) hoặc `tuongwr tuongwj` (`Telex`), nhưng với `v7` ta chỉ cần `t3t5`!
- Nhưng tất nhiên, ta nhận ra vấn đề là `tiểu tiện` cũng thỏa `t3t5`, với `3` là dấu `hỏi` và `5` là dấu nặng `nặng`.
- Dự án này phân tích và giải quyết các vấn đề của ý tưởng trên, để phát triển thành công `v7`, một bộ gõ tối ưu trải nghiệm khi nhập.
  
## Tổng Quan

### Cách Nhập

`v7` lấy cảm hứng từ cả VNI và Telex!

- **Phụ âm đặc biệt**:
  - `g` cho cả `g` và `gh`.
  - `ng` cho cả `ng` và `ngh`.
  - `z` cho `gi`. (`z6` → `giúp`, `giết`, `giáp`, ...)
  - `dd` cho `đ`. (`dd4` → `đã`, `đãi`, `đỗ`, ...) (`giống Telex`)

- **Thanh điệu** (`giống VNI`):
  - `0` cho không dấu (thanh ["phù bình"](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)): `tuân`, `câm`, `tân`...
  - `1` cho dấu sắc (thanh ["phù khứ"](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)): `cấm`, `tiếng`, `tấn`, `thính`... (xem thanh `6` để thấy sự khác biệt)
  - `2` cho dấu huyền (thanh ["trầm bình"](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)): `tuần`, `cầm`, `tần`...
  - `3` cho dấu hỏi (thanh ["phù thượng"](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)): `tẩn`, `cẩm`, `hỉ`...
  - `4` cho dấu ngã (thanh ["trầm thượng"](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)): `mãi`, `rã`, `phũ`...
  - `5` cho dấu nặng (thanh ["trầm khứ"](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)): `nhậm`, `phụng`, `độn`, `mạnh`... (xem thanh `7` để thấy sự khác biệt)
  - `6` cho thanh ["phù nhập"](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis): `cấp`, `tiếc`, `tất`, `thích`... (các từ có dấu sắc và kết thúc bằng `p`, `c`, `t`, `ch` sẽ là thanh `6`)
  - `7` cho thanh ["trầm nhập"](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis): `nhập`, `phục`, `đột`, `mạch`... (các từ có dấu nặng và kết thúc bằng `p`, `c`, `t`, `ch` sẽ là thanh `7`)
  
- **Nguyên âm đặc biệt**:
  - Chả cần quan tâm `ă`, `â`, `ê`, `ô`, `ơ`, `ư`. Vì chỉ cần nhập `a`, `e`, `o`, `u` là `v7` có thể hiểu được và đưa ra dự đoán đúng ý nhất! Tính năng này giúp giảm đáng kể thời gian nhập.

<!-- {0: 1811243,
 1: 1177092,
 2: 1486109,
 3: 987875,
 4: 353059,
 5: 972686,
 6: 815346,
 7: 703205} -->

Thanh điệu được mở rộng so với 6 dấu của VNI. Xem [Hệ 8 thanh điệu trong tiếng Việt](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis) để hiểu rõ hơn về 8 thanh điệu.

**Lưu ý:** *Nếu không quen với hệ 8 thanh điệu, ta hoàn toàn có thể chọn dùng 6 dấu như VNI thông thường. Nhưng sử dụng hệ 8 thanh điệu sẽ có kết quả dự đoán tốt hơn rất nhiều!*

### Tương thích

**Hệ điều hành**:
- ✅ **macOS** – Chuyển sang bàn phím tiếng Anh khi dùng
- ✅ **Windows** – Chuyển sang bàn phím tiếng Anh khi dùng
- ⛔ **Linux** – Chưa được hỗ trợ

**Hạn chế hiện tại**:
- 🚫 **CapsLock**: Chưa được hỗ trợ. Vui lòng tắt CapsLock khi gõ.  
- ⚠️ **Quyền truy cập hệ thống**: Một số nền tảng (ví dụ macOS) có thể yêu cầu cấp quyền truy cập bàn phím để công cụ hoạt động chính xác.
- Đang trong quá trình phát triển phiên bản ổn định...

### Các Chế Độ

`v7` dự đoán các từ/cụm từ mà người dùng muốn gõ bằng cách kiểm tra và xếp hạng các từ/cụm từ có thể có.

#### Chế Độ AI
Chế độ này sử dụng `v7gpt` - một mô hình tựa GPT với bộ tokenizer của riêng `v7`, được huấn luyện trên kho ngữ liệu tiếng Việt, dựa trên [nanoGPT](https://github.com/karpathy/build-nanogpt) của Andrej Karpathy.

- **Ưu Điểm**:
  - Hoạt động tốt trong mọi ngữ cảnh.
  - Hiểu ngữ cảnh mà người dùng đang viết để dự đoán từ tiếp theo phù hợp nhất.
  - Có thể dự đoán hiệu quả toàn bộ câu.

## Sử dụng
<!-- TODO: (Warn user about the computer accessibility issues) -->
`v7` chạy trên Python 3.12.

#### Sử Dụng Chế Độ AI

1. Cài đặt các thư viện cần thiết cho chế độ AI (yêu cầu Torch):
    ```bash
    pip install -r requirements_ai.txt
    ```
2. Tải về mô hình đã được huấn luyện:
    ```bash
    gdown 1dDP0jIJ79syE6vt6QnVl05_4fYpuwrqd -O checkpoints/v7gpt-1.3.pth
    # Hoặc tải file model https://drive.google.com/file/d/12ZBG5IBOKmgmv7mh32uFdDUqr-K0SzPS/view?usp=drive_link về checkpoints/v7gpt-1.3.pth
    ```
3. Khởi động ứng dụng:
    ```bash
    python main.py
    ```
