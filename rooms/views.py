from django.http import HttpResponse


def see_all_rooms(request):
    return HttpResponse("see all rooms.")


def see_one_room(request, id_):
    return HttpResponse(f"see one room. {id_}")


def see_one_order(request, name):
    return HttpResponse(f"{name}")
