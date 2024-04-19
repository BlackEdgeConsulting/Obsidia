from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from CaseManagement.models import Organization
from utils import get_db_handle


# handle, db_client = get_db_handle()

def current_organization(request):
    return HttpResponse("Hello, world. You're in the DEFAULT organization\n")

def get_organization_by_id(request, org_id):
    # return HttpResponse(f"You requested Organization ORG-{org_id}")
    return get_object_or_404(Organization, pk=org_id)