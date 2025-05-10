[**English**](README.md) | [**Tiếng Việt**](README_VI.md)
[[IJCAI 2025 Accepted Paper Preprint]](assets/v7_preprint.pdf)
# `v7` Input Method

This project aims to analyze the Vietnamese language to develop a faster typing method by implementing word prediction based on partial input. For instance, inputting only `x0ch2` should yield `xin chào` as the predicted output.

*Completeness:* `v7` is basically better VNI, everything VNI can do, `v7` also can do. So you can input any possible Vietnamese words with `v7`.

Use the below script to try `v7` method!

[![Introduction to v7: Toward a Faster Vietnamese Typing Toolkit](https://img.youtube.com/vi/8oCy65ZKvzc/maxresdefault.jpg)](https://www.youtube.com/watch?v=8oCy65ZKvzc)

<!-- ![Demo](assets/v7ai.gif) -->

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
  - `6` for `entering/checked` acute: `cấp`, `tiếc`, `tất`, `thích`... (everything with acute and ends with `p`, `t`, `c`, `ch` must be tone `6`)
  - `7` for `entering/checked` underdot: `nhập`, `phục`, `đột`, `mạch`... (everything with underdot and ends with `p`, `t`, `c`, `ch` must be tone `7`)
  
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
 7: 703205} 
 
 # 1590000/12169131 rows on VTSNLP/vietnamese_curated_dataset
 {0: 327807887,
 1: 181193062,
 2: 230149590,
 3: 130067773,
 4: 59128896,
 5: 134059571,
 6: 109569975,
 7: 87877665}

 
 -->

**Note:** *If you aren't familiar with 8-tone system, you can still config to use traditional VNI 6-tone. But using 8-tone system is highly recommended for much much better AI result!* 

### Platform Support

**Operating Systems**:
- ✅ **macOS** - Please switch to English keyboard
- ✅ **Windows** - Please switch to English keyboard
- ⛔ **Linux** – Not supported *yet*

**Current Limitations**:
- 🚫 **CapsLock**: Not currently supported. Please make sure CapsLock is off when typing.
- ⚠️ **Accessibility**: Some platforms (e.g., macOS) may require enabling accessibility permissions such as input monitoring for the tool to function correctly.
- Stable version in progress...

### Modes

`v7` predicts the words/phrases users want to type by checking and ranking possible words/phrases. 

#### AI Mode
This mode utilize `v7gpt`: a GPT-like model with a custom tokenizer only for `v7`, trained on a Vietnamese corpus, based on Andrej Karpathy's [nanoGPT](https://github.com/karpathy/build-nanogpt).

- **Advantages**:
  - Works in any circumstances.
  - Understands the context in which the user is writing to predict the most suitable next word.
  - Can effectively predict entire sentences at a time.
  
## Run the App
<!-- TODO: (Warn user about the computer accessibility issues) -->
This project uses Python 3.12. 

#### Using AI Mode
To run the app in AI Mode, follow these steps:

1. Install the required packages for AI Mode (Torch is required):
    ```bash
    pip install -r requirements_ai.txt
    ```
2. Download the pretrained model checkpoint:
    ```bash
    gdown 1dDP0jIJ79syE6vt6QnVl05_4fYpuwrqd -O checkpoints/v7gpt-1.3.pth
    # Or download the file at https://drive.google.com/file/d/12ZBG5IBOKmgmv7mh32uFdDUqr-K0SzPS/view?usp=drive_link to checkpoints/v7gpt-1.3.pth
    ```
3. Start the application:
    ```bash
    python main.py
    ```
