"""
【完结】
"""
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:  # Windows系统
    prefix = 'sqlite:///'
else:  # Linux系统
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

login_manager.login_view = 'login'


@app.context_processor  # 指定上下文，这样user就可以在任何地方直接使用，不需要额外引入
def inject_user():  # 注射
    from watchlist.models import User
    user = User.query.first()  # 从数据库中查到第一个用户
    return dict(user=user)  # 返回字典，等同于 return {'user': user}


from watchlist import views, errors, commands  # 这个必须放在最后，避免循环导入

# if __name__ == '__main__':
#     app.run(debug=True)