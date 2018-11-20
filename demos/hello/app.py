# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import click
from flask import Flask
# from flask_script import Manager # 另外一种控制方法

app = Flask(__name__)
# # 把 Manager 类和应用程序实例进行关联
# manager = Manager(app)


# the minimal Flask application
# 最小的flask应用
@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'


# bind multiple URL for one view function
# 为一个视图函数绑定多个URL
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


# dynamic route, URL variable default
# 动态路由，URL默认变量
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


# custom flask cli command
# 自定义命令
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')


# if __name__ == "__main__":
#     manager.run()