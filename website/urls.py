from django.urls import path
from website.views import HomepageView

urlpatterns = [
    path("", HomepageView.as_view(), name='index'),
]