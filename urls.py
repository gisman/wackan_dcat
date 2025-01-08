from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(
        r"^dataset/(?P<name>\S+)\.(?P<format>n3|ttl|xml|jsonld)/?$",
        views.dcat,
        name="dcat",
    ),
]
