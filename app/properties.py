from typing import Literal
import sys

GOLDEN_RATIO = 1.618
class Assets:
    _background_color = "qlineargradient(x1: 0, x2: 1, stop: 0 #122918, stop: 1 #123d2c)"
    _color = "#FFF"
    _logo_path = "assets/v7ai.1.png"
    
    if sys.platform == "darwin":
        _HELP_COMBINATION = "⌃H"
        _CHOOSE_COMBINATION = "[①-⑨]"
        _MOVE_TO_TOP_COMBINATION = "[⌃①-⌃⑨]"
        _REMOVE_LAST_TERM_COMBINATION = "⌫"
        _NEXT_PAGE_COMBINATION = "Right⌥"
        _PREV_PAGE_COMBINATION = "Right⌘"
        _ADD_RAW_COMBINATION = "␣"
        _TOGGLE_ENABLE_COMBINATION = "Right⌘ Left⌘"
        _QUIT_COMBINATION = "⌃ Right⌘ Left⌘"
        
    else:
        _HELP_COMBINATION = "Alt H"
        _CHOOSE_COMBINATION = "[①-⑨]"
        _MOVE_TO_TOP_COMBINATION = "[Alt ①-Alt ⑨]"
        _REMOVE_LAST_TERM_COMBINATION = "⌫"
        _NEXT_PAGE_COMBINATION = "RightCtrl"
        _PREV_PAGE_COMBINATION = "RightAlt"
        _ADD_RAW_COMBINATION = "␣"
        _TOGGLE_ENABLE_COMBINATION = "RightCtrl LeftCtrl"
        _QUIT_COMBINATION = "LeftAlt RightCtrl LeftCtrl"
    
    _geometry = {
        's': (200, 100, int(270*GOLDEN_RATIO), 270),
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
        's': 70,
        'l': 70
    }
    _gui_help_button_width = {
        's': 15,
        'l': 15
    }
    _input_box_font_size = {
        's': 10,
        'l': 20
    }
    _predict_box_font_size = {
        's': 14,
        'l': 20
    }
    _predict_box_height = {
        's': 130,
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
    _gui_help = {
        'en': f"Help: {_HELP_COMBINATION}",
        'vi': f"Trợ giúp: {_HELP_COMBINATION}"
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
        'en': f"Usage: Press key {_CHOOSE_COMBINATION} {_MOVE_TO_TOP_COMBINATION} {_PREV_PAGE_COMBINATION} {_NEXT_PAGE_COMBINATION} {_REMOVE_LAST_TERM_COMBINATION} {_ADD_RAW_COMBINATION}",
        'vi': f"Sử dụng: Dùng phím {_CHOOSE_COMBINATION} {_MOVE_TO_TOP_COMBINATION} {_PREV_PAGE_COMBINATION} {_NEXT_PAGE_COMBINATION} {_REMOVE_LAST_TERM_COMBINATION} {_ADD_RAW_COMBINATION}"
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
    
    _gui_instruction = {
        'en': (
            f"• Please turn off Unikey or other keyboard input tools when using this app to avoid conflicts.\n"
            f"• CapsLock is not supported yet.\n"
            f"• Typing rules is in README.md.\n"
            f"• Press {_CHOOSE_COMBINATION} to choose the combination.\n"
            f"• Press {_MOVE_TO_TOP_COMBINATION} to move the chosen combination to the top.\n"
            f"• Press {_PREV_PAGE_COMBINATION}/{_NEXT_PAGE_COMBINATION} to move to previous/next prediction page.\n"
            f"• Press {_REMOVE_LAST_TERM_COMBINATION} to delete last raw term.\n"
            f"• Press {_ADD_RAW_COMBINATION} to keep raw input.\n"
            f"• Press {_TOGGLE_ENABLE_COMBINATION} to toggle on/off v7.\n"
            f"• Press {_QUIT_COMBINATION} to quit v7."
        ),
            'vi': (
            f"• Tắt VNI / Telex trước khi dùng.\n"
            f"• Chưa hỗ trợ CapsLock.\n"
            f"• Cách gõ nằm trong file README_VI.md.\n"
            f"• Dùng {_CHOOSE_COMBINATION} để xuất cụm từ mong muốn.\n"
            f"• Dùng {_MOVE_TO_TOP_COMBINATION} để chuyển cụm từ mong muốn lên trên.\n"
            f"• Dùng {_PREV_PAGE_COMBINATION}/{_NEXT_PAGE_COMBINATION} để chuyển trang dự đoán trước/sau.\n"
            f"• Dùng {_REMOVE_LAST_TERM_COMBINATION} để xóa thô.\n"
            f"• Dùng {_ADD_RAW_COMBINATION} để xuất thô.\n"
            f"• Dùng {_TOGGLE_ENABLE_COMBINATION} để đóng/mở v7.\n"
            f"• Dùng {_QUIT_COMBINATION} để tắt v7."
        )
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
    def gui_help_button_width(self):
        return Assets._gui_help_button_width[self.size]
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
    def gui_help(self):
        return Assets._gui_help[self.lang]
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
    def gui_instruction(self):
        return Assets._gui_instruction[self.lang]
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
    
    