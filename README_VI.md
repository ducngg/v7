[**English**](README.md) | [**Tiếng Việt**](README_VI.md)

# Bộ gõ Tiếng Việt `v7`

Dự án này phân tích tiếng Việt để phát triển một phương pháp gõ nhanh hơn bằng cách dự đoán từ dựa trên một phần từ muốn nhập. Ví dụ, chỉ cần nhập `x0ch2` sẽ có thể dự đoán ra `xin chào`.

*Độ toàn diện:* Nói ngắn gọn, `v7` có thể xem như là một VNI phiên bản nhanh hơn, vì vậy bạn hoàn toàn có thể nhập tất cả mọi từ tiếng Việt có thể nhập.

Hiện tại, bạn có thể sử dụng các lệnh ở phần dưới để mở ứng dụng để sử dụng `v7`, trong tương lai sẽ tích hợp trực tiếp lên bàn phím để có thể sử dụng trực tiếp không cần qua app.

![Demo](assets/v7ai.gif)

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

### Các Chế Độ

`v7` dự đoán các từ/cụm từ mà người dùng muốn gõ bằng cách kiểm tra và xếp hạng các từ/cụm từ có thể có. Nó hoạt động ở hai chế độ:

#### Chế Độ Từ Điển
Trong chế độ này, `v7` tìm kiếm các cụm từ phù hợp trong từ điển và xếp hạng chúng dựa trên tần suất sử dụng đã được huấn luyện.

- **Hạn Chế**:
  - Chỉ có thể phát hiện các cụm từ có trong từ điển (người dùng có thể thêm nhiều cụm từ hơn vào từ điển).
  - Không có khả năng hiểu ngữ cảnh.
  - Chỉ hiệu quả trong việc dự đoán các từ đơn hoặc một cụm từ có trong từ điển.

![Demo](assets/v7dict.gif)

#### Chế Độ AI
Chế độ này sử dụng `v7gpt` - một mô hình tựa GPT với bộ tokenizer của riêng `v7`, được huấn luyện trên kho ngữ liệu tiếng Việt, dựa trên [nanoGPT](https://github.com/karpathy/build-nanogpt) của Andrej Karpathy.

- **Ưu Điểm**:
  - Hoạt động tốt trong mọi ngữ cảnh.
  - Hiểu ngữ cảnh mà người dùng đang viết để dự đoán từ tiếp theo phù hợp nhất.
  - Có thể dự đoán hiệu quả toàn bộ câu.

Trong tương lai sẽ kết hợp cả hai chế độ để tạo ra phương pháp nhập tiếng Việt ưu việt nhất.

![Demo](assets/v7ai.gif)

## Sử dụng

`v7` chạy trên Python 3.12.

#### Sử Dụng Chế Độ Từ Điển

1. Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```
2. Khởi động ứng dụng:
    ```bash
    python main.py --lang vi --ai false
    # hiện tại chưa hỗ trợ hệ 6 dấu VNI thông thường cho chế độ này
    ```

#### Sử Dụng Chế Độ AI

1. Cài đặt các thư viện cần thiết cho chế độ AI (yêu cầu Torch):
    ```bash
    pip install -r requirements_ai.txt
    ```
2. Tải về mô hình đã được huấn luyện:
    ```bash
    gdown 1dDP0jIJ79syE6vt6QnVl05_4fYpuwrqd -O checkpoints/v7gpt.pth
    ```
3. Khởi động ứng dụng:
    ```bash
    python main.py --lang vi --ai true --vni_tones false 
    # hãy chọn [--vni_tones true] nếu muốn dùng hệ 6 dấu của VNI
    ```

<!-- ## Details -->

# Xem Thêm: Phân tích sự tối ưu của `v7`

**Bảng so sánh số lượng phím cần bấm để nhập một từ, cụm từ cho `Telex`/`VNI` và `v7`.**

Bảng thống kê này nhóm các cụm từ theo độ dài cụm từ. 

*Lưu ý: Số liệu được đánh giá qua trường hợp tốt nhất khi nhập bằng `v7`, giả sử rằng người dùng chỉ nhập `nguyên âm đầu` (hay còn gọi là **`âm`**) và `thanh điệu` (hay còn gọi là **`thanh`**) tương ứng, và cụm từ người dùng muốn nhập nằm trong từ điển và thuộc 9 cụm từ đoán được đầu tiên.*

| Độ dài cụm từ | Số lượng cụm từ | Số phím giảm<br>(so với VNI/Telex)<br>(± 1 std) | Tốc độ tăng<br>(so với VNI/Telex)<br>(± 1 std)|
|-|-|-|-|
| 1 | 6170 | 0.42 ± 1.12 | 3.1% ± 28.5%*  |
| 2 | 51614 | 4.74 ± 1.64 | 44.3% ± 9.9% |
| 3 | 6236 | 7.93 ± 2.09 | 49.0% ± 7.4% |
| 4+ <br>(không có trong từ điển) | 9589 | 8.79 ± 2.42 | 37.5% ± 5.1% |

So sánh cho thấy v7 có thể giảm mạnh số lượng phím và thời gian nhập khi người dùng cần nhập cụm từ trong từ điển, điều này giúp việc nhập tiếng Việt trở nên nhanh hơn vì ta thường dùng các cụm từ trong sinh hoạt, giao tiếp.

*\*: Khi nhập từ đơn, người dùng phải nhập toàn bộ chữ cái của từ, thêm vào đó là số `thanh`, đôi khi dẫn đến việc phải nhập nhiều hơn so với VNI/Telex (đây là điểm yếu chính của `v7`). Ví dụ: Để nhập `anh` bằng v7, người dùng phải nhập `anh0` và cần bấm thêm 1 số nữa để chọn trong số những dự đoán.*

<!-- Configuration:
```python
class InputMethod():
    def __init__(self, strict_k=False, flexible_k=True):
        self.strict_k = strict_k     # Do not accept `c`, `q`, if you want the words start with them, use `k` instead.
        self.flexible_k = flexible_k # Only works is strict_k is False: flexible_k helps `q`, `c`, and `k` yields the same predicted words of `k` family.
``` -->

## Sử dụng thư viện:
### Phân tách
Phân tách một từ tiếng Việt là quá trình chuyển 1 từ thành một bộ ba (tuple) `(họ_âm, họ_vần, thanh)`**. Quá trình này là nền móng cho việc phát triển bộ gõ `v7`. Đây là một hàm **không đơn ánh**, có thể có vài từ được phân tách ra cùng một bộ ba. Ví dụ: `cuốc` và `quốc` đều được phân tách ra là `('k', 'uông', 6)`; `mi` và `my` đều được phân tách ra là `('m', 'i', 0)`.

**: Chi tiết hơn về `họ_âm` (tượng trưng cho những phụ âm đầu giống nhau); `họ_vần` (tượng trưng cho những vần giống nhau); `thanh` có thể được tìm thấy trong file `vietnamese.py`.

Sử dụng `Vietnamese.analyze(word: str)` cho quá trình này.
**Hàm này có thể được dùng để kiểm tra xem một từ có phải thuộc tiếng Việt hay không!**

```python
from vietnamese import Vietnamese

# Đoạn văn mẫu
corpus = "kiểm soát phối hợp tra cứu trực tiếp trên máy tính để phát hiện phương tiện vi phạm qua hình ảnh mà đã có thông báo chưa đến nộp phạt thì tổ tra cứu sẽ thông báo"

# Phân tách từng từ
for word in corpus.split(' '):
    print(Vietnamese.analyze(word))
```

***Kết quả*** **(họ_âm, họ_vần, thanh)**

```
('k', 'iêm', 3)
('s', 'oan', 6)
('ph', 'ôi', 1)
('h', 'ơm', 7)
('tr', 'a', 0)
('k', 'ưu', 1)
('tr', 'ưng', 7)
('t', 'iêm', 6)
('tr', 'ên', 0)
('m', 'ay', 1)
('t', 'inh', 1)
('đ', 'ê', 3)
('ph', 'an', 6)
('h', 'iên', 5)
('ph', 'ương', 0)
('t', 'iên', 5)
('v', 'i', 0)
('ph', 'am', 5)
('k', 'oa', 0)
('h', 'inh', 2)
('0', 'anh', 3)
('m', 'a', 2)
('đ', 'a', 4)
('k', 'o', 1)
('th', 'ông', 0)
('b', 'ao', 1)
('ch', 'ưa', 0)
('đ', 'ên', 1)
('n', 'ôm', 7)
('ph', 'an', 7)
('th', 'i', 2)
('t', 'ô', 3)
('tr', 'a', 0)
('k', 'ưu', 1)
('s', 'e', 4)
('th', 'ông', 0)
('b', 'ao', 1)
```

***Giải thích***

Tiếng Việt trên thực tế có **8 thanh điệu** [Hệ 8 thanh điệu trong tiếng Việt](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis), không phải 6 thanh điệu như nhiều người thường nghĩ. 6 ở đây thật ra là số lượng `dấu` (ngang/không dấu (`a`), sắc (`á`), huyền (`à`), hỏi (`ả`), ngã (`ã`), nặng (`ạ`)). Với những từ kết thúc bằng /p/, /t/, /c/, and /ch/, ta có thêm 2 `thanh` nữa!

Những từ với `thanh 7`: xuất, cấp, tất, chiếc, thích, mút... (họ vần theo thứ tự là: uân, âm, ân, iêng, inh, un).

Những từ với `thanh 8`: nhập, phục, đột, chục, mạch, kịp... (họ vần theo thứ tự là: âm, ung, ôn, ung, anh, im).

**Đây là khởi nguồn cho tên dự án v7: là từ `Việt` với thanh thứ 8 (nếu đếm từ 0 thì sẽ là 7).**

### Hợp nhất
Ngược lại với Phân tách, Hợp nhất là quá trình từ một bộ ba `(họ_âm, họ_vần, thanh)` ra một **dãy** (thay vì một từ vì tính chất ***không đơn ánh*** của Phân tách) nhưng thật ra trong đa số trường hợp, Hợp nhất sẽ cho một dãy chỉ có 1 phần tử.

Sử dụng `Vietnamese.synthesize(consonant: str, rhyme: str, tone: int)` hoặc `Dictionary.db[consonant][rhyme][tone]` cho quá trình này. Cả hai đều cho kết quả giống nhau nhưng cách thứ hai sẽ nhanh hơn vì nó truy xuất trực tiếp trên các khóa của Python Dictionary.

```python
from utils.vietnamese import Vietnamese
from utils.dictionary import Dictionary

print(Vietnamese.synthesize('k', 'u', 4))
print(Vietnamese.synthesize('k', 'uông', 6))
print(Vietnamese.synthesize('0', 'iên', 1))
print(Vietnamese.synthesize('0', 'i', 1))
print(Vietnamese.synthesize('z', 'i', 2))
print(Vietnamese.synthesize('ng', 'iêm', 7))
print(Vietnamese.synthesize('ng', 'iêm', 5))
print(Dictionary.db['z']['iên'][6])
print(Dictionary.db['d']['iên'][7])
print(Dictionary.db['k']['oeo'][5])
print(Dictionary.db['k']['oang'][0])
print(Dictionary.db['g']['i'][2])
print(Dictionary.db['z']['ăng'][7])
print(Dictionary.db['g']['i'][2])
print(Dictionary.db['kh']['ung'][3])
print(Dictionary.db['ng']['ênh'][2])
print(Dictionary.db['h']['oang'][3])
print(Dictionary.db['x']['uân'][6])
print(Dictionary.db['kh']['uênh'][2])
print(Dictionary.db['kh']['uênh'][7])
print(Dictionary.db['kh']['uênh'][6])
print(Dictionary.db['k']['oai'][1])
print(Dictionary.db['k']['ưu'][3])
# for c in Vietnamese.consonant_families:
#     print(Dictionary.db[c]['i'][0])
```
(Bỏ comment 2 dòng cuối để xem cách các `họ_âm` khác nhau ghép với `họ_vần` **`'i'`**)

***Kết quả*** 
```['cũ']
['cuốc', 'quốc']
['yến']
['í', 'ý']
['gì']
['nghiệp']
['nghiệm']
['giết']
['diệt']
['quẹo']
['quang']
['ghì']
['giặc']
['ghì']
['khủng']
['nghềnh']
['hoảng']
['xuất']
['khuềnh']
['khuệch']
['khuếch']
['quái']
['cửu']
```

### Nhập tiếng Việt bằng phương thức v7

Quá trình này tương tự với GIF ở trên. Có thể sử dụng code như dưới đây nếu muốn dùng trực tiếp bằng Python thay vì nhập trên app.

```python
from imethod.v7 import InputMethod # Chế độ Từ Điển
# from imethod.v7ai import AIInputMethod # Chế độ AI
inputAgent = InputMethod()

print(inputAgent.predict('xi0chao2mo5ng2'))
print(inputAgent.predict('xi0chao2mo')) # Chưa đầy đủ
print(inputAgent.predict('ximg0ch2')) # Không khớp với từ nào (`ximg`)
print(inputAgent.predict('xi0')) # Khi nhập chỉ 1 từ và có sử dụng vần (ở đây dùng vần `i`), v7 sẽ dự đoán từ chính xác là `xi` (không dự đoán `xin`/`xinh`/...)
print(inputAgent.predict('b7')) # Không nhập vần -> Vần bất kỳ -> Kết quả là một dãy các từ bắt đầu bằng `b` và có thanh 7, giảm dần theo tần số sử dụng (dựa trên tập dữ liệu lớn)
print(inputAgent.predict('b7t2'))
print(inputAgent.predict('ba7ti2'))
print(inputAgent.predict('bac7ti2'))
```
***Kết quả*** 
```
['xin chào mộ người', 'xin chào mộ ngày', 'xin chào mọi người', 'xin chào mọi ngày', 'xinh chào mộ người', 'xinh chào mộ ngày', 'xinh chào mọi người', 'xinh chào mọi ngày']
None
None
['xi']
['biệt', 'bạc', 'bật', 'buộc', 'bạch', 'bậc', 'bột', 'bẹp', 'bọc', 'bịt', 'bọt', 'bạt', 'bực', 'bộc', 'bịp', 'bục', 'bịch', 'bệt', 'bụt', 'bặt', 'bập', 'bụp', 'bệch', 'buột', 'bẹc']
['biệt tài', 'bạc tình', 'bật tường', 'bạch tiền']
['bạc tình', 'bạch tiền']
['bạc tình']
```

### ...có thể tìm hiểu nhiều cách sử dụng hơn tại [`sandbox`](sandbox).

## Tham khảo:
[Hệ 8 thanh điệu trong tiếng Việt](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)


**Ngày tạo:** 10:05 Sáng, Thứ 3, 27 tháng 2 năm 2024

Nguồn dữ liệu:
- Từ điển và tần số suất hiện chữ:
  - [Tập dữ liệu báo chí](https://github.com/binhvq/news-corpus)
  - [Từ điển tiếng Việt 1](https://github.com/JaplinChen/rime-vietnamese-pinyin)
- Huấn luyện mô hình v7gpt:
  - [Vietnamese-alpaca-gpt4-gg-translated](https://huggingface.co/datasets/5CD-AI/Vietnamese-alpaca-gpt4-gg-translated)
<!-- https://github.com/tienhapt/generalcorpus -->

<!-- Reference: -->
<!-- https://github.com/vncorenlp/VnCoreNLP -->
<!-- https://nlp.uit.edu.vn/datasets/#h.p_Uj6Wqs5dCpc4 -->
