
name1 = "Đức"
name2 = "Nguyễn"
name3 = "sỮ"

def char_by_char(s):
    print(f'Len: {len(s)}')
    [print(f'[{ch}]') for ch in s]
    [print(f'({s[i]}), {type(s[i])}') for i in range(len(s))]

# char_by_char(name3)
# char_by_char(name2)
