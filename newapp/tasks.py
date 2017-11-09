import time
import redis
import uuid
import datetime
from proj import app
import os

@app.task
def sleep_fun(model_class, validated_data):
    print("task start %s" % datetime.datetime.now().ctime())
    rename = 1
    while model_class.objects.filter(**validated_data).exists():
        tamp = validated_data["name"].split(".")
        if rename == 1:
            tamp[-2] += '(%s)' % str(rename)
        else:
            tamp[-2] = tamp[-2][:-3] + '(%s)' % str(rename)
        validated_data["name"] = ".".join(tamp)
        rename += 1
    instance = model_class.objects.create(**validated_data)
    instance.uuid = "file-" + str(instance.id) + "-" + str(uuid.uuid1()) + "-end"
    instance.save()
    time.sleep(30)     # 模拟耗时操作
    instance.uploaded = True
    instance.save()
    print("task stop %s" % datetime.datetime.now().ctime())
    return instance


@app.task
def file_upload(request):
    print("task start %s" % datetime.datetime.now().ctime())
    print(request)
    my_file = request.data["file"]
    destination = open(os.path.join("E:\\upload", my_file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in my_file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    # file_obj = request.data["file"]
    print("task stop %s" % datetime.datetime.now().ctime())
    return "OK"


@app.task
def sleep_func(a):
    print("task start %s" % datetime.datetime.now().ctime())
    time.sleep(a)     # 模拟耗时操作
    print("task stop %s" % datetime.datetime.now().ctime())
    return "OK over"


queue_name = "celery"
client1 = redis.Redis(host="192.168.72.10", port=6379, db=1, password="packet")
client2 = redis.Redis(host="192.168.72.10", port=6379, db=2, password="packet")


def task_count():
    print(client1.llen(queue_name))
    print(client2.llen(queue_name))
    return True
