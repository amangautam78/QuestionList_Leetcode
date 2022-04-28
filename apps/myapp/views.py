from asyncio import QueueEmpty
from django.shortcuts import render
from html5lib import serialize
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question
from .serializer import QuestionSerializer
from rest_framework import status
# Create your views here.

#views to get the questionlists (url: http://127.0.0.1:8000/question-list/)
class QuestionList(APIView):
    def get(self, request):
        question = Question.objects.all()
        serialize = QuestionSerializer(question, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)
#views to create a question (urlhttp://127.0.0.1:8000/add/)
class CreateQuestion(APIView):
    def post(self, request):
        question = request.data
        serialize = QuestionSerializer(data = question)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

#views to get, update(put) and delete a particular quesion from the list(http://127.0.0.1:8000/question/<int:id>/)
class UpdateQuestion(APIView):
    def get(self, request, id):
        try:
            question = Question.objects.get(pk=id)
        except Question.DoesNotExist:
            return Response({'error':'question does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serialize = QuestionSerializer(question)
        return Response(serialize.data, status = status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            question = Question.objects.get(pk=id)
        except Question.DoesNotExist:
            return Response({'error':'question does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serialize = QuestionSerializer(question, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        question = Question.objects.get(pk=id)
        question.delete()
        return Response({'status':'Question deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
