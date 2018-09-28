import os

from sklearn.externals import joblib
from TextTools import CleanData,TokenWords,DelStop

# 算法计算预测结果


class TextPrediction(object):
    def prediction(self,news):
        model_path = os.path.dirname(os.path.abspath(__file__))+"/lr.pkl"
        tfidf_path = os.path.dirname(os.path.abspath(__file__))+"/tf_fit.pkl"
        Model = joblib.load(model_path)
        tf_fit = joblib.load(tfidf_path)
        content_new = CleanData().clean_data(news)  # 对新闻进行清洗
        Tw = TokenWords()
        seg_content = Tw.token(content_new)  # 分词
        stop_content = DelStop().del_stop(seg_content)  # 去停用词
        tf_tra = tf_fit.transform(stop_content)
        return Model.predict(tf_tra)


if __name__ == '__main__':

    news = ['选股宝讯，四通股份公告，公司拟将截至评估基准日除保留资产以外的全部资产与负债作为置出资产，与磐信昱然等持有的康恒环境100%股权中的等值部分进行资产置换。拟置出资产最终作价8.02亿元，拟置入资产康恒环境100%股权作价85亿元。差额部分由上市公司以发行股份方式自康恒环境全体股东购买，发行价格为9.04元/股。交易完成后，公司将持有康恒环境100%股权，控股股东将变更为磐信昱然。']
    print(TextPrediction().prediction(news))