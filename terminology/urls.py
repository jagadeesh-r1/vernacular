from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="IndexPage"),
    path('validate_finite_values',views.finite_values_entity,name="First API"),
    path('validate_numeric_values',views.numeric_values_entity,name="Second API")
]