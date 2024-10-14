[**English**](README.md) | [**Tiếng Việt**](README_VI.md)

# `v7` Input Method

This project aims to analyze the Vietnamese language to develop a faster typing method by implementing word prediction based on partial input. For instance, inputting only `x0ch2` should yield `xin chào` as the predicted output.

*Completeness:* `v7` is basically better VNI, everything VNI can do, `v7` also can do. So you can input any possible Vietnamese words with `v7`.

Use the below script to try `v7` method!

![Demo](assets/v7ai.gif)

## Motivation

- The Vietnamese language consists of many diacritics, making typing in Vietnamese time-consuming due to the need for these diacritical marks.
- `v7` aims to simplify Vietnamese typing by using only the initial consonant and tone to predict the intended words. For example, instead of typing `tưởng tượng` as `tuong73 tuong75` (`VNI`) or `tuongwr tuongwj` (`Telex`), you can type `t3t5` with `v7`!
- Naturally, this reduction in key usage leads to some information loss. For instance, the input `t3t5` could also correspond to `tiểu tiện`, as `3` represents the hook tone `hỏi` and `5` represents the underdot tone `nặng`.
- This project analyzes and addresses these problems to ultimately introduce `v7`, enhancing the Vietnamese typing experience.

## Overview

### Input Style

`v7` inherits both from former VNI and Telex.

- **Special consonants**:
  - `g` for both `g` and `gh`.
  - `ng` for both `ng` and `ngh`.
  - `z` for `gi`. (`z6` → `giúp`, `giết`, `giáp`, ...)
  - `dd` for `đ`. (`dd4` → `đã`, `đãi`, `đỗ`, ...) (`Telex style`)

- **Tones** (`VNI style`):
  - `0` for no tones: `tuân`, `câm`, `tân`...
  - `1` for normal acute: `cấm`, `tiếng`, `tấn`, `thính`... (compare with `6` to see the differences)
  - `2` for grave: `tuần`, `cầm`, `tần`...
  - `3` for hook: `tẩn`, `cẩm`, `hỉ`...
  - `4` for tilde: `mãi`, `rã`, `phũ`...
  - `5` for normal underdot: `nhậm`, `phụng`, `độn`, `mạnh`... (compare with `7` to see the differences)
  - `6` for `entering` acute: `cấp`, `tiếc`, `tất`, `thích`... (everything with acute and ends with `p`, `t`, `c`, `ch` must be tone `6`)
  - `7` for `entering` underdot: `nhập`, `phục`, `đột`, `mạch`... (everything with underdot and ends with `p`, `t`, `c`, `ch` must be tone `7`)
  
- **Special vowels**:
  - Lots of `ă`, `â`, `ê`, `ô`, `ơ`, `ư` when typing Vietnamese? Not a problem anymore because just typing `a`, `e`, `o`, `u` and `v7` will predict the most suitable ones for you! This feature also helps reducing number of keys you have to type!

This 8-tone system follows the [Vietnamese Eight-Tone Analysis](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis).

<!-- {0: 1811243,
 1: 1177092,
 2: 1486109,
 3: 987875,
 4: 353059,
 5: 972686,
 6: 815346,
 7: 703205} -->

**Note:** *If you aren't familiar with 8-tone system, you can still config to use traditional VNI 6-tone. But using 8-tone system is highly recommended for much much better AI result!* 

### Modes

`v7` predicts the words/phrases users want to type by checking and ranking possible words/phrases. It operates in two modes:

#### Dictionary Mode
In this mode, `v7` searches for matching phrases in the dictionary and ranks them based on trained usage frequency.

- **Limitations**:
  - Can only detect phrases present in the dictionary (although users can add more phrases to the dictionary).
  - No understanding of the context.
  - Effective for predicting single words or one phrase in the dictionary at a time.

![Demo](assets/v7dict.gif)

#### AI Mode
This mode utilize `v7gpt`: a GPT-like model with a custom tokenizer only for `v7`, trained on a Vietnamese corpus, based on Andrej Karpathy's [nanoGPT](https://github.com/karpathy/build-nanogpt).

- **Advantages**:
  - Works in any circumstances.
  - Understands the context in which the user is writing to predict the most suitable next word.
  - Can effectively predict entire sentences at a time.

Future plans include combining both modes to create the most robust Vietnamese input method.

![Demo](assets/v7ai.gif)

## Run the App

This project uses Python 3.12. 

#### Using Dictionary Mode
To run the app in Dictionary Mode, follow these steps:

1. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Start the application:
    ```bash
    python main.py --lang en --ai false
    # VNI 6-tone is not yet supported for Dictionary mode
    ```

#### Using AI Mode
To run the app in AI Mode, follow these steps:

1. Install the required packages for AI Mode (Torch is required):
    ```bash
    pip install -r requirements_ai.txt
    ```
2. Download the pretrained model checkpoint:
    ```bash
    gdown 1dDP0jIJ79syE6vt6QnVl05_4fYpuwrqd -O checkpoints/v7gpt.pth
    ```
3. Start the application:
    ```bash
    python main.py --lang en --ai true --vni_tones false 
    # use [--vni_tones true] if you want VNI 6-tone
    ```

<!-- ## Details -->


# Further Reading: Optimization Analysis

**Comparison of Keystrokes Required for Vietnamese Phrase Input: Traditional Methods(`Telex` or `VNI`) vs. `v7` Method.**

Phrases are categorized based on the number of words inside. 

*Note: The statistics provided are derived under optimal conditions, assuming the user inputs only consonants and tones, and the target phrase is both in the dictionary and appear in the top 9 predictions.*

| Phrase length | Number of phrases | Keystrokes reduced<br>(± 1 std) | Speed improvement<br>(± 1 std)|
|-|-|-|-|
| 1 | 6170 | 0.42 ± 1.12 | 3.1% ± 28.5%*  |
| 2 | 51614 | 4.74 ± 1.64 | 44.3% ± 9.9% |
| 3 | 6236 | 7.93 ± 2.09 | 49.0% ± 7.4% |
| 4+ <br>(not in dictionary) | 9589 | 8.79 ± 2.42 | 37.5% ± 5.1% |

The statistics show that v7 demonstrates significant improvements in performance when typing phrases with multiple words from the dictionary, greatly reducing keystrokes and boosting typing speed. This makes it effective since in Vietnamese communication phrases are often used rather than isolated words.

*\*: When typing single words, users are required to input the entire word and tone, sometimes lead to a slight increase in keystrokes compared to traditional methods(this is the only main drawback to traditional method since if user wants to type `anh` in v7, they must type `anh0` anh type one more number to choose from the prediction list).*
<!-- Configuration:
```python
class InputMethod():
    def __init__(self, strict_k=False, flexible_k=True):
        self.strict_k = strict_k     # Do not accept `c`, `q`, if you want the words start with them, use `k` instead.
        self.flexible_k = flexible_k # Only works is strict_k is False: flexible_k helps `q`, `c`, and `k` yields the same predicted words of `k` family.
``` -->

## Sandbox Usage Example:
### Analyzing
In the context of the Vietnamese language, analyzing involves the mapping of a Vietnamese word to a tuple of `(consonant_family, rhyme_family, tone)`. This process is essential for various language processing tasks. It's important to note that the analysis is **non-injective**, meaning that multiple Vietnamese words may map to the same tuple. For instance, both (`cuốc`, `quốc`) or (`mi`, `my`)  can be mapped to the same tuple.

For further details on consonant families, rhyme families, and tones, refer to the `vietnamese.py` file.

Use `Vietnamese.analyze(word: str)` for this process.
**This function is a great tool for detecting if a word is Vietnamese or not!**

```python
from vietnamese import Vietnamese

# Sample corpus for analysis
corpus = "kiểm soát phối hợp tra cứu trực tiếp trên máy tính để phát hiện phương tiện vi phạm qua hình ảnh mà đã có thông báo chưa đến nộp phạt thì tổ tra cứu sẽ thông báo"

# Analyze each word in the corpus
for word in corpus.split(' '):
    print(Vietnamese.analyze(word))
```

***Output*** **(consonant family, rhyme family, tone)**

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

The Vietnamese language actually encompasses **8 tones** [Vietnamese Eight-Tone Analysis](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis), contrary to the commonly known 6 tones. The number 6 refers to the number of diacritics used (which include none (`a`), acute (`á`), grave (`à`), hook (`ả`), tilde (`ã`), underdot (`ạ`)). Additionally, there are two extra tones in Vietnamese for syllables ending in /p/, /t/, /c/, and /ch/.

Example words for the seventh tone include: xuất, cấp, tất, chiếc, thích, mút... (with rhyme families being uân, âm, ân, iêng, inh, un respectively).

Example words for the eighth tone include: nhập, phục, đột, chục, mạch, kịp... (with rhyme families being âm, ung, ôn, ung, anh, im respectively).

**Note: This is the reason why the project name is v7: `Việt` with the 8th tone (count from index 0 is 7).**

### Synthesizing
In contrast to analyzing, synthesizing is the process of mapping a tuple of `(consonant_family, rhyme_family, tone)` to a list of words(due to the ***non-injective*** property mentioned above), it's worth noting that in most cases, the resulting list typically contains just one word.

Use `Vietnamese.synthesize(consonant: str, rhyme: str, tone: int)` or you can use `Dictionary.db[consonant][rhyme][tone]` for this process. Both methods yield the same result, but the second method is generally faster as it directly retrieves the keys. 

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

### Raw input string to Vietnamese - v7 rule

This is the process showcased in the demo GIF above. If you prefer testing via a Python script, you can use the following code.

```python
from imethod.v7 import InputMethod # Dictionary mode
# from imethod.v7ai import AIInputMethod # AI mode
inputAgent = InputMethod()

print(inputAgent.predict('xi0chao2mo5ng2'))
print(inputAgent.predict('xi0chao2mo')) # Not completed
print(inputAgent.predict('ximg0ch2')) # No match (`ximg`)
print(inputAgent.predict('xi0')) # Exact match when predict just one word and that word is provided with rhyme
print(inputAgent.predict('b7')) # Wildcard rhyme -> All possibilities in descending order of frequency (based on a large corpus)
print(inputAgent.predict('b7t2'))
print(inputAgent.predict('ba7ti2'))
print(inputAgent.predict('bac7ti2'))
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

### ...and many more in [`sandbox`](sandbox).

## References:
[Vietnamese Eight-Tone Analysis](https://en.wikipedia.org/wiki/Vietnamese_phonology#Eight-tone_analysis)


**Date Created:** 10:05 AM, Tue 27 Feb 2024

Data sources:
- Dictionary and Frequency
  - [News Corpus](https://github.com/binhvq/news-corpus)
  - [Vietnamese Dictionary 1](https://github.com/JaplinChen/rime-vietnamese-pinyin)
- Training v7gpt:
  - [Vietnamese-alpaca-gpt4-gg-translated](https://huggingface.co/datasets/5CD-AI/Vietnamese-alpaca-gpt4-gg-translated)
<!-- https://github.com/tienhapt/generalcorpus -->

<!-- Reference: -->
<!-- https://github.com/vncorenlp/VnCoreNLP -->
<!-- https://nlp.uit.edu.vn/datasets/#h.p_Uj6Wqs5dCpc4 -->
<!-- https://machinelearningmastery.com/training-the-transformer-model/ -->

<!-- https://online-video-cutter.com/change-video-speed -->
<!-- https://www.veed.io/convert/mp4-to-gif -->
<!-- 24 FPS -->