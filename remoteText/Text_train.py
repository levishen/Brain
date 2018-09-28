# 接受来自news_filter的新闻，进行分类，返回一个分类结果

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from thrifttest.thrifttest.HanlpUtil import HanlpUtil
from sklearn.model_selection import cross_val_score
import numpy as np
import pickle
from sklearn.externals import joblib
from jpype import *
import re
import xlrd as xl

# startJVM(getDefaultJVMPath(),
#          "-Djava.class.path=/opt/hanlp-1.6.4-release/hanlp-1.6.4.jar:/opt/hanlp-1.6.4-release", "-Xms1g",
#          "-Xmx1g")
# HanLP = JClass('com.hankcs.hanlp.HanLP')


# 新闻分类Version 1.0
PATH = 'xuangubao/offenceandviolationV3.xlsx'


class Train(object):
    def __init__(self,path):
        self.path = path

    def read_execl(self):
        """
        #从excel文件读入文本
        :return:label，content
        """
        data = xl.open_workbook(self.path)
        names = data.sheet_names()
        label = []
        content = []
        title = []
        label_count = [0]
        count = 0
        for name in names[1:]:  # 不读取第一个子表
            table = data.sheet_by_name(name)
            nrows = table.nrows   # 判断表有多少有效行数
            for i in range(nrows):
                tmp_con = table.row_values(rowx=i)
                tmp_con = [j for j in tmp_con if len(j) > 3]  # 过滤掉中间的空单元格
                if tmp_con:
                    if len(tmp_con) > 1:    # 预防没有标题的列表报错
                        content.append(tmp_con[1])
                        title.append(tmp_con[0])
                        label.append(name)
                        count += 1
                    else:
                        content[-1] = content[-1] + tmp_con[0]
            label_count.append(count)
        return label, content,title,label_count   # 返回lable 和cotent

    def clean_data(self, lines):
        """
        #去除符号等字符
        :return:
        """
        content_new = []
        #f = open('content.txt','w',encoding='utf-8')
        for line in lines:
            string = re.sub(r'（.*?）','',line)
            string1 = re.sub(r'[，。？！“”《》；：* 、.%\d]+','',string)
            string2 = re.sub(r'选股宝讯','',string1)
            string3 = re.sub(r'\(.*?\)','',string2)
            content_new.append(string3)
            #f.write(string3 + '\n')
        #f.close()
        print('清洗完毕')
        return content_new

    def token(self,lines):
        """
        #对文本进行分词
        :return:
        """
        # f1 = open('seg_content.txt','w',encoding='utf-8')

        # han = HanLP.newSegment().enableCustomDictionary(True).enableOrganizationRecognize(True)
        han = HanlpUtil()

        seg_content = []
        for line in lines:
            words = []
            res = han.seg(line)
            for w in res:
                w = str(w)
                word = w.split('/')[0]
                words.append(word)
            seg_content.append(' '.join(words))
            # f1.write(string + '\n')
        return seg_content

    def del_stop(self,seg):
        """
        #去除停用词
        :return:
        """
        stop_words = []
        with open('stopwords.txt',encoding='utf-8') as w:
            for word in w:
                word = word.split('\n')
                stop_words.append(word[0])
        stop_content = []
        for lines in seg:
            line = ' '.join([word for word in lines.split() if word not in
                             stop_words])
            stop_content.append(line)
        # print(stop_content)
        return stop_content

    def cal_tf_idf(self,stop):
        """
        #提取文本特征tf-idf
        :return:
        """
        # tfidf = TfidfVectorizer(ngram_range=(1,2))
        tfidf = TfidfVectorizer()
        tf_fit = tfidf.fit(stop)
        tf_tra = tf_fit.transform(stop)

        joblib.dump(tf_fit,'tf_fit.pkl')
# 将tf-idf模型固化在磁盘
        # pickle.dump(tf_tra,open('tftra.pickle','wb'))
        # 下载tfidf模型文件
        # tf_tra = pickle.load(open('tftra.pickle', 'rb'))

# 打印大于阈值的tf-idf值
#         words = tf_fit.get_feature_names()
#         for i in range(len(stop_content)):
#             print('-----Document %d-----'%(i))
#             for j in range(len(words)):
#                 if tf_tra[i,j] > 0.1:
#                     print(words[j],tf_tra[i,j])

        # print(tf_tra.toarray())
        # print(tf_tra.toarray().shape)
        # print(tf_fit.vocabulary_)
        # print(tf_fit.idf_)

        return tf_tra.toarray()

    def get_data(self,tf_tra,label):
        """
        #处理数据，得到训练集和测试集
        :return:
        """
        X_train,X_test,y_train,y_test = train_test_split(tf_tra,label,test_size= 0.2,random_state=42)
        return X_train,X_test,y_train,y_test

    def get_model(self,X_train,y_train,X_test):
        """
        #训练模型，返回模型结果
        :return:
        """
        lr = LogisticRegression(multi_class = 'multinomial',solver = 'sag',max_iter= 20000)
        lr.fit(X_train,y_train)
        y_pred = lr.predict(X_test)
        joblib.dump(lr, 'lr.pkl')
        return lr, y_pred

    def eva_model(self,report,y_test,y_pred):
        """
        #多维度评价模型
        :return:
        """
        if report == True:
            # print(classification_report(y_test,y_pred)) # 模型评价报告
            # return cross_val_score(lr,X_test,y_test) # 交叉验证
            return classification_report(y_test,y_pred)


if __name__ == '__main__':
    Text = Train(PATH)
    label, content, title,label_count = Text.read_execl()
    content_new = Text.clean_data(content)
    seg_content = Text.token(content_new)
    stop_content = Text.del_stop(seg_content)
    tf_tra = Text.cal_tf_idf(stop_content)
    X_train, X_test, y_train, y_test = Text.get_data(tf_tra,label)
    lr,y_pred = Text.get_model(X_train,y_train,X_test)
    score = Text.eva_model(True,y_test,y_pred)


# version 1.0已经完成，下一步需要改进的地方
# 1：特征，加入chi2提取特征；
# 2：自己想一些特征加加来，比如文本的关键词，或者标题
# 3：使用正则分类，将这两种分类结果综合使用




