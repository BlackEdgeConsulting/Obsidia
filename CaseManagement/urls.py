from django.urls import path

from . import views

urlpatterns = [
    path("", views.handle_organization_landing, name="currentOrganization"),
    path("new", views.handle_organization_new, name="newOrganization"),
    path("<int:org_id>/", views.handle_organization_by_index, name="organizationById"),
    path("inventory", views.handle_inventory, name="inventory"),
    path("casefile/<int:casefile_id>", views.handle_casefile, name="casefile")
]