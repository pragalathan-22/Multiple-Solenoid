
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import LockCommand
from .serializers import LockCommandSerializer
from .forms import LockCommandForm

@api_view(['POST'])
def create_command(request):
    port = int(request.data.get('port'))
    password = str(request.data.get('password'))
    confirm_password = str(request.data.get('confirm_password'))

    if password != confirm_password:
        return Response({"error": "Passwords do not match"}, status=400)

    if LockCommand.objects.filter(port=port, outtime__isnull=True).exists():
        return Response({"error": "Port already in use. Close session before creating a new one."}, status=400)

    command = LockCommand.objects.create(port=port, password=password, opentime=timezone.now())
    return Response(LockCommandSerializer(command).data)


@api_view(['POST'])
def open_existing_port(request):
    port = int(request.data.get('port'))
    password = str(request.data.get('password'))

    session = LockCommand.objects.filter(port=port, password=password, outtime__isnull=True).order_by('-intime').first()

    if not session:
        return Response({"error": "No active session found or incorrect password"}, status=404)

    session.outtime = timezone.now()
    session.out_opened = False  # Mark as not yet opened
    session.save()

    return Response({
        "success": True,
        "message": f"Device retrieved. Session closed for port {port}.",
        "id": session.id
    })



@api_view(['GET'])
def list_all_sessions(request):
    sessions = LockCommand.objects.all().order_by('-id')
    serializer = LockCommandSerializer(sessions, many=True)
    return Response(serializer.data)


def home(request):
    return render(request, "index.html")


def manage_sessions(request):
    sessions = LockCommand.objects.all().order_by('-id')
    edit_id = request.GET.get('edit')
    delete_id = request.GET.get('delete')

    if request.method == 'POST' and 'delete_all' in request.POST:
        LockCommand.objects.all().delete()
        return redirect('manage_sessions')

    if edit_id:
        session = get_object_or_404(LockCommand, id=edit_id)
        if request.method == 'POST' and 'edit_session' in request.POST:
            form = LockCommandForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                return redirect('manage_sessions')
        else:
            form = LockCommandForm(instance=session)
        return render(request, 'manage_sessions.html', {
            'sessions': sessions,
            'edit_session': session,
            'form': form
        })

    if delete_id:
        session = get_object_or_404(LockCommand, id=delete_id)
        if request.method == 'POST' and 'confirm_delete' in request.POST:
            session.delete()
            return redirect('manage_sessions')
        return render(request, 'manage_sessions.html', {
            'sessions': sessions,
            'delete_session': session
        })

    return render(request, 'manage_sessions.html', {'sessions': sessions})

@api_view(['GET'])
def get_latest_command(request):
    now = timezone.now()

    # Priority: outtime not opened yet
    command = LockCommand.objects.filter(outtime__isnull=False, out_opened=False).order_by('-outtime').first()
    if command and (now - command.outtime).total_seconds() <= 3:
        command.out_opened = True
        command.save()
        return HttpResponse(f"open{command.port}", content_type="text/plain")

    # Otherwise, open based on opentime
    command = LockCommand.objects.filter(outtime__isnull=True).order_by('-intime').first()
    if command and command.opentime and (now - command.opentime).total_seconds() <= 3:
        return HttpResponse(f"open{command.port}", content_type="text/plain")

    return HttpResponse("none", content_type="text/plain")