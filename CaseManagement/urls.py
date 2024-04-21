from django.urls import path

from . import organization_views

urlpatterns = [
    path("", organization_views.current_organization, name="currentOrganization"),
    path("<int:org_id>/", organization_views.get_organization_by_id, name="organizationById"),
    path("inventory", organization_views.inventory, name="inventory"),
    path("casefile/<int:casefile_id>", organization_views.get_casefile_by_id, name="casefile"),
    path("casefile/all", organization_views.inventory, name="all_casefiles"),
    path("casefile/by_tags", organization_views.get_casefile_by_tags, name="all_casefiles"),
]