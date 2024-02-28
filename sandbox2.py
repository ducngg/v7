from vietnamese import Vietnamese
from long_text import *
import utils

corpus = "ghi ghệ duềnh quẹo giềng giêng giết giến giêm pin pía pô khuếch giũa ngoèo óoc"

for word in utils.separate_words(corpus):
    print(Vietnamese.AVT(word))