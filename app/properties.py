from typing import Literal
# TODO: check os type for [⌘①-⌘⑨]

GOLDEN_RATIO = 1.618
class Assets:
    _background_color = "qlineargradient(x1: 0, x2: 1, stop: 0 #122918, stop: 1 #123d2c)"
    _color = "#FFF"
    _logo_path = "assets/v7ai.1.png"
    
    _geometry = {
        's': (200, 100, int(260*GOLDEN_RATIO), 260),
        'l': (200, 100, int(500*GOLDEN_RATIO), 500)
    }
    _logo_height = {
        's': 15,
        'l': 30
    }
    _app_font_size = {
        's': 10,
        'l': 14
    }
    _help_button_width = {
        's': 50,
        'l': 50
    }
    _input_box_font_size = {
        's': 10,
        'l': 20
    }
    _predict_box_font_size = {
        's': 10,
        'l': 20
    }
    _predict_box_height = {
        's': 120,
        'l': 230
    }
    _result_box_font_size = {
        's': 10,
        'l': 20
    }
    _result_box_height = {
        's': 60,
        'l': 120
    }
    
    
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
        'en': "Usage: Press key [①-⑨] [⌘①-⌘⑨] ← → ⌫ ⏎ ",
        'vi': "Sử dụng: Dùng phím [①-⑨] [⌘①-⌘⑨] ← → ⌫ ⏎ "
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
    
    def __init__(
        self, 
        lang: Literal['en', 'vi'],
        size: str,
    ):
        self.lang = lang
        self.size = size
    
    @property
    def app_styleSheet(self):
        return (
            "QWidget {"
                f"background-color: {Assets._background_color};"
                f"color: {Assets._color};"
                f"font-size: {Assets._app_font_size}px;"
            "};"
        )
    @property
    def default_styleSheet(self):
        return (
            f"font-size: {Assets._app_font_size[self.size]}px;"
        )
    @property
    def input_box_styleSheet(self):
        return (
            "background-color: #FFF;"
            "color: #224938;"
            "border: 1px solid #6D8C68;"
            "border-radius: 1px;"
            f"font-size: {Assets._input_box_font_size[self.size]}px;"
            "font-weight: bold;"
        )
    @property
    def predict_box_styleSheet(self):
        return (
            f"font-size: {Assets._predict_box_font_size[self.size]}px;"
            "font-weight: bold;"
        )
    @property
    def result_box_styleSheet(self):
        return (
            f"font-size: {Assets._result_box_font_size[self.size]}px;"
            "font-weight: bold;"
        )


    @property
    def logo_path(self):
        return Assets._logo_path

    @property
    def geometry(self):
        return Assets._geometry[self.size]
    @property
    def logo_height(self):
        return Assets._logo_height[self.size] 
    @property
    def help_button_width(self):
        return Assets._help_button_width[self.size]
    @property
    def predict_box_height(self):
        return Assets._predict_box_height[self.size]
    @property
    def result_box_height(self):
        return Assets._result_box_height[self.size]
            
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
    
    