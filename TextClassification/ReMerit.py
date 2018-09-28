# 计算正则的准确率和召回率
import xlrd as xl
import re
from re_textclassification import read_ini
from Text_classification import TextClassification
from sklearn import metrics
PATH = 'xuangubao/offenceandviolation2.xlsx'

Text = TextClassification(PATH)


class Metric(object):
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

        label_count = [0]
        count = 0
        label_cal = {}
        for name in names[1:]:  # 不读取第一个子表
            title = []
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
                        # content.append(tmp_con[0])
                        content[-1] = content[-1] + tmp_con[0]
            label_count.append(count)
            label_cal[name] = title

        config = read_ini('classre.ini')  # 读取配置文件

        return label_cal ,config  # 返回lable 和cotent

    def get_title(self):
        """
        获取所有的标题
        :return:
        """
        _, _ ,title_all ,_ = Text.read_execl()
        return title_all

    def get_classification(self,title,config):
        """
        获取所有正则分类后的结果
        :return:
        """
        # 对新闻标题进行清洗
        title_new = Text.clean_data(title)

        # 选择配置文件中的类型
        class_list = config.options('classre.org')

        # 正则匹配得到结果

        re_class = {} # 正则分类后的结果
        for i in class_list:
            result = []
            char_pattern = config['classre.org'][i]
            pattern = re.compile(char_pattern)
            for line in title:
                res = pattern.findall(line)
                if res:
                    result.append(line)
            re_class[i] = result
        return re_class

    def calculation(self,re_class,label_cal,title_all):
        """
        计算准确率与召回率
        :param re_class: 正则分类得到的结果
        :param label_cal: 训练集正确的结果
        :return:
        """
        metdict = {}
        for key in re_class.keys():
            count = 0
            for val in re_class.get(key):
                if val in label_cal.get(key):
                    count += 1
            num_true = len(label_cal.get(key))
            num_pred = len(re_class.get(key))
            precision = round(count/num_pred,3)  # 准确率
            recall = round(count/num_true,3)  # 召回率
            TPR = recall
            FPR = (num_pred-count)/(len(title_all) - num_true)
            # AUC = metrics.auc(FPR,TPR)
            F1 = (2 * precision*recall)/(precision+recall)
            metdict[key] = ['Precision：{}'.format(precision),'Recall：{}'.format(recall)
                            ,'F1:{}'.format(round(F1,3))]

        return metdict


if __name__ == '__main__':
    metric = Metric(PATH)
    label_cal,config = metric.read_execl()
    title_all = metric.get_title()
    re_class = metric.get_classification(title_all,config)
    metdict = metric.calculation(re_class,label_cal,title_all)
    for i in metdict.items():
        print(i)