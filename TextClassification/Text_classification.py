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
from sklearn.model_selection import cross_val_score
import numpy as np
import pickle
from jpype import *
import re
import xlrd as xl

# 新闻分类Version 1.0
PATH = 'xuangubao/offenceandviolation.xlsx'


class TextClassification(object):
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
        for name in names[1:]:  # 不读取第一个子表
            table = data.sheet_by_name(name)
            nrows = table.nrows   # 判断表有多少有效行数
            for i in range(nrows):
                tmp_con = table.row_values(rowx=i)
                tmp_con = [j for j in tmp_con if len(j) > 3]  # 过滤掉中间的空单元格
                if tmp_con:
                    if len(tmp_con) > 1:    # 预防没有标题的列表报错
                        content.append(tmp_con[1])
                    else:
                        content.append(tmp_con[0])
                    label.append(name)
        return label, content   # 返回lable 和cotent

    def clean_data(self):
        """
        #去除符号等字符
        :return:
        """
        content_new = []
        f = open('content.txt','w',encoding='utf-8')
        for line in content:
            string = re.sub(r'（.*?）','',line)
            string1 = re.sub(r'[，。？！“”《》；：* 、.%\d]+','',string)
            string2 = re.sub(r'选股宝讯','',string1)
            string3 = re.sub(r'\(.*?\)','',string2)
            content_new.append(string3)
            f.write(string3 + '\n')
        f.close()
        print('清洗完毕')
        return content_new

    def token(self):
        """
        #对文本进行分词
        :return:
        """
        f1 = open('seg_content.txt','w',encoding='utf-8')
        startJVM(getDefaultJVMPath(),
                 "-Djava.class.path=/opt/hanlp-1.6.4-release/hanlp-1.6.4.jar:/opt/hanlp-1.6.4-release", "-Xms1g",
                 "-Xmx1g")
        HanLP = JClass('com.hankcs.hanlp.HanLP')
        han = HanLP.newSegment().enableCustomDictionary(True).enableOrganizationRecognize(True)

        seg_content = []
        for line in content_new:
            words = []
            res = han.seg(line)
            for w in res:
                w = str(w)
                word = w.split('/')[0]
                words.append(word)
            seg_content.append(' '.join(words))
            # f1.write(string + '\n')
        return seg_content

    def del_stop(self):
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
        for lines in seg_content:
            line = ' '.join([word for word in lines.split() if word not in
                             stop_words])
            stop_content.append(line)
        # print(stop_content)
        return stop_content

    def cal_tf_idf(self):
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

# 打印大于阈值的tf-idf值
        # words = tf_fit.get_feature_names()
        # for i in range(len(stop_content)):
        #     print('-----Document %d-----'%(i))
        #     for j in range(len(words)):
        #         if tf_tra[i,j] > 0.1:
        #             print(words[j],tf_tra[i,j])

        # print(tf_tra.toarray())
        # print(tf_tra.toarray().shape)
        # print(tf_fit.vocabulary_)
        # print(tf_fit.idf_)
        return tf_tra.toarray()

    def get_data(self):
        """
        #处理数据，得到训练集和测试集
        :return:
        """
        X_train,X_test,y_train,y_test = train_test_split(tf_tra,label,test_size= 0.5,random_state=42)
        return X_train,X_test,y_train,y_test

    def get_model(self):
        """
        #训练模型，返回模型结果
        :return:
        """
        lr = LogisticRegression(multi_class = 'multinomial',solver = 'sag',max_iter= 20000)
        lr.fit(X_train,y_train)
        y_pred = lr.predict(X_test)
        return lr,y_pred

    def eva_model(self,report):
        """
        #多维度评价模型
        :return:
        """
        if report == True:
            print(classification_report(y_test,y_pred)) # 模型评价报告
        return cross_val_score(lr,X_test,y_test) # 交叉验证


if __name__ == '__main__':
    Text = TextClassification(PATH)
    label, content = Text.read_execl()
    content_new = Text.clean_data()
    seg_content = Text.token()
    stop_content = Text.del_stop()
    tf_tra = Text.cal_tf_idf()
    X_train, X_test, y_train, y_test = Text.get_data()
    lr,y_pred = Text.get_model()
    score = Text.eva_model(True)


# version 1.0已经完成，下一步需要改进的地方
# 1：特征，加入chi2提取特征；
# 2：自己想一些特征加加来，比如文本的关键词，或者标题
# 3：使用正则分类，将这两种分类结果综合使用




