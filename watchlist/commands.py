"""
【完结】
"""
import click
from watchlist import app, db
from watchlist.models import User, Movie


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='删除后重建')  # 设置选项
def initdb(drop):
    """ 
    数据库初始化
    $ flask initdb
    $ flask initdb --drop
    """
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('数据库已被初始化')  # 输出提示信息


@app.cli.command()
def forge():  # 伪造数据
    """ 
    创建测试数据 
    $ flask forge
    完成
    """
    db.create_all()

    # name = 'Grey Li'
    # user = User(name=name)
    # db.session.add(user)

    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('完成')


@app.cli.command()
@click.option('--username', prompt=True, help='用于登录的用户名')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='用于登录的密码')
def admin(username, password):
    """ 
    创建用户 
    $ flask admin
    Username: greyli
    Password:
    Repeat for confirmation:
    正在更新用户...
    完成
    """
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('正在更新用户...')
        user.username = username  # 更新原用户
        user.set_password(password)
    else:
        click.echo('正在创建用户...')
        user = User(username=username, name='Admin')  # 新建用户
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('完成')