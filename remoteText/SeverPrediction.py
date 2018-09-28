from flask import Flask, Response, request, make_response, jsonify, g, render_template

from news_filter import filter_news
import ModelTrain

app = Flask(__name__)
@app.route('/')
def index():
    response = make_response(jsonify({'Hello':'world'}))
    return response


@app.route('/classification', methods=['GET'])
def classification():
    text = request.args.get('text')  # 获取URL中提供的参数
    text = [text]
    title = request.args.get('title')
    title = [title]
    res = filter_news(title,text)
    print(res)
    if res == []:
        res = '无效新闻'
    data = {
        'prediction':res
    }
    return make_response(jsonify(data))

@app.route('/train')
def train():
    res = ModelTrain.train()
    # return make_response(res)
    return make_response(jsonify('训练完成'))


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0',port=5001,debug=True)


# 2018.09.21
# 报JVM已启动，解决方案，关闭JVM或者，使用单例模式(高鹏）
