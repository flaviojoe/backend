from cProfile import label
from rest_framework import serializers
from django.forms import ValidationError
from .models import ClassRoom, Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class AddClassSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    name = serializers.CharField(max_length=100)

    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError('deve ter pelo menos três caracteres')
        return value


class ClassRoomSerializer(serializers.ModelSerializer):
    teacher_name = serializers.ReadOnlyField()

    class Meta:
        model = ClassRoom
        fields = '__all__'