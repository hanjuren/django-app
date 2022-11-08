from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer


class Categories(APIView):

    def get(self, request):
        categories = Category.objects.all()
        return Response(
            {
                "total": categories.count(),
                "records": CategorySerializer(categories, many=True).data,
            }
        )

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(CategorySerializer(category).data)
        else:
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class CategoryDetail(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        category = self.get_object(pk)
        return Response(CategorySerializer(category).data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, request.data, partial=True)
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)

