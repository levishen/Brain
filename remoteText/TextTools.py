# 文本处理工具类
from sklearn.feature_extraction.text import TfidfVectorizer

from thrifttest.thrifttest.HanlpUtil import HanlpUtil

from jpype import *
import threading
import re

class CleanData(object):

    def clean_data(self,lines):
        """
        :param lines:
        :return: 清洗好的文本
        """
        content_new = []
        for line in lines:
            string = re.sub(r'（.*?）','',line)
            string1 = re.sub(r'[，。？！“”《》；：* 、.%\d]+','',string)
            string2 = re.sub(r'选股宝讯','',string1)
            string3 = re.sub(r'\(.*?\)','',string2)
            content_new.append(string3)
            # f.write(string3 + '\n')
        # f.close()
        print('清洗完毕')

        return content_new


class TokenWords(object):


    #instance_lock = threading.Lock()

    # def __init__(self):
    #     pass
    #
    # def __new__(cls, *args, **kwargs):
    #     """
    #     单例模式
    #     """
    #     if not hasattr(TokenWords,"_instance"):
    #         #with TokenWords.instance_lock:
    #         if not hasattr(TokenWords,"_instance"):
    #             TokenWords._instance = object.__new__(cls)
    #             startJVM(getDefaultJVMPath(),
    #                      "-Djava.class.path=/opt/hanlp-1.6.4-release/hanlp-1.6.4.jar:/opt/hanlp-1.6.4-release",
    #                      "-Xms1g",
    #                      "-Xmx1g") # 开启JVM
    #             TokenWords.HanLP = JClass('com.hankcs.hanlp.HanLP')
    #     return TokenWords._instance

    def token(self, lines):

        """
        #对文本进行分词
        :return:
        """
        # f1 = open('seg_content.txt','w',encoding='utf-8')

        # if isJVMStarted():
        #     pass
        # else:
        #     startJVM(getDefaultJVMPath(),
        #              "-Djava.class.path=/opt/hanlp-1.6.4-release/hanlp-1.6.4.jar:/opt/hanlp-1.6.4-release",
        #              "-Xms1g",
        #              "-Xmx1g")  # 开启JVM
        # HanLP = JClass('com.hankcs.hanlp.HanLP')
        #
        # han = HanLP.newSegment().enableCustomDictionary(True).enableOrganizationRecognize(True)

        han = HanlpUtil()  # 不再使用JVM，而是改调用高鹏做的thrift接口

        seg_content = []
        for line in lines:
            words = []
            res = han.seg(line)
            for w in res:
                w = str(w)
                word = w.split('/')[0]  # 因为hanlp的分词结果中含有词性，所以要单独将词拿出来
                words.append(word)
            seg_content.append(' '.join(words))  # 将一篇新闻的分词结果转换为一个字符串

        return seg_content


class DelStop(object):

    def del_stop(self,seg_content):
        """
        #去除停用词
        :return:
        """
        stop_words = []
        with open('TextClassification/stopwords.txt',encoding='utf-8') as w:
            for word in w:
                word = word.split('\n')
                stop_words.append(word[0])
        stop_content = []
        for lines in seg_content:
            line = ' '.join([word for word in lines.split() if word not in
                             stop_words])
            stop_content.append(line)
        # print(stop_content)
        return stop_content


class TextVector(object):

    def cal_tf_idf(self,stop_content):
        """
        #提取文本特征tf-idf
        :return:
        """
        tfidf = TfidfVectorizer(ngram_range=(1,2))
        tf_fit = tfidf.fit(stop_content)
        tf_tra = tf_fit.transform(stop_content)
        # 将tf-idf模型固化在磁盘
        # pickle.dump(tf_tra,open('tftra.pickle','wb'))
        # 下载tfidf模型文件
        # tf_tra = pickle.load(open('tftra.pickle', 'rb'))
        return tf_tra.toarray()