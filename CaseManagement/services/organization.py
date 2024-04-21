from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from CaseManagement.models import CaseFile, Organization

class OrganizationService():
    @classmethod
    def current_organization(cls):
        return HttpResponse("Hello, world. You're in the DEFAULT organization\n")
    
    @classmethod
    def create_new_organization(cls, request):
        return HttpResponse("Created the new organization!")

    @classmethod
    def get_organization_by_id(cls, org_id):
        # return HttpResponse(f"You requested Organization ORG-{org_id}")
        orginization = get_object_or_404(Organization, pk=org_id)
        return HttpResponse(orginization)

    @classmethod
    def get_casefile_by_id(cls, casefile_id):
        organization = cls._get_current_users_organization()
        casefile = CaseFile.objects.filter(pk=casefile_id, organization__id=organization.pk) # pylint: disable=no-member
        return HttpResponse(casefile)
        
    @classmethod
    def inventory(cls):
        organization = cls._get_current_users_organization()
        return cls._get_inventory_by_organization(organization)

    @classmethod
    def _get_current_users_organization(cls):
        current_org_id = cls._get_org_id_by_current_user()
        return get_object_or_404(Organization, pk=current_org_id)

    @classmethod
    def _get_inventory_by_organization(cls, organization):
        try:
            case_files = CaseFile.objects.filter(organization__id=organization.pk) # pylint: disable=no-member
            return HttpResponse(case_files)
        except:
            return Http404()
    
    @classmethod
    def _get_org_id_by_current_user(cls):
        # TODO: After the USER model has been created and authorization has been taken care of
        # then we need to go back here and enhance this
        return 1