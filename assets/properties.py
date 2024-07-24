from typing import Literal

class Assets:
    _title = {
        'en': "v7 Typing Method",
        'vi': "Bộ gõ v7"
    }
    _help = {
        'en': "Help",
        'vi': "Trợ giúp"
    }
    _welcome = {
        'en': "Welcome to v7 - an innovative input method for typing Vietnamese!",
        'vi': "Chào mừng đến với v7 - bộ gõ tối ưu tốc độ cho Tiếng Việt!"
    }
    _pred_label = {
        'en': "Predictions",
        'vi': "Dự đoán"
    }
    _usage = {
        'en': "Usage: Press key [①-⑨] ← → ⌫ ⏎ ",
        'vi': "Sử dụng: Dùng phím [①-⑨] ← → ⌫ ⏎ "
    }
    _copy = {
        'en': "Copy",
        'vi': "Sao chép"
    }
    _clear = {
        'en': "Clear",
        'vi': "Xóa"
    }
    _add_phrase_button = {
        'en': "Add your own common phrase",
        'vi': "Thêm cụm từ"
    }
    _instruction = {
        'en': """
- Please turn off Unikey or other keyboard input tools when using this app to avoid conflicts.
- Please provide rhymes for better prediction on uncommon words (to input `tí tách`, use `ti1t6` instead of `t1t6`).
- Similar with long phrase, don't type `ng0l2ng0ng4`, instead type something like `nguy0li1ngon0ngu4` for `nguyên lý ngôn ngữ`.
- Press `Enter` to append raw input to the text area at the bottom.

Special consonants:
- `g` for both `g` and `gh`.
- `ng` for both `ng` and `ngh`.
- `z` for `gi`. (z6  → giúp, giết, giáp, ...)
- `dd` for `đ`. (dd4 → đã, đãi, đỗ, ...)
Tones:
- 0 for no tones
- [1-5] for tones from 1 to 5 (VNI style)
- 6 for `entering` accute: xuất, cấp, tất, chiếc, thích, mút... 
- 7 for `entering` underdot: nhập, phục, đột, chục, mạch, kịp...
""",
        'vi': """
- Tắt VNI / Telex trước khi dùng.
- Hãy nhập thêm vần cho các từ không thông dụng để được dự đoán tốt hơn (để nhập `tí tách`, nên dùng `ti1t6` thay cho `t1t6`).
- Tương tự với những cụm dài, thay vì `ng0l2ng0ng4`, hãy nhập `nguy0li1ngon0ngu4` cho cụm `nguyên lý ngôn ngữ`.
- Bấm `Enter` để nhập thô.

Phụ âm đặc biệt:
- `g` cho cả `g` và `gh`.
- `ng` cho cả both `ng` và `ngh`.
- `z` cho `gi`. (z6  → giúp, giết, giáp, ...)
- `dd` cho `đ`. (dd4 → đã, đãi, đỗ, ...)
Thanh điệu:
- 0 cho không dấu (thanh ngang)
- [1-5] cho thanh 1 đến 5 (tương tự như VNI)
- 6 cho thanh sắc `nhập` (thanh phù nhập): xuất, cấp, tất, chiếc, thích, mút... 
- 7 cho thanh nặng `nhập` (thanh trầm nhập): nhập, phục, đột, chục, mạch, kịp...
"""
    }
    _page = {
        'en': "Showing",
        'vi': "Trang"
    }
    _percent_keys = {
        'en': "%Keys reduced",
        'vi': "%Phím đã giảm"
    }
    _update_dictionary_title = {
        'en': "Update dictionary",
        'vi': "Cập nhật từ điển"
    }
    _change_log = {
        'en': "Change log",
        'vi': "Thay đổi"
    }
    _invalid = {
        'en': "Invalid",
        'vi': "Không hợp lệ"
    }
    _added = {
        'en': "Added",
        'vi': "Thêm"
    }
    _removed = {
        'en': "Removed",
        'vi': "Xóa"
    }
    
    def __init__(self, lang: Literal['en', 'vi']):
        self.lang = lang
            
    @property
    def title(self):
        return Assets._title[self.lang]
    @property
    def help(self):
        return Assets._help[self.lang]
    @property
    def welcome(self):
        return Assets._welcome[self.lang]
    @property
    def pred_label(self):
        return Assets._pred_label[self.lang]
    @property
    def usage(self):
        return Assets._usage[self.lang]
    @property
    def copy(self):
        return Assets._copy[self.lang]
    @property
    def clear(self):
        return Assets._clear[self.lang]
    @property
    def add_phrase_button(self):
        return Assets._add_phrase_button[self.lang]
    @property
    def instruction(self):
        return Assets._instruction[self.lang]
    @property
    def page(self):
        return Assets._page[self.lang]
    @property
    def percent_keys(self):
        return Assets._percent_keys[self.lang]
    @property
    def update_dictionary_title(self):
        return Assets._update_dictionary_title[self.lang]
    @property
    def change_log(self):
        return Assets._change_log[self.lang]
    @property
    def invalid(self):
        return Assets._invalid[self.lang]
    @property
    def added(self):
        return Assets._added[self.lang]
    @property
    def removed(self):
        return Assets._removed[self.lang]
    
    