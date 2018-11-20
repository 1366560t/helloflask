# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
try:  # 兼容性处理
    from urlparse import urlparse, urljoin  # python2
except ImportError:
    from urllib.parse import urlparse, urljoin  # python3

from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify

app = Flask(__name__)
# 密钥可以通过Flask.secret_key属性或配置变量SECRET_KEY设置
# 把密钥写进系统环境变量（在命令行中使用export或set命令），或是保存在.env文件中：SECRET_KEY=secret string
# 使用os模块提供的getenv（）方法获取
# 在getenv（）方法中添加第二个参数，作为没有获取到对应环境变量时使用的默认值
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


# get name value from query string and cookie
# 从查询字符串和cookie中获取名称值
@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')  # 获取查询参数name的值
    if name is None:
        name = request.cookies.get('name', 'Human')  # 从Cookie中获取name值
        # Jinja2提供的escape（）函数对用户传入的数据进行转义
    response = '<h1>Hello, %s!</h1>' % escape(name)  # 转义名称以避免XSS escape name to avoid XSS
    # return different response according to the user's authentication status
    # 根据用户认证状态返回不同的内容  session中的数据可以像字典一样
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


# redirect
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


# use int URL converter
# 使用int URL转换器  把year的值转换为整数
@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to %d!' % (2018 - year)


# use any URL converter
# 使用anyURL转换器
@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


# return error response
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)  # abort（）函数中传入状态码即可返回对应的错误响应
    else:
        return 'A drop of tea.'


# 404
@app.route('/404')
def not_found():
    abort(404)  # abort（）函数前不需要使用return语句，一旦abort（）函数被调用，abort（）函数之后的代码将不会被执行。


# return response with different formats
# 返回不同格式的响应
@app.route('/note', defaults={'content_type': 'text'})
@app.route('/note/<content_type>')
def note(content_type):
    content_type = content_type.lower()  # 小写处理？
    if content_type == 'text':
        body = '''Note
to: Peter
from: Jane
heading: Reminder
body: Don't forget the party!
'''
        response = make_response(body)  # make_response（）方法生成响应对象，传入响应的主体作为参数
        response.mimetype = 'text/plain'  # 响应对象的mimetype属性设置MIME类型 # 纯文本
    elif content_type == 'html':
        body = '''<!DOCTYPE html>
<html>
<head></head>
<body>
  <h1>Note</h1>
  <p>to: Peter</p>
  <p>from: Jane</p>
  <p>heading: Reminder</p>
  <p>body: <strong>Don't forget the party!</strong></p>
</body>
</html>
'''
        response = make_response(body)
        response.mimetype = 'text/html'  # HTML
    elif content_type == 'xml':
        body = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Peter</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget the party!</body>
</note>
'''
        response = make_response(body)
        response.mimetype = 'application/xml'  # XML
    elif content_type == 'json':
        body = {"note": {
            "to": "Peter",
            "from": "Jane",
            "heading": "Remider",
            "body": "Don't forget the party!"
        }
        }
        response = jsonify(body)  # Flask更方便的jsonify（）函数
        # equal to:  # 这是python json模块的dumps方法  将字典、列表或元组序列化为JSON字符串
        # response = make_response(json.dumps(body))
        # response.mimetype = "application/json"  # JSON
    else:
        abort(400)
    return response


# set cookie 设置cookie（不安全的）
@app.route('/set/<name>')
def set_cookie(name):
    # make_response（）方法手动生成响应对象，传入响应的主体作为参数
    response = make_response(redirect(url_for('hello')))
    # 在响应中添加一个cookie
    response.set_cookie('name', name)
    return response


# log in user 安全的用户登录
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))  # redirect（）函数来生成重定向响应 url_for（）函数生成目标URL


# protect view 受保护的视图  模拟管理后台
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


# log out user 注销用户  登出账户
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')  # 字典的pop方法
    return redirect(url_for('hello'))


# AJAX 异步加载长文章示例
@app.route('/post')
def show_post():
    # 随机正文通过Jinja2提供的generate_lorem_ipsum（）函数生成 一段常用的无意义的填充文字
    post_body = generate_lorem_ipsum(n=2)  # n参数用来指定段落的数量，默认为5
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {                      // $（function（）{...}）用来在页面DOM加载完毕后执行代码
    $('#load').click(function() {    // $（'#load'）选择器  .click（function（）{...}）会为加载按钮注册一个单击事件处理函数
        $.ajax({                     // $.ajax（）方法发送一个AJAX请求
            url: '/more',                      // 目标url设为“/more”
            type: 'get',                       // 请求方法的类型设为GET
            success: function(data){       // 请求成功处理并返回2XX响应 会触发success回调函数
                $('.body').append(data);       // 将返回的响应插入到页面中
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)


# redirect to last page 重定向回上一个页面
@app.route('/foo')
def foo():
    # request.full_path获取当前页面的完整路径
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    # 指向do_something视图的链接
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/do-something')
def do_something():
    # do something here
    return redirect_back()


# 验证url安全性(通用）否则会形成开放重定向漏洞
def is_safe_url(target):
    # urlparse（）函数解析两个URL
    # 通过request.host_url获取程序内的主机URL
    ref_url = urlparse(request.host_url)
    # 使用urljoin（）函数将目标URL转换为绝对URL
    test_url = urlparse(urljoin(request.host_url, target))
    # 对目标URL的URL模式和主机地址进行验证
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# 返回上页(通用）默认重定向到hello视图
def redirect_back(default='hello', **kwargs):
    # 获取next参数 如果为空就尝试获取refere
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
