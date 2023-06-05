import unittest

from app import app, db, Movie, User


class WatchlistTestCase(unittest.TestCase):

    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        # 创建数据库和表
        db.create_all()
        # 创建测试数据，一个用户，一个电影条目
        user = User(name='Test', username='test')
        user.set_password('123')
        movie = Movie(title='Test Movie Title', year='2019')
        # 使用 add_all() 方法一次添加多个模型类实例，传入列表
        db.session.add_all([user, movie])
        db.session.commit()

        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表

    # 测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)
        print('1')

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])
        print('2')

    # # 测试 404 页面
    # def test_404_page(self):
    #     response = self.client.get('/nothing')  # 传入目标 URL
    #     data = response.get_data(as_text=True)
    #     self.assertIn('Page Not Found - 404', data)
    #     self.assertIn('Go Back', data)
    #     self.assertEqual(response.status_code, 404)  # 判断响应状态码

    # # 测试主页
    # def test_index_page(self):
    #     response = self.client.get('/')
    #     data = response.get_data(as_text=True)
    #     self.assertIn('Test\'s Watchlist', data)
    #     self.assertIn('Test Movie Title', data)
    #     self.assertEqual(response.status_code, 200)