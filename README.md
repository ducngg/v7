# Vietnamese Typing Optimization Analysis

This project aims to analyze the Vietnamese language to develop a faster typing method by implementing word prediction based on partial input. For instance, inputting 'x ch' or 'x0 ch2' should yield 'xin chào' as the predicted output.

## Current Development Status
The project is currently in the development phase.

### Usage Example:
```python
from vietnamese import Vietnamese

# Sample corpus for analysis
corpus = "kiểm soát phối hợp tra cứu trực tiếp trên máy tính để phát hiện phương tiện vi phạm qua hình ảnh mà đã có thông báo chưa đến nộp phạt thì tổ tra cứu sẽ thông báo"

# Analyze each word in the corpus
for word in corpus.split(' '):
    # CRT is short for Consonant, Rhyme family, and Tone
    print(Vietnamese.CRT(word))
```

### Output:
**(consonant: âm, rhyme family: vần, tone: thanh)**

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

### Explanation:
The Vietnamese language actually encompasses **8 tones**, contrary to the commonly known 6 tones. The number 6 refers to the number of diacritics used (which include none (`a`), acute (`á`), grave (`à`), hook (`ả`), tilde (`ã`), underdot (`ạ`)). Additionally, there are two extra tones in Vietnamese for syllables ending in /p/, /t/, /c/, and /ch/.

Example words for the seventh tone include: xuất, cấp, tất, chiếc, thích, mút... (with rhyme families being uân, âm, ân, iêng, inh, un respectively)

Example words for the eighth tone include: nhập, phục, đột, chục, mạch, kịp... (with rhyme families being âm, ung, ôn, ung, anh, im respectively)

### Further Reading:
[Vietnamese Eight-Tone Analysis](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)

**Date Created:** 10:05 AM, Tue 27 Feb 2024
