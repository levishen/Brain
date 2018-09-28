import requests as req
from TextPredict import TextPrediction
from classification_result import fusions
from re_textclassification import ReTextClassification

# 目前存在的问题，不能确定来的新闻格式，需要将新闻的标题取出来做判断，并将新闻标题和内容返回


def filter_news(title,text):
    """
    新闻过滤器：将新闻标题中不含有公司名称的新闻过滤出去
    :param news: 新拿到的新闻标题
    :return: 如果含有公司名，则返回该新闻给分类器
    """
    ret = req.get('http://10.116.19.195:8011/findCompany?text={}'.format(title[0]))
    if len(ret.text) > 3:
        prediction = TextPrediction().prediction(text)
        print(prediction)
        result = ReTextClassification().re_classification(title)
        print(result)
        result = fusions(prediction, result)
        return result
    else:
        return []


if __name__ == '__main__':
    title,text = (['证监会：方正证券未如实披露控股股东等信息，对相关人员罚款'],['方正证券自IPO开始，连续多年未如实披露控股股东与其他股东的关联关系，违法情节严重。方正集团还隐瞒股东签署的对方正集团股权结构及控制关系产生重大影响的协议，未配合方正证券履行信息披露义务。证监会决定对控股股东顶格处以60万'])
    news_ok = filter_news(title,text)
    print(news_ok)

