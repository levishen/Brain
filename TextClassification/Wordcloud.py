# 根据文本标题生成词云图
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from Text_classification import TextClassification
PATH = 'xuangubao/offenceandviolation.xlsx'

Text = TextClassification(PATH)
_, _, title = Text.read_execl()
title = title[:196]
# 对标题进行分词


def token(lines):
    """
    #对文本进行分词
    :return:
    """

    # 清洗标题
    lines_new = []
    for line in lines:
        string = re.sub(r'（.*?）', '', line)
        string1 = re.sub(r'[，。？！“”《》；：* 、.%\d]+', '', string)
        lines_new.append(string1)

    # 分词
    words = []
    for line in lines_new:
        res = jieba.cut(line)
        for word in res:
            words.append(word)
        # f1.write(string + '\n')
    cur_text = ' '.join(words)
    return cur_text
#


def plot_word(word):
    wc = WordCloud(font_path= 'simsun.ttc',
                   background_color="white",  # 背景颜色
                   max_words=200,      # 允许最多词汇
                   max_font_size=100,  # 最大号字体
                   random_state=42,
                   width=1200, height=860, margin=2,
                   )
    wc.generate(word)
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    word = token(title)
    plot_word(word)