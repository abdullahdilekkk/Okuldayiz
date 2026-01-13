from django.urls import path
from .views import CommentCreateAPIView

app_name = "comments"

urlpatterns = [
    path("create/", CommentCreateAPIView.as_view(), name="create"),
]
