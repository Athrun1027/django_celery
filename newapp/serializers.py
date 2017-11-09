import datetime
from rest_framework import serializers
from .models import Resources
from .tasks import sleep_fun


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, write_only=True)
    file2 = serializers.FileField(required=True, write_only=True)

    def create(self, validated_data):
        print("create start1 %s" % datetime.datetime.now().ctime())
        model_class = self.Meta.model
        file_object = validated_data["file"]
        del validated_data["file"]
        validated_data["name"] = file_object.name
        validated_data["size"] = file_object.size
        print("create start2 %s" % datetime.datetime.now().ctime())
        sleep_fun.apply_async(args=(model_class, validated_data))
        # sleep_fun(model_class, validated_data)
        print("create stop %s" % datetime.datetime.now().ctime())
        return {"data": "OK"}

    class Meta:
        model = Resources
        read_only_fields = ['name', 'uuid', 'size', 'uploaded', 'create_time', 'update_time']
        fields = '__all__'
