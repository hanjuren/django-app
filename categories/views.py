from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.response import Response
from .models import Category
from .serializers import CategoryResponseSerializer, CategoryCreationSerializer, CategoryUpdateSerializer


class Categories(APIView):
    def get(self, request):
        categories = Category.objects.all()

        return Response(
            {
                "total": categories.count(),
                "records": CategoryResponseSerializer(categories, many=True).data,
            }
        )

    def post(self, request):
        serializer = CategoryCreationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=HTTP_422_UNPROCESSABLE_ENTITY
            )
        else:
            category = serializer.save()

            return Response(
                CategoryResponseSerializer(category).data,
                status=HTTP_201_CREATED,
            )


class CategoryDetail(APIView):
    def get_object(self, id_):
        try:
            return Category.objects.get(id=id_)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, id_):
        category = self.get_object(id_)
        return Response(CategoryResponseSerializer(category).data)

    def put(self, request, id_):
        category = self.get_object(id_)
        serializer = CategoryUpdateSerializer(
            category,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            serializer.save()
            return Response(CategoryResponseSerializer(category).data)

    def delete(self, request, id_):
        category = self.get_object(id_)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
