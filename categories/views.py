from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        queryset = Category.objects.all()

        total = queryset.count()
        records = CategorySerializer(queryset, many=True).data
        return Response(
            {
                "total": total,
                "records": records,
            }
        )
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors, status=422)


@api_view()
def category(request, pk):
    queryset = Category.objects.get(pk=pk)

    return Response(CategorySerializer(queryset).data)
