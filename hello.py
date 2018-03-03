#!/usr/bin/Python
# -*- coding: utf-8 -*-


from flask_wtf import Form
from wtforms import StringField, SubmitField



from flask_mail import Message
from threading import Thread


# 生成一个表单类
# StringField为属性为type=text 的input元素
# SubmitField为属性为type=submit的input元素
# validators=[Required()] 这种写法已经不能用了
class NameForm(Form):
    name = StringField('What is your name?')
    submit = SubmitField('Submit')


# make_shell_context函数注册了程序，数据库实例以及模型，因此这些对象可直接导入shell

# 发送email函数


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# 异步分发email函数


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


# 首页路由第一版
# @app.route('/', methods=['GET','POST'])
# def index():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         old_name = session.get('name')
#         if old_name is not None and old_name != form.name.data:
#             flash('Looks like you have changed your name!')
#         session['name'] = form.name.data
#         # redirect函数的参数是重定向的url
#         return redirect(url_for('index'))
#         # print('用户已经提交数据')
#         # name = form.name.data
#         # print('name======', name)
#         # form.name.data=''
#         # print(form.name)
#     return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())




@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)




# @app.route('/')
# def index():
#     user_agent = request.headers.get('User-Agent')
#     return '<p>Your browser is %s</p>' % user_agent, 400
# @app.route('/')
# def index():
#     return '<h4>Bad Request<h4>', 400
# @app.route('/')
# def index():
#     response = make_response('<h3>This document carries a cookie!<h3>')
#     response.set_cookie('answer', 42)
#     return response
# @app.route('/')
# def index():
#     response = make_response('<h1>This document carries a cookie!</h1>')
#     response.set_cookie('answer', '42')
#     return response

# 重定向
# @app.route('/')
# def index():
#     return redirect('http://www.baidu.com')


# @app.route('/user/<name>')
# def user(name):
#     return '<h5>flask,%s!</h5>' % name
# @app.route('/')
# def index():
#     return 'Index Page'
# @app.route('/user/<username>')
# def profile(username):
#     pass

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()

# @app.route('/login')
# def login():
#     pass
#
# @app.route('/login', methods=['POST','GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'], request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#         return render_template('login.html', error=error)
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('profile', username='JohnDoe'))

# @app.route('/user/<id>')
# def get_user(id):
#     user = load_user(id)
#     if not user:
#         abort(404)
#     return '<h4>hello,%s</h4>' % user.name
