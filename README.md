# Vietnamese Typing Optimization Analysis

This project aims to analyze the Vietnamese language to develop a faster typing method by implementing word prediction based on partial input. For instance, inputting 'x0ch2' should yield 'xin chào' as the predicted output.

## Current Development Status
The `app.py` has been implemented using PyQt5. To test the application, simply run `python app.py`. Make sure to install the required dependencies listed in `requirements.txt` first.
🤝 **This application will be the place for you to try out v7 method!**

![Demo](assets/demo.gif)

## Sandbox Usage Example:
### Analyzing (Phân tích)
In the context of the Vietnamese language, analyzing involves the mapping of a Vietnamese word to a tuple of `(consonant_family, rhyme_family, tone)`. This process is essential for various language processing tasks. It's important to note that the analysis is **non-injective**, meaning that multiple Vietnamese words may map to the same tuple. For instance, both (`cuốc`, `quốc`) or (`mi`, `my`)  can be mapped to the same tuple.

For further details on consonant families, rhyme families, and tones, refer to the `vietnamese.py` file.

Use `Vietnamese.analyze(word: str)` for this process.

```python
from vietnamese import Vietnamese

# Sample corpus for analysis
corpus = "kiểm soát phối hợp tra cứu trực tiếp trên máy tính để phát hiện phương tiện vi phạm qua hình ảnh mà đã có thông báo chưa đến nộp phạt thì tổ tra cứu sẽ thông báo"

# Analyze each word in the corpus
for word in corpus.split(' '):
    print(Vietnamese.analyze(word))
```

***Output*** **(consonant family: âm, rhyme family: vần, tone: thanh)**

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

***Explanation***
The Vietnamese language actually encompasses **8 tones**, contrary to the commonly known 6 tones. The number 6 refers to the number of diacritics used (which include none (`a`), acute (`á`), grave (`à`), hook (`ả`), tilde (`ã`), underdot (`ạ`)). Additionally, there are two extra tones in Vietnamese for syllables ending in /p/, /t/, /c/, and /ch/.

Example words for the seventh tone include: xuất, cấp, tất, chiếc, thích, mút... (with rhyme families being uân, âm, ân, iêng, inh, un respectively)

Example words for the eighth tone include: nhập, phục, đột, chục, mạch, kịp... (with rhyme families being âm, ung, ôn, ung, anh, im respectively)

**Note: This is the reason why the project name is v7: `Việt` with the 8th tone (count from index 0 is 7)**

### Synthesizing (Kết hợp)
In contrast to analyzing, synthesizing is the process of mapping a tuple of `(consonant_family, rhyme_family, tone)` to a list of words(due to the ***non-injective*** property mentioned above), it's worth noting that in most cases, the resulting list typically contains just one word.

Use `Vietnamese.synthesize(consonant: str, rhyme: str, tone: int)` or you can use `Dictionary.db[consonant][rhyme][tone]` for this process. Both methods yield the same result, but the second method is generally faster as it directly retrieves the keys. 

```python
from vietnamese import Vietnamese
from dictionary import Dictionary

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
(Uncomment the last 2 lines to see the differences between different `consonants` go with `i`)
***Output*** 
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

### Raw input string to Vietnamese - v7 rule (Nhập)

This is the process showcased in the demo GIF above. If you prefer testing via a Python script, you can use the following code.

```python
from inputmethod import InputMethod
inputAgent = InputMethod()

print(inputAgent.predict('xi0chao2mo5ng2'))
print(inputAgent.predict('xi0chao2mo')) # Not completed
print(inputAgent.predict('ximg0ch2')) # No match (`ximg`)
print(inputAgent.predict('xi0')) # Exact match when predict just one word and that word is provided with rhyme
print(inputAgent.predict('b7')) # Wildcard rhyme -> All possibilities in descending order of frequency (based on a large corpus)
print(inputAgent.predict('b7t2'))
print(inputAgent.predict('ba7ti2'))
print(inputAgent.predict('bang7ti2')) # If you want words end with /p/, /t/, /c/, and /ch/; use  /m/, /n/, /ng/, and /nh/ respectively.
```
***Output*** 
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

### ...and many more in `sandbox.py`.

## Further Reading:
[Vietnamese Eight-Tone Analysis](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)


**Date Created:** 10:05 AM, Tue 27 Feb 2024

Data sources:
- [News Corpus](https://github.com/binhvq/news-corpus)
- [Vietnamese Dictionary 1](https://github.com/JaplinChen/rime-vietnamese-pinyin)
