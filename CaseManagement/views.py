from enum import Enum
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from CaseManagement.services.casefile import CaseFileService
from CaseManagement.services.validators import Validators
from CaseManagement.services.organization import OrganizationService
from utils import get_db_handle

class ValidHttpType(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

def handle_organization_landing(request):
    if request.method == ValidHttpType.GET.name:
        return HttpResponse(OrganizationService.get_current_organization())
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

def handle_organization_inventory(request, **kwargs):
    if request.method == ValidHttpType.GET.name:
        return OrganizationService.get_all_inventory()
    return HttpResponseNotAllowed([ValidHttpType.GET.name])
    
def handle_casefile_inventory(request, **kwargs):
    if request.method == ValidHttpType.GET.name:
        querydict = dict(request.GET)
        casefiles = _handle_get_by_tags(querydict)
        if casefiles is not None:
            return casefiles
        
        return OrganizationService.casefile_inventory()
    return HttpResponseNotAllowed([ValidHttpType.GET.name])

def handle_tags_inventory(request, **kwargs):
    if request.method == ValidHttpType.GET.name:
        return OrganizationService.get_tag_keys_in_use()
    return HttpResponseNotAllowed([ValidHttpType.GET.name])

def handle_casefile(request, **kwargs):
    if request.method == ValidHttpType.GET.name:
        kwargs["current_organization_id"] = OrganizationService.get_current_organization_id().content.decode("UTF-8")
        casefile: str = CaseFileService.get_casefile(**kwargs)
        if casefile is not None:
            return HttpResponse(casefile)
        else:
            return Http404()
    elif request.method == ValidHttpType.POST.name:
        return CaseFileService.create_new_casefile(request)
    return HttpResponseNotAllowed([ValidHttpType.GET.name, ValidHttpType.POST.name])

def _handle_get_by_tags(querydict):
    if len(list(querydict.items())) > 0:
        if Validators.is_valid_tag(querydict):
            querydict["key"] = querydict["key"][0] if isinstance(querydict["key"], list) else querydict["key"]
            querydict["value"] = querydict["value"][0] if isinstance(querydict["value"], list) else querydict["value"]
            return OrganizationService.casefile_inventory(requested_tags=querydict)
        else:
            return HttpResponse("Invalid tag was supplied.", status=400)
    else:
        return None