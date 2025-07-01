# from django.urls import path
# from .views import SendLockCommand, GetLatestCommand, LockControlPage

# urlpatterns = [
#     path('send-command/', SendLockCommand.as_view()),
#     path('get-latest-command/', GetLatestCommand.as_view()),
#     path('control/', LockControlPage.as_view(), name='lock_control'),  # Web page UI
# ]

# urls.py
from django.urls import path
from .views import SendLockCommand, GetLatestCommand, LockControlPage

urlpatterns = [
    path('send-lock-command/', SendLockCommand.as_view(), name='send-lock-command'),
    path('get-latest-command/', GetLatestCommand.as_view(), name='get-latest-command'),
    path('control/', LockControlPage.as_view(), name='lock-control-page'),
]