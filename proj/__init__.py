import pymysql
pymysql.install_as_MySQLdb()


from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
app = Celery('demo')
app.config_from_object('proj.celeryconfig')
