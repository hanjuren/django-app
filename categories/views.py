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
        data = CategorySerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response("This is Create Category API")
        else:
            return Response(data.errors, status=422)



@api_view()
def category(request, pk):
    queryset = Category.objects.get(pk=pk)

    return Response(CategorySerializer(queryset).data)
