# -*- coding: utf-8 -*-

# # python stdlib
# import json

# # django imports
# from django.http import HttpResponse
# from django.shortcuts import render

# # horsebook imports
# from horsebook.trainer.models import Trainer
# from horsebook.student.models import Student
# from horsebook.booking.models import Booking


# def search(request):
#     """
#     Fetch all upcomming bookings that the student has booked and show
#     the status of each booking, the payment status etc.
#     """
#     return render(request, 'search/search.html', {})


# def trainer(request):
#     """
#     Search for trainers
#     """
#     term = request.GET.get("term")

#     all_trainers = Trainer.objects.all()
#     result = []

#     for trainer in all_trainers:
#         if trainer.name.startswith(term):
#             result.append({"label": str(trainer), "id": trainer.pk})

#     return JsonResponse(result)


# def student(request):
#     """
#     Search for a student
#     """
#     term = request.GET.get("term")

#     all_students = Student.objects.all()
#     result = []

#     for student in all_students:
#         if student.name.startswith(term):
#             result.append({"label": str(student), "id": student.pk})

#     return JsonResponse(result)


# def location(request):
#     """
#     Search for a booking based on some location
#     """
#     term = request.GET.get("term")
#     all_bookings = Booking.objects.all()
#     result = []

#     for b in all_bookings:
#         if b.street.startswith(term):
#             result.append(
#                 {"id": b.pk, "label": str(b)}
#             )
#         elif b.zipcode.startswith(term):
#             result.append(
#                 {"id": b.pk, "label": str(b)}
#             )
#         elif b.city.startswith(term):
#             result.append(
#                 {"id": b.pk, "label": str(b)}
#             )
#         elif b.county.startswith(term):
#             result.append(
#                 {"id": b.pk, "label": str(b)}
#             )

#     return JsonResponse(result)


# class JsonResponse(HttpResponse):
#     def __init__(self, content, mimetype="application/json", status=None, content_type=None, indent=2):
#         super(JsonResponse, self).__init__(
#             content=json.dumps(content, indent=indent),
#             # mimetype=mimetype,
#             status=status,
#             content_type=content_type
#         )
