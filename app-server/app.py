from flask import Flask, request
#跨域问题
# from flask_cors import *
import control.video
import control.book
import control.spider
import control.fateadm_api
# from control import library
import json

app = Flask(__name__)
# CORS(app, supports_credentials=True)

print('python爬虫启动')
@app.route("/")
def hello_world():
    return "Hello World!"

# @app.route('/video/<type>', methods=['GET', 'POST'])
# def video(type):
#     if type == 'frist':
#         return control.video.frist()
#     if type == 'detailed':
#         return control.video.detailed_func(request.data)
#     if type == 'search':
#         return control.video.search_func(request.args.get('q'))


@app.route('/book/<type>', methods=['GET', 'POST'])
def book(type):
    # if type == 'free':
    #     return control.book.free_func()
    # if type == 'wrap':
    #     return control.book.wrap_func()
    # if type == 'week':
    #     return control.book.week_func()
    # if type == 'writer':
    #     return control.book.writer_func()
    # if type == 'detailed':
    #     return control.book.detailed_func(request.args.get('url'))
    # if type == 'detailed_read':
    #     return control.book.read_func(request.args.get('url'), request.args.get('type'))
    # if type == 'detailed_list':
    #     return control.book.list_func(request.args.get('url'))
    # if type == 'groom':
    #     return control.book.groom_func()
    # if type == 'search':
    #     return control.book.search_func(request.args.get('value'))
    # 图书馆图书查询
    if type == 'searchBook':
        return control.book.findBook_func(request.args.get('value'))

@app.route('/spider/<type>', methods=['GET', 'POST'])
def spider(type):
    # 获取校园卡主页信息
    if type=='gotoHome':
        return control.spider.gotoHome(request.args.get('value'))
    # 获取校园卡消费历史记录
    if type=='gotoBalance':
        return control.spider.gotoBalance(request.args.get('value'))


# if __name__ == '__main__':
#     app.debug = True
#     app.run(threaded=True)
if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True) #多线程
    # app.run()
    # app.run(debug=True,host='0.0.0.0', port=8080)

