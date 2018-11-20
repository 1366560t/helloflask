# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
from flask_ckeditor import CKEditorField  # 从flask_ckeditor包导入
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError, Email


# 4.3.1 basic form example基本形式示例
class LoginForm(FlaskForm):
    # 文本字段StringField
    # 验证器（validator）是用于验证字段数据的类  使用validators关键字来指定附加的验证器列表
    # DataRequired验证器，用来验证输入的数据是否有效
    username = StringField('Username', validators=[DataRequired()])
    # 密码字段Password-Field
    # Length验证器，用来验证输入的数据长度是否在给定的范围内
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    # 勾选框字段BooleanField
    remember = BooleanField('Remember me')
    # 提交按钮字段SubmitField
    submit = SubmitField('Log in')


# custom validator 自定义验证器
# 针对特定字段的验证器 行内验证器
class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number')
    submit = SubmitField()

    # 当表单类中包含以“validate_字段属性名”形式命名的方法时，在验证字段数据时会同时调用这个方法来验证对应的字段
    # form为表单类实例  field为字段对象
    def validate_answer(form, field):
        # 通过field.data获取字段数据
        if field.data != 42:
            # 验证出错时抛出从wtforms.validators模块导入的ValidationError异常
            raise ValidationError('Must be 42.')


# upload form 上传表格
class UploadForm(FlaskForm):
    # 扩展Flask-WTF提供的FileField类 创建文件上传字段
    # FileRequired确保提交的表单字段中包含文件数据
    # FileAllowed设置允许的文件类型
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField()


# multiple files upload form 多个文件上传表单
class MultiUploadForm(FlaskForm):
    # DataRequired验证器来确保包含文件
    photo = MultipleFileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField()


# multiple submit button 多个提交按钮 包含两个提交按钮的表单
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save')  # 保存按钮
    publish = SubmitField('Publish')  # 发布按钮


# 为两个表单设置不同的提交字段名称
class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit1 = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit2 = SubmitField('Register')


class SigninForm2(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField()


class RegisterForm2(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 24)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField()


# CKEditor Form 文章表单
class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')
