# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, ShiftViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'shifts', ShiftViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employees/<int:pk>/shifts/', EmployeeViewSet.as_view({'get': 'shifts'}), name='employee-shifts'),

]