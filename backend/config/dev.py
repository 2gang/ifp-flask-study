from config.common import *
import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'flastagram.db'))
