from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from config.pagination import Pagination
from .models import Category
from .serializers import CategoryResponseSerializer, CategoryListSerializer, \
    CategoryCreationSerializer, CategoryUpdateSerializer


class Categories(APIView, Pagination):
    @swagger_auto_schema(responses={200: CategoryListSerializer()})
    def get(self, request):
        query = Category.objects.all()

        total = query.count()
        offset = self.offset(request)
        limit = self.limit(request) + offset
        records = query.order_by('created_at')[offset:limit]

        return Response(
            {
                "total": total,
                "records": CategoryResponseSerializer(records, many=True).data,
            }
        )

    @swagger_auto_schema(
        request_body=CategoryCreationSerializer,
        responses={200: CategoryResponseSerializer()}
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
    id_ = openapi.Parameter('id_', openapi.IN_PATH, description='category id', required=True, type=openapi.TYPE_NUMBER)

    @swagger_auto_schema(manual_parameters=[id_], responses={200: CategoryResponseSerializer()})
    def get(self, request, id_):
        category = Category.objects.get(id=id_)
        return Response(CategoryResponseSerializer(category).data)

    @swagger_auto_schema(
        manual_parameters=[id_],
        request_body=CategoryUpdateSerializer,
        responses={200: CategoryResponseSerializer()}
    )
    def put(self, request, id_):
        category = Category.objects.get(id=id_)
        serializer = CategoryUpdateSerializer(
            category,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            serializer.save()
            return Response(CategoryResponseSerializer(category).data)

    @swagger_auto_schema(manual_parameters=[id_])
    def delete(self, request, id_):
        category = Category.objects.get(id=id_)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
