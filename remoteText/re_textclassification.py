# 接受来自news_filter的新闻，进行正则分类,返回一个类别列表

import re
import configparser
# from jpype import *
# import matplotlib.pyplot as plt
# from collections import Counter
# from Text_classification import TextClassification
from TextTools import CleanData
# PATH = 'xuangubao/offenceandviolationV2.xlsx'
# Text = TextClassification(PATH)
# _, _, title, label_count = Text.read_execl()


class ReTextClassification(object):

    def __init__(self, path='TextClassification/classre.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def write_conf(self,filename):
        """
        写配置文件
        :param file: 文件名称
        :return: 写好的配置文件路径
        """
        config = configparser.ConfigParser()
        config['classre.org'] = {'违法违规': '证监会|违法|违规|调查|涉嫌|罚',
                                  '管理层动态': '离职|辞职',
                                  '股权结构异动': '股权|转让|股份|收购',
                                  '实际控制人变更': '实控人|变更|控股股东',
                                  '股票融资': '募资|定增|融资|增持',
                                  '债券融资': '发行|可转债|债券|证券|定增',
                                  '经营动态': '采购|增长|销量|同比'
                                 }

        with open(filename, 'w') as configfile:
            config.write(configfile)
        return filename

    def read_ini(self,path):
        """
        读配置文件
        :param path:
        :return: 返回读取结果
        """
        config = configparser.ConfigParser()
        config.read(path)
        return config

    def re_classification(self,news):
        """
        按照配置文件进行规制分类
        :param news: 得到的新闻标题
        :return: 类别列表
        """
        # 对新闻标题进行清洗
        title_new = CleanData().clean_data(news)

        # 对分好词的标题进行正则匹配
        class_list = self.config.options('classre.org')  # 读取配置文件中的类别
        class_all = []
        for i in class_list:
            char_pattern = self.config['classre.org'][i]
            pattern = re.compile(char_pattern)
            res = pattern.findall(title_new[0])
            if res:
                class_all.append(i)
        return class_all


if __name__ == '__main__':

    Title = ["好当家：控股股东拟6个月内增持不超过6000万元"]
    # config = ReTextClassification().read_ini('classre.ini')
    # rtc = ReTextClassification()
    result = ReTextClassification().re_classification(Title)
    print(result)




