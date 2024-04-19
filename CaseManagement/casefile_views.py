from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from CaseManagement.models import CaseFile
from utils import get_db_handle

# handle, db_client = get_db_handle()

def get_casefile_by_id(request, casefile_id):
    # return HttpResponse(f"Hello, you requested case file OBSID-{casefile_id}\n")
    return get_object_or_404(CaseFile, pk=casefile_id)

def inventory(request):
    return _get_all_casefiles_by_organization()

def _get_all_casefiles_by_organization():
    raise NotImplementedError()