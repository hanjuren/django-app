from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request):
    return HttpResponse("hello")


def see_all_rooms(request):
    return HttpResponse("See all rooms")


def see_one_room(request, room_id):
    return HttpResponse(f"See room with id {room_id}")
