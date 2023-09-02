class Pagination:
    def limit(self, request):
        try:
            return int(request.query_params.get("limit", 105))
        except ValueError:
            return 105

    def offset(self, request):
        offset = request.query_params.get("offset", None)

        try:
            if offset:
                return int(offset)
            else:
                page = request.query_params.get("page", None)
                if page:
                    return self.limit(request) * max([int(page) - 1, 0])
                else:
                    return 0
        except ValueError:
            return 0
