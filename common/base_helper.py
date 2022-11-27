class BaseHelper:

    def limit(self, request):
        try:
            limit = int(request.query_params.get("limit", 105))
            print(limit)
        except ValueError:
            limit = 105
        return limit

    def offset(self, request):
        if request.query_params.get("page"):
            offset = int(request.query_params.get("limit")) * max([int(request.query_params.get("page")) - 1, 0])
        else:
            offset = 0
        return offset
