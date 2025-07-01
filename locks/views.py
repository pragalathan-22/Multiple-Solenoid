# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.views import View

# from .models import LockCommand


# class SendLockCommand(APIView):
#     def post(self, request):
#         port = request.data.get('port')
#         password = request.data.get('password')
#         confirm_password = request.data.get('confirm_password')

#         if not all([port, password, confirm_password]):
#             return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

#         if password != confirm_password:
#             return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

#         LockCommand.objects.create(
#             port=port,
#             password=password,
#             confirm_password=confirm_password,
#             confirmed=True
#         )
#         return Response({'message': 'Command created', 'command': f'open{port}'})


# class GetLatestCommand(APIView):
#     def get(self, request):
#         cmd = LockCommand.objects.filter(confirmed=True).order_by('-created_at').first()
#         if cmd:
#             return HttpResponse(cmd.command_string(), content_type='text/plain')
#         return HttpResponse("", content_type='text/plain')


# class LockControlPage(View):
#     def get(self, request):
#         return render(request, 'locks/control.html')

#     def post(self, request):
#         port = request.POST.get('port')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         message = ""

#         if not all([port, password, confirm_password]):
#             message = "All fields are required."
#         elif password != confirm_password:
#             message = "Passwords do not match."
#         else:
#             LockCommand.objects.create(
#                 port=port,
#                 password=password,
#                 confirm_password=confirm_password,
#                 confirmed=True
#             )
#             message = f"Port {port} unlocked successfully."

#         return render(request, 'locks/control.html', {'message': message})


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from datetime import timedelta

from .models import LockCommand

class SendLockCommand(APIView):
    def post(self, request):
        port = request.data.get('port')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not all([port, password, confirm_password]):
            return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        LockCommand.objects.create(
            port=port,
            password=password,
            confirm_password=confirm_password,
            confirmed=True
        )
        return Response({'message': 'Command created', 'command': f'open{port}'})


class GetLatestCommand(APIView):
    def get(self, request):
        time_threshold = timezone.now() - timedelta(minutes=1)
        cmd = LockCommand.objects.filter(confirmed=True, created_at__gte=time_threshold).order_by('-created_at').first()
        if cmd:
            response = HttpResponse(cmd.command_string(), content_type='text/plain')
            cmd.confirmed = False  # Mark command as used
            cmd.save()
            return response
        return HttpResponse("", content_type='text/plain')


class LockControlPage(View):
    def get(self, request):
        return render(request, 'locks/control.html')

    def post(self, request):
        port = request.POST.get('port')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        message = ""

        if not all([port, password, confirm_password]):
            message = "All fields are required."
        elif password != confirm_password:
            message = "Passwords do not match."
        else:
            LockCommand.objects.create(
                port=port,
                password=password,
                confirm_password=confirm_password,
                confirmed=True
            )
            message = f"Port {port} unlocked successfully."

        return render(request, 'locks/control.html', {'message': message})
