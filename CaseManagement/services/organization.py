from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from CaseManagement.models import CaseFile, Organization, Tag

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
    def get_casefile_by_tags(cls, requested_tags: list[dict] = []):
        organization = cls._get_current_users_organization()
        # case_files = CaseFile.objects.filter(organization__id=organization.pk, tagSet__key=requested_tags["key"], tagSet__value__contains=requested_tags["value"]) # pylint: disable=no-member
        case_files = CaseFile.objects.filter(
            organization__id=organization.pk,
            tag__key=requested_tags["key"],
            tag__value__contains=requested_tags["value"]
        )
        return HttpResponse(case_files)

    @classmethod
    def get_tag_keys_in_use(cls):
        organization = cls._get_current_users_organization()
        tags = Tag.objects.filter( # pylint: disable=no-member
            casefile__in=CaseFile.objects.filter(organization__id=organization.pk) # pylint: disable=no-member
        ).distinct()
        tag_keys = list(map(lambda t: t.key, tags))
        return HttpResponse(tag_keys)
        
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