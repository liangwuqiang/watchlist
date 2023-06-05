"""
【完结】
主页、编辑、删除
登录、登出、设置
"""
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from watchlist import app, db
from watchlist.models import User, Movie


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    主页
    """
    if request.method == 'POST':
        if not current_user.is_authenticated:  # 用户未登录
            return redirect(url_for('index'))
        
        title = request.form.get('title')  # 在表单中提取数据
        year = request.form.get('year')

        if not title or not year or len(year) > 4 or len(title) > 60:  # 数据验证
            flash('输入无效')
            return redirect(url_for('index'))
        
        movie = Movie(title=title, year=year)  # 数据存入数据库
        db.session.add(movie)
        db.session.commit()
        flash('数据已存入数据库')
        return redirect(url_for('index'))
    
    movies = Movie.query.all()  # 更新主页内容
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    """
    编辑记录
    """
    movie = Movie.query.get_or_404(movie_id)  # 数据库中返回的数据

    if request.method == 'POST': 
        title = request.form['title']  # 从表单中提取的数据
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('输入无效')
            return redirect(url_for('edit', movie_id=movie_id))  # 重来

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('数据库已更新')

        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST']) 
@login_required
def delete(movie_id):
    """
    删除记录
    """
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('数据库中已删除该记录')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录
    """
    if request.method == 'POST':
        username = request.form['username']  # 从表单中提取内容
        password = request.form['password']

        if not username or not password:
            flash('输入无效')
            return redirect(url_for('login'))

        user = User.query.first()  # 与数据库中的用户对比
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('登录成功')
            return redirect(url_for('index')) 

        flash('用户名或密码无效')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """
    登出用户
    """
    logout_user()  # 登出
    flash('再见')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    设置
    """
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('输入无效')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('设置已更新')
        return redirect(url_for('index'))

    return render_template('settings.html')