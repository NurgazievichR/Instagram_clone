from apps.direct.views import delete_message, inbox, Directs, SendDirect, NewConversation
from django.urls import path

urlpatterns = [
    path('s/', inbox, name="message"),
    path('direct/<username>', Directs, name="directs"),
    path('send/', SendDirect, name="send-directs"),
    path('new/<username>', NewConversation, name="conversation"),
    path('delete_message/<int:id>/<username>', delete_message, name='deleteM')
]