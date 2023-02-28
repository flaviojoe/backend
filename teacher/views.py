from django.db import DatabaseError,IntegrityError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from django.shortcuts import get_object_or_404

from teacher.models import ClassRoom, Teacher
from teacher.serializers import (
    AddClassSerializer, ClassRoomSerializer, TeacherSerializer
)



def _get_full_details(detail):
    if isinstance(detail, dict):
        # return {key: _get_full_details(value) for key, value in detail.items()}
        lista_resp=[]
        for key, value in detail.items():
            # print('chave', key, 'valor', value)
            dict_resp = {key: value}
            if isinstance(value, list):
                for item in value:
                    lista_resp.append(item)
        # print('dados dicionario:', dict_resp)
        try:
            # print(v_key)
            # print(detail)
            if key == 'non_field_errors':
                content = {"message": lista_resp[0]}
            else:
                if key == 'picture':
                    key = 'foto'
                elif key == 'description':
                    key = 'descrição'
                elif key == 'hour_value':
                    key = 'valor_hora'
                elif key == 'name':
                    key = 'nome'
                content = {
                    "message": "campo: {0} - {1}".format(key, lista_resp[0]),
                    "campo": key
                }
            return content 
        except Exception as e:
            print(e)
    else:
        print('caiu aqui')
        return {
            'message': detail
        }

class TeacherAPIView(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def create(self, request):
        teacher_data = TeacherSerializer(data=request.data)
        try:
            teacher_data.is_valid(raise_exception=True)
            pessoa = Teacher.objects.create(
                name=teacher_data.validated_data['name'],
                description=teacher_data.validated_data['description'],
                hour_value=teacher_data.validated_data['hour_value'],
                picture=teacher_data.validated_data['picture']
            )
            pessoa.save()
            serialized_data = TeacherSerializer(pessoa)
            return Response(serialized_data.data,status=HTTP_201_CREATED)
        except IntegrityError:
            content = {"message": "Já existe um professor com essa mesma descrição."}
            return Response(content, status=HTTP_400_BAD_REQUEST)
        
        except DatabaseError:
            content = {"message": "Há uma inconsistência no banco."}
            return Response(content, status=HTTP_400_BAD_REQUEST)

        except ValidationError as err:
            # content = {"message":"Dados inválidos: " + str(err.detail)}
            # print(custom_exception_handler(exc=err, context=err.detail))
            # print(_get_full_details(err.detail))
            content = _get_full_details(err.detail)
            return Response(content, status=HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            # print(custom_exception_handler(exc=e, context='erro'))
            content = {
                "message": str(e)
            }
            return Response(content, status=HTTP_500_INTERNAL_SERVER_ERROR)


class AddClassAPIView(APIView):
    def post(self, request, id, format=None):
        teacher = get_object_or_404(Teacher, id=id)
        serializer = AddClassSerializer(data=request.data)
        if serializer.is_valid():
            try:
                classroom = ClassRoom(
                    name = serializer.validated_data.get('name'),
                    email = serializer.validated_data.get('email'),
                    teacher = teacher
                )
                classroom.save()
                class_serializer = ClassRoomSerializer(classroom, many=False)
                return Response(class_serializer.data, status=HTTP_201_CREATED)
            except IntegrityError:
                    content = {"message": "Erro de duplicidade: Aluno já cadastrado para esse professor."}
                    return Response( content,status=HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
 
class ClassRoomAPIView(ModelViewSet):
    serializer_class = ClassRoomSerializer
    queryset = ClassRoom.objects.all()