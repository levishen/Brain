import re
import configparser
from jpype import *
import matplotlib.pyplot as plt
from collections import Counter
from Text_train import Train
PATH = 'xuangubao/offenceandviolationV3.xlsx'
Text = Train(PATH)
_, _, title, label_count = Text.read_execl()


def Main(title,label_count):
    for i, j in enumerate(label_count):
        if i != len(label_count) - 1:
            title2 = title[j:label_count[i + 1]]

            # 对标题进行清洗
            title_new = Text.clean_data(title2)

            # 对标题进行分词
            token = Text.token(title_new)
            token_count = []
            for i in token:
                tmp = i.split(' ')
                for j in tmp:
                    if len(j) > 1:
                        token_count.append(j)
            # 统计词频
            Count = Counter(token_count)
            print(Count.most_common(20))



# 对分词进行计数

#Count = Counter(token_count)

count = 0
for line in title:
    pattern = re.compile(r'发行|可转债|债券|定增')
    res = pattern.findall(line)   # 返回一个列表
    if res:
        count += 1
    else:
        print(line)
print(count)


# 练习使用配置文件
# config = configparser.ConfigParser()

# 写配置文件

#  config['DEFAULT'] = {'ServerAliveInterval': '45',
#                       'Compression': 'yes',
#                       'CompressionLevel': '9'}
# config['classre.org'] = {'违法违规': '证监会|违法|违规|调查|涉嫌|罚',
#                           '管理层动态': '离职|辞职',
#                           '股权结构异动': '股权|转让|股份',
#                           '实际控制人变更': '实控人|变更|控股股东',
#                           '股票融资': '募资|定增|融资',
#                           '债券融资': '',
#                           '经营动态': ''
#                          }
#
# with open('classre.ini', 'w') as configfile:
#     config.write(configfile)


# 读配置文件

# config.read('classre.ini')
# count = 0
# class_list = config.options('classre.org')
# for i in class_list:
#     char_Pattern = config['classre.org'][i]
#     pattern = re.compile(char_Pattern)
#     if i == '违法违规':
#         for line in title:
#             res = pattern.findall(line)
#             if res:
#                 count += 1
#             else:
#                 print(line)

# if __name__ == '__main__':
    # print(token_count)
    # print(Count.most_common(20))
    # print(count)
    # Main(title, label_count)