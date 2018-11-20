# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
from flask import Flask, render_template, flash, redirect, url_for, Markup

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
# 用来删除Jinja2语句后的第一个空行
app.jinja_env.trim_blocks = True
# 用来删除Jinja2语句所在行之前的空格和制表符
app.jinja_env.lstrip_blocks = True

# 创建虚拟数据
user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/')
def index():
    return render_template('index.html')


# register template context handler
# 注册模板上下文处理函数
@app.context_processor
def inject_info():
    foo = 'I am foo.'
    return dict(foo=foo)  # equal to等同于: return {'foo': foo}


# register template global function
# 注册模板全局函数
@app.template_global()
def bar():
    return 'I am bar.'


# reigster template filter
# 添加自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')  # 将变量转换为Markup对象 用Markup类将它标记为安全字符


# register template test
# 自定义测试器
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('watchlist_with_static.html', user=user, movies=movies)


# message flashing 闪现
@app.route('/flash')
def just_flash():
    flash(u'I am flash, who is looking for me?你好，我是闪电。')  # Python 2.x中在字符串前添加u前缀
    return redirect(url_for('index'))


# 404 error handler
# 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
