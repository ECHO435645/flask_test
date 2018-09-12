# encoding:utf-8
from flask import Flask,render_template,request,redirect,url_for,session,blueprints
import config
from models import User,Question,Comment
from exts import db
from decorator import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)



@app.route('/')
def index():
    content={
        'question':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**content)

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question = question_model)

@app.route('/add_comment/',methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('answer-comment')
    question_id = request.form.get('question_id')
    comment = Comment(content = content)
    user_id = session['id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    question = Question.query.filter(Question.id == question_id).first()
    comment.question = question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail',question_id = question.id))

@app.route('/logout/')
def logout():
    del session['id']
    return redirect(url_for('login'))


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        '''and user.check_password(password)'''
        if user :
            session['id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"输入的用户名或密码错误！"

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
#         手机号码验证，如果注册过了 提示
        user = User.query.filter(User.telephone == telephone).first()
        # pattern = '^1[3578]\d{9}$'
        # re.match(pattern,telephone,)

        if user:
            return u'该手机号码已被注册！'
        else:
            # 两次密码一致
            if password1 !=password2:
                return u'密码不一致，请核对后再试！'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
#                 注册成功页面跳转
                return redirect(url_for('login'))
# 注销登陆
@app.context_processor
def my_contex_processor():
    id = session.get('id')
    if id:
        user =User.query.filter(User.id == id).first()
        if user:
            return {'user':user}
    return {}

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title = title,content = content)
        id = session.get('id')
        user = User.query.filter(User.id == id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/search/',methods=['GET','POST'])
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html',question= questions)
if __name__ == '__main__':
    app.run()
