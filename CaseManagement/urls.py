from django.urls import path

from . import views

urlpatterns = [
    path("", views.handle_organization_landing, name="currentOrganization"),
    path("new", views.handle_organization_new, name="newOrganization"),
    path("<int:org_id>", views.handle_organization_by_index, name="organizationById"),
    path("inventory", views.handle_organization_inventory, name="inventory"),
    path("inventory/casefiles", views.handle_casefile_inventory, name="inventory"),
    path("inventory/tags", views.handle_tags_inventory, name="inventory"),
    path("casefile/<int:casefile_id>", views.handle_casefile, name="casefile"),
    path("casefile/by_tags", views.handle_casefile, name="all_casefiles"),
]