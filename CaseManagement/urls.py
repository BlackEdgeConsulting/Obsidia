from django.urls import path

from . import organization_views

urlpatterns = [
    path("", organization_views.current_organization, name="currentOrganization"),
    path("<int:org_id>/", organization_views.get_organization_by_id, name="organizationById"),
    path("inventory", organization_views.inventory, name="inventory"),
    path("casefile/<int:casefile_id>", organization_views.get_casefile_by_id, name="casefile")
]