from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'tangle'
# 因为编码问题这里将mysql改为mysql+mysqlconnector，解决warning:1366问题，在这之前需要pip install mysql+mysqlconnector
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:******@127.0.0.1/flask_sql_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
'''
两张表
角色（管理员/普通用户）
用户（角色ID）
'''

# 数据库的模型，类需要继承db.Model,相当于数据库的一个表
class Role(db.Model):
    # 定义表名和字段
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    # 添加关系引用，不是字段，只是方便调用查询的属性，User为模型的名字（不是数据库中表的名字
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role: %s %s>' %(self.name, self.id)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    # 以下方式表示外键，roles为上表表名
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # User希望有一个role属性，但需要在另一个模型中定义

    def __repr__(self):
        return '<User: %s %s %s %s>' %(self.name, self.id, self.email, self.password)


# flash需要对内容加密 app.secret_key = '密文'
# 使用flask wtf实现表单 index为普通表单实现方式，login页面为wtf表单实现方式-->实现一步验证
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password1 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', 'correct your password')])
    submit = SubmitField('提交')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('username')
        password1 = request.form.get('username')

        if login_form.validate_on_submit():
            return 'success'
        else:
            # 这里应该捕获line-19抛出的error，方便起见直接flash('参数有误')
            flash('参数有误')

    # 传参，form是模板中要用到的变量
    return render_template('login.html', form=login_form)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        # print(username, password, password1)
        if not all([username, password, password1]):
            # print('complete all arguments')
            flash('complete all arguments')
        elif(password1 != password):
            flash('correct your password')
            # print('correct your password')
        else:
            return('success')

    return render_template('index.html')

if __name__ == '__main__':
    # 删除表，确保每次运行表都是干净的，数据没有冗余，实际中别这么干
    db.drop_all()
    # 创建表
    db.create_all()

    # 创建表之后进行操作
    role_1 = Role(name='admin')
    db.session.add(role_1)
    db.session.commit()
    role_2 = Role(name='user')
    db.session.add(role_2)
    db.session.commit()

    user_1 = User(name='zs', email='zs@qq.com', password='123456', role_id=role_1.id)
    user_2 = User(name='ls', email='ls@163.com', password='455345', role_id=role_2.id)
    user_3 = User(name='wu', email='wu@126.com', password='135634', role_id=role_2.id)
    user_4 = User(name='zl', email='zl@mail.com', password='635354', role_id=role_2.id)
    user_5 = User(name='wq', email='wq@163.com', password='567767', role_id=role_2.id)
    user_6 = User(name='jb', email='jb@qq.com', password='854564', role_id=role_2.id)
    user_7 = User(name='ll', email='ll@126.com', password='345674', role_id=role_2.id)
    user_8 = User(name='mm', email='mm@126.com', password='256735', role_id=role_2.id)
    user_9 = User(name='gg', email='gg@163.com', password='745645', role_id=role_2.id)
    user_10 = User(name='xc', email='xc@qq.com', password='345435', role_id=role_2.id)
    db.session.add_all([user_1, user_2, user_3, user_4, user_5, user_6, user_7, user_8, user_9, user_10])
    db.session.commit()

    app.run(debug=True)
