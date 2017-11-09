from rest_framework import mixins, viewsets, status
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from .models import Resources
from .serializers import FileSerializer
import datetime
import os
from .tasks import file_upload, sleep_func
# Create your views here.


class FileViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Resources.objects.all()
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        print("view load file start %s" % datetime.datetime.now().ctime())
        file_list = []
        for file_obj in request.FILES:
            file_list.append(file_obj)
        print("view load file stop %s" % datetime.datetime.now().ctime())
        for file_obj in file_list:
            destination = open(file_obj.name, 'w')
            print("view save file start %s" % datetime.datetime.now().ctime())
            if file_obj.multiple_chunks() is False:
                destination.write(file_obj.read())
            else:
                for chunk in file_obj.chunks():  # 分块写入文件
                    destination.write(chunk)
            destination.close()
        print("view save file stop %s" % datetime.datetime.now().ctime())
        # file_obj = file_upload.delay(request=request.FILE)
        # print file_obj.ready()

        # file_obj = request.data["file"]
        # serializer = self.get_serializer(data=request.data)
        # print "view start2 %s" % datetime.datetime.now().ctime()
        # serializer.is_valid(raise_exception=True)
        # print "view start3 %s" % datetime.datetime.now().ctime()
        # try:
        #     print "view start4 %s" % datetime.datetime.now().ctime()
        #     self.perform_create(serializer)
        # except ValidationError as e:
        #     raise ValidationError(e.detail[0])
        # headers = self.get_success_headers(serializer.data)
        print("view stop %s" % datetime.datetime.now().ctime())
        return Response("OK", status=status.HTTP_201_CREATED)
