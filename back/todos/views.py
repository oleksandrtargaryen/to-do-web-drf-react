from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Todo
from .serializers import TodoSerializer
from .services.todo_services import get_user_todos, create_todo, get_todo_by_id, delete_todo

class TodoListCreateAPIView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    def get(self, request):
        todos = get_user_todos(user = request.user)
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data)
    def post(self, request):
        todo = create_todo(user = request.user, data = request.data)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class TodoDetailAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    def get(self, request, todo_id):
        todo = get_todo_by_id(user = request.user, todo_id = todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, todo_id):
        todo = get_todo_by_id(user=request.user, todo_id=todo_id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id):
        # Просто передаємо юзера та ID в сервіс
        # PyCharm побачить, що аргументи (user, todo_id) збігаються з дефініцією
        delete_todo(request.user, todo_id)

        return Response(status=status.HTTP_204_NO_CONTENT)

class TodoListAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed']

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
