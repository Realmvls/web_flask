#!/usr/bin/Python
# -*- coding: utf-8 -*-


# 代码量比较少的时候可以都下在一个hello文件中





# make_shell_context函数注册了程序，数据库实例以及模型，因此这些对象可直接导入shell


#
# @app.route('/user/<name>')
# def user(name):
#     return render_template('user.html', name=name)
#



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
