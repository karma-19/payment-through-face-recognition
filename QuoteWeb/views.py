from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import QuoteModel
from .serializers import QuoteModelSerializer
import random
#Create your views here.
@api_view(['GET'])
def home(request):
  last = QuoteModel.objects.count() - 1
  index1 = random.randint(0, last)
  index2 = random.randint(0, last - 1)
  if index2 == index1: index2 = last
  serialiser = QuoteModelSerializer(QuoteModel.objects.all(), many=True)
  MyObj1 = QuoteModelSerializer(QuoteModel.objects.all()[index1], many=False)
  MyObj2 = QuoteModelSerializer(QuoteModel.objects.all()[index2], many = False)
  print(MyObj1.data, MyObj2.data)
  return Response({"Quote1":MyObj1.data, "Quote2":MyObj2.data})

# @api_view(['GET'])
# def home(request):
#   return Response({"name":"praveen"})
  