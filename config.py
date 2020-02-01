import os
import json


class Config():
    DEBUG = False
    THREADED = True
    EXE_MODE = 'proc'
    PORT = 80
    HOST = "0.0.0.0"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_PATH = os.getcwd()
    STATIC_FOLDER = "static"
    # SERVER_ADDRESS = "https://kidocode.com/"
    LOGS_FOLDER = os.path.dirname(__file__) + '/app/.log'
    if not os.path.exists(LOGS_FOLDER):
        os.mkdir(LOGS_FOLDER)

    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript',
                          'image/gif', 'image/jpeg', 'audio/mpeg', 'video/mpeg', 'font/otf', 'image/png', 'font/ttf']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500

    try:
        config_data = json.loads(open('key.json').read())
    except:
        config_data = json.loads(open('/var/www/key.json').read())

    DATABASE_CONNECT_OPTIONS = {}

    # EMAILS
    EMAILS = {
        'info': {
            'smtp': ('smtp.gmail.com', 587),
            'auth': (
                os.environ.get('INFO_EMAIL', config_data.get('INFO_EMAIL')),
                os.environ.get('INFO_EMAIL_PASS', config_data.get('INFO_EMAIL_PASS'))
            )

        }
    }

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = config_data.get('CSRF_SESSION_KEY')

    # Secret key for signing cookies
    SECRET_KEY = config_data.get('SECRET_KEY')

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevLocalConfig(Config):
    DEBUG = True
    PORT = 9091
    EXE_MODE = 'DevLocalConfig'
    SERVER_ADDRESS = 'http://localhost:{}/'.format(PORT)
    CONFIG_MOD = 'Local Development ' + 'http://0.0.0.0:' + str(PORT) + '/'
    DATABASES = {
        'mongo': {
            'dbname': Config.config_data.get('LOCAL_DBNAME'),
            'url': Config.config_data.get('LOCAL_MONGODB'),
        }
    }


class LiveConfig(Config):
    DEBUG = False
    PORT = 8081
    EXE_MODE = 'LiveConfig'
    SERVER_ADDRESS = 'https://kidocode.com/'
    CONFIG_MOD = 'Live Development ' + 'https://kidocode.com/'
    DATABASES = {
        'mongo': {
            'auth': True,
            'dbname': Config.config_data.get('LIVE_DBNAME'),
            'url': Config.config_data.get('LIVE_MONGODB'),
        }
    }
