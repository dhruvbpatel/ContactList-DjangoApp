"""contactlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from crudapp import views

urlpatterns = [
    path("", views.insertView.as_view(), name="addview"),
    path("search/", views.listView, name="contact_list"),
    # path('edit/<int:pk>/', views.editView.as_view(), name='editView'),
    path("edit/<int:pk>/", views.updateView.as_view(), name="editView"),
    path("delete/<int:pk>/", views.deleteView.as_view(), name="deleteView"),
    # path('data-table/', views.data_list_table, name="showData"),
    path("show/", views.show),
]
