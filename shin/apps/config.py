from pathlib import  Path
basedir = Path(__file__).parent.parent

class BaseConfig :
    SECRET_KEY = "1234"
    WTF_CSRF_SECRET_KEY="1234"

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:7984@localhost:3306/shinfood"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:7984@localhost:3306/shinfood"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

config = {
    "testing" : TestingConfig,
    "local" : LocalConfig
}