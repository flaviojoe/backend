from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
)
from django.shortcuts import get_object_or_404

from teacher.models import ClassRoom, Teacher
from teacher.serializers import (
    AddClassSerializer, ClassRoomSerializer, TeacherSerializer
)

class TeacherAPIView(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class AddClassAPIView(APIView):
    def post(self, request, id, format=None):
        teacher = get_object_or_404(Teacher, id=id)
        serializer = AddClassSerializer(data=request.data)
        if serializer.is_valid():
            classroom = ClassRoom(
                name = serializer.validated_data.get('name'),
                email = serializer.validated_data.get('email'),
                teacher = teacher
            )
            classroom.save()
            class_serializer = ClassRoomSerializer(classroom, many=False)
            return Response(class_serializer.data, status=HTTP_201_CREATED)
        return Response(
            {
                "message": "Houveram erros de validação",
                "errors": serializer.errors
            }, 
            status=HTTP_400_BAD_REQUEST
        )
 
class ClassRoomAPIView(ModelViewSet):
    serializer_class = ClassRoomSerializer
    queryset = ClassRoom.objects.all()