from django.shortcuts import render
from .calc import plut
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Production
from .serializers import ProductionSerializer

from .analysis import run_analysis

from itertools import chain
import numpy as np
import json
from ast import literal_eval
from .calc import plut

@api_view(['GET', 'POST'])
def production_list(request, format=None):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        productions = Production.objects.all()
        serializer = ProductionSerializer(productions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        al = Production.objects.all() #delete all previous entry when post is ran
        al.delete()

        # process_data = JSONRenderer().render(request.data)
        process_data = request.data
        print('what the f',process_data)

       
        print(process_data['production_list'])
        processed_rundata = process_data['production_list']
        ################# version 1 ######################
        # process_data = dict(process_data) #change querydict to dictionary values

        # process_data = chain.from_iterable(process_data.values()) # combine into array, and filter into numpy
        # process_data = np.array(list(process_data))

        # process_data= process_data[0] #locate the correct array place
        # process_data = np.fromstring(process_data, sep=',') #convert numpy string into float


        # #process_data = np.add(process_data,100000)
        # process_data = run_analysis(process_data)#run algorithm here


        # process_data= str(process_data)  #convert an array of floats into an array of string so we can input as dictioary

        # #trim the data so it can fit in the input parameters

        # process_data =process_data.replace("  ",",") #there is extra space after first number for some reason
        # process_data =process_data.replace(" ",",")
        # process_data =process_data.replace("[","")
        # process_data =process_data.replace("]","")

        ########################## Version 2 ###############################
        print("done 1")
        print("done 2")
        processed_rundata = JSONRenderer().render(processed_rundata)
        process_data = run_analysis(processed_rundata)
        print("done 3")
        print(process_data)
        process_data = np.squeeze(np.asarray(process_data))
        print(process_data)
        process_data=process_data.tolist()
        print(process_data)

        input_data = {"production_list":process_data} #initialize empty dictionary
       
        # input_data =input_data.replace("]","'")
        print(input_data)
        return Response(input_data, status=status.HTTP_201_CREATED)

        # pre_seal = {'production_list': [1,2,3,4,5]}

        # serializer = ProductionSerializer(data =pre_seal)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def production_detail(request, pk, format=None):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        production = Production.objects.get(pk=pk)
    except Production.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductionSerializer(production)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductionSerializer(production, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        production.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)