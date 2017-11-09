from datetime import timedelta
from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://:packet@192.168.72.10:6379/1'
CELERY_RESULT_BACKEND = 'redis://:packet@192.168.72.10:6379/2'

# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'

# import: celery worker -A proj --loglevel=info
CELERY_IMPORTS = (
    'newapp.tasks',
)

# schedules: celery beat -A proj
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'newapp.tasks.sleep_fun',
         'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
         'args': (5,)                           # 任务函数参数
    },
    'multiply-at-some-time': {
        'task': 'newapp.tasks.sleep_fun',
        'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
        'args': (3, )                            # 任务函数参数
    }
}
