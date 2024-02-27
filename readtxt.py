import json

with open('vowels(+none).txt', 'r') as f:
    vowels = f.readlines()
    content = ""
    for vowel in vowels:
        content += f'    \'{vowel[:-1]}\',\n'
    with open('vowels.txt', 'w') as txtf:
        txtf.write(content)