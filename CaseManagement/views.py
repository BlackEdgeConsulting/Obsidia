from enum import Enum
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from CaseManagement.services.organization import OrganizationService
from utils import get_db_handle

class ValidHttpType(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

def handle_organization_landing(request):
    if request.method == ValidHttpType.GET.name:
        return OrganizationService.current_organization()
    else:
        return HttpResponseNotAllowed([ValidHttpType.GET.name])
    

@csrf_exempt
def handle_organization_new(request):
    if request.method == ValidHttpType.POST.name:
        return OrganizationService.create_new_organization(request)
    else:
        return HttpResponseNotAllowed([ValidHttpType.POST.name])

def handle_organization_by_index(request, **kwargs):
    if request.method == ValidHttpType.GET.name:
        return OrganizationService.get_organization_by_id(kwargs.get("org_id"))
    return HttpResponseNotAllowed([ValidHttpType.GET.name])
    
def handle_casefile_inventory(request, **kwargs):
    if request.method == ValidHttpType.GET.name:
        return OrganizationService.inventory()
    return HttpResponseNotAllowed([ValidHttpType.GET.name])

def handle_tags_inventory(request, **kwargs):
    if request.method == ValidHttpType.GET.name:
        return OrganizationService.get_tag_keys_in_use()
    return HttpResponseNotAllowed([ValidHttpType.GET.name])

def handle_casefile(request, **kwargs):
    if request.method == ValidHttpType.GET.name:
        casefile_id = kwargs.get("casefile_id")
        if casefile_id:
            return OrganizationService.get_casefile_by_id(casefile_id)
        else:
            requested_tags = {
                "key": "name",
                "value": "OBSID"
            }
            return OrganizationService.get_casefile_by_tags(requested_tags)
    elif request.method == ValidHttpType.POST.name:
        pass
    return HttpResponseNotAllowed([ValidHttpType.GET.name, ValidHttpType.POST.name])