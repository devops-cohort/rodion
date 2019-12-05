def test_aboutpage_view(self):
    #Test that aboutpage is accesible
    response = self.client.get(url_for('about'))
    self.assertEqual(response.satus_code, 200)

def test_login_view(self):
    #Test that loginpage is accesible
    response = self.client.get(url_for('login'))
    self.assertEqual(response.satus_code, 200)

def test_aboutpage_view(self):
    #Test that registerpage is accesible
    response = self.client.get(url_for('register'))
    self.assertEqual(response.satus_code, 200)

class TestBase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('MYSQL_USER'))+':'+str(getenv('MY            SQL_PASS'))+'@'+str(getenv('MYSQL_URL'))+'/'+str(getenv('MYSQL_DB_TEST'))        )
    return app
    
    def setup(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

        admine = Users(first

