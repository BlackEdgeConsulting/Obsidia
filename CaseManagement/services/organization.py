import json
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from CaseManagement.DTOModels import DTOOrganization, DTOCaseFile
from CaseManagement.models import CaseFile, Organization
from CaseManagement.services.casefile import CaseFileService

class OrganizationService():
    @classmethod
    def get_current_organization(cls):
        result = cls._get_current_users_organization()
        return HttpResponse(result) if result is not None else Http404
    
    @classmethod
    def get_current_organization_id(cls):
        result = cls._get_org_id_by_current_user()
        return HttpResponse(result) if result is not None else Http404
    
    @classmethod
    def create_new_organization(cls, request):
        try:
            new_organization = cls._create_new_organization(request)
            new_organization.save()
        except:
            return HttpResponse("Failed to create new organization!", status=400)
        return HttpResponse("Created the new organization!", status=201)

    @classmethod
    def get_organization_by_id(cls, org_id):
        # return HttpResponse(f"You requested Organization ORG-{org_id}")
        result = cls._get_organization_by_id(org_id)
        return HttpResponse(result) if result is not None else Http404()

    
    # FIXME: The casefile and tags inventory needs unified such that they can be easily converted into loaded JSON or dumped to Json string
    @classmethod
    def get_all_inventory(cls):
        organization = cls._get_current_users_organization()
        result = json.dumps({
            "organization": {
                organization.name: {
                    "properties": json.loads(str(organization)),
                    "inventory": {
                        # "tags_inventory": cls._get_tag_keys_in_use(),
                        "casefile_inventory": list(map(lambda c: json.loads(str(c)), list(CaseFileService.get_casefile(current_organization_id=organization.pk))))
                    }
                } 
            }
        })
        return HttpResponse(result) if result is not None else Http404()
    
    @classmethod
    def casefile_inventory(cls):
        organization = cls._get_current_users_organization()
        result: list[CaseFile] = CaseFileService.get_casefile(current_organization_id=organization.pk)
        return HttpResponse(result) if result is not None else Http404()

    # @classmethod
    # def get_tag_keys_in_use(cls):
    #     tag_keys = cls._get_tag_keys_in_use()
    #     return HttpResponse(tag_keys)
    
    @classmethod
    def _get_organization_by_id(cls, org_id):
        try:
            organization = get_object_or_404(Organization, pk=org_id)
            if isinstance(organization, Organization):
                dto_organization: DTOOrganization = DTOOrganization(properties=str(organization))
                clean_dto_org: str = str(dto_organization)
                return clean_dto_org
            else:
                return None
        except:
            return None
    
    @classmethod
    def _create_new_organization(cls, request):
        decoded_request = request.body.decode("UTF-8")
        dto_org = DTOOrganization(properties=decoded_request)
        return Organization(
            name=dto_org.name,
            users=dto_org.users,
            adminUsers=dto_org.adminUsers
        )

    @classmethod
    def _get_current_users_organization(cls):
        current_org_id = cls._get_org_id_by_current_user()
        return get_object_or_404(Organization, pk=current_org_id)
    
    @classmethod
    def _get_org_id_by_current_user(cls):
        # TODO: After the USER model has been created and authorization has been taken care of
        # then we need to go back here and enhance this
        return 1
    
    # @classmethod
    # def _get_tag_keys_in_use(cls):
    #     organization = cls._get_current_users_organization()
    #     tags = Tag.objects.filter( # pylint: disable=no-member
    #         casefile__in=CaseFile.objects.filter(organization__id=organization.pk) # pylint: disable=no-member
    #     ).distinct()
    #     tag_keys = list(map(lambda t: t.key, tags))
    #     return tag_keys