import os,django
from websocket import views


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wdpy-master.settings")  # project_name 项目名称
    django.setup()
    print('log is comming')
    while True:
        views.send("hello im ");