from django.urls import path
from .views import echo_view
from .views import GptView
from .views import gpt_view

urlpatterns = [
    path('echo/', echo_view, name='echo'),
    path('gpt/', gpt_view, name='gpt'),
    path('agent/', GptView.as_view(), name='agent')
]