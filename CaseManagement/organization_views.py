from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import Http404, HttpResponse
from CaseManagement.models import CaseFile, Organization
from utils import get_db_handle


# handle, db_client = get_db_handle()

def current_organization(request):
    return HttpResponse("Hello, world. You're in the DEFAULT organization\n")

def get_organization_by_id(request, org_id):
    # return HttpResponse(f"You requested Organization ORG-{org_id}")
    orginization = get_object_or_404(Organization, pk=org_id)
    return HttpResponse(orginization)

def get_casefile_by_id(request, casefile_id):
    organization = _get_current_users_organization()
    casefile = CaseFile.objects.filter(pk=casefile_id, organization__id=organization.pk) # pylint: disable=no-member
    return HttpResponse(casefile)
    
def inventory(request):
    organization = _get_current_users_organization()
    return _get_inventory_by_organization(organization)

def _get_current_users_organization():
    current_org_id = _get_org_id_by_current_user()
    return get_object_or_404(Organization, pk=current_org_id)

def _get_inventory_by_organization(organization):
    try:
        case_files = CaseFile.objects.filter(organization__id=organization.pk) # pylint: disable=no-member
        return HttpResponse(case_files)
    except:
        return Http404()
    
def _get_org_id_by_current_user():
    # TODO: After the USER model has been created and authorization has been taken care of
    # then we need to go back here and enhance this
    return 1