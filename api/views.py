from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

# Create your views here.

def hello_word(request):

    return JsonResponse({'text':'hello world'})

    #return Response('Hello World', status=status.HTTP_200_OK)
