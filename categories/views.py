from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.response import Response
from .models import Category
from .serializers import CategoryResponseSerializer, CategoryCreationSerializer, CategoryUpdateSerializer


@api_view(["GET", "POST"])
def all_categories(request):
    if request.method == "GET":
        categories = Category.objects.all()

        return Response(
            {
                "message": "OK",
                "records": CategoryResponseSerializer(categories, many=True).data,
            }
        )
    elif request.method == "POST":
        serializer = CategoryCreationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            category = serializer.save()
            return Response(
                CategoryResponseSerializer(category).data,
                status=HTTP_201_CREATED,
            )


@api_view(["GET", "PUT", "DELETE"])
def get_category(request, id_):
    try:
        category = Category.objects.get(id=id_)
    except Category.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        return Response(CategoryResponseSerializer(category).data)
    elif request.method == "PUT":
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
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)

