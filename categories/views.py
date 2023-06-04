from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategoryResponseSerializer, CategoryCreationSerializer


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
            return Response(serializer.errors)
        else:
            category = serializer.save()
            return Response(CategoryResponseSerializer(category).data)


@api_view()
def get_category(request, id_):
    category = Category.objects.get(id=id_)

    return Response(CategoryResponseSerializer(category).data)
