from rest_framework.response import Response
from rest_framework.decorators import api_view
from .parser import parser
# Create your views here.

@api_view(['GET'])
def main(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        data = parser(query).block()

        # result = {
        #     'query':data,
        #     'method':1,
        # }
        # a = []
        # for i in range(5):
        #     a.append(result)

        return Response(data)

