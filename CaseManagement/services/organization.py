import json
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from CaseManagement.DTOModels import DTOOrganization, DTOCaseFile
from CaseManagement.models import CaseFile, Organization

class OrganizationService():
    @classmethod
    def current_organization(cls):
        return "Hello, world. You're in the DEFAULT organization\n"
    
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
    
    @classmethod
    def get_casefile(cls, **kwargs):
        casefile_id = kwargs.get("casefile_id")
        result = []
        if casefile_id:
            casefiles = OrganizationService._get_casefile_by_id(casefile_id)
            if casefiles is not None:
                result.append(*(list(map(lambda c: str(c), casefiles))))
            else:
                return None
        else:
            requested_tags = {
                "key": "name",
                "value": "OBSID"
            }
            # TODO: Refactor
            casefiles = cls._get_casefile_by_tags(requested_tags)
            if casefiles is not None:
                result.append(*(list(map(lambda c: str(c), casefiles))))
            else:
                return None
        return result
    
    @classmethod
    def create_new_casefile(cls, request):
        try:
            new_casefile = cls._create_new_casefile(request)
            new_casefile.save()
        except:
            return HttpResponse("Failed to create new casefile!", status=400)
        return HttpResponse("Created the new casefile!", status=201)
    
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
                        "casefile_inventory": list(map(lambda c: json.loads(str(c)), list(cls._get_casefile_inventory_by_organization(organization))))
                    }
                } 
            }
        })
        return HttpResponse(result)
        
    @classmethod
    def casefile_inventory(cls):
        organization = cls._get_current_users_organization()
        result = cls._get_casefile_inventory_by_organization(organization)
        return HttpResponse(result) if result is not None else Http404()
    
    @classmethod
    def _create_new_casefile(cls, request) -> CaseFile:
        decoded_request = request.body.decode("UTF-8")
        dto_casefile = DTOCaseFile(properties=decoded_request)
        org = Organization.objects.get(pk=dto_casefile.organization)
        return CaseFile(
            caseIdentifier=dto_casefile.caseIdentifier,
            organization=org,
            status=dto_casefile.status
        )
    
    @classmethod
    def _get_casefile_by_id(cls, casefile_id) -> list|None:
        organization = cls._get_current_users_organization()
        casefiles = CaseFile.objects.filter(pk=casefile_id, organization__id=organization.pk) # pylint: disable=no-member
        if len(casefiles) > 0:
            dto_result = []
            for each_casefile in list(casefiles):
                dto = DTOCaseFile(properties=str(each_casefile))
                dto_result.append(dto)

            return dto_result
        else:
            return None
    
    @classmethod
    def _get_casefile_by_tags(cls, requested_tags: list[dict] = []):
        organization = cls._get_current_users_organization()
        # case_files = CaseFile.objects.filter(organization__id=organization.pk, tagSet__key=requested_tags["key"], tagSet__value__contains=requested_tags["value"]) # pylint: disable=no-member
        case_files: str = CaseFile.objects.filter(
            organization__id=organization.pk,
            tag__key=requested_tags["key"],
            tag__value__contains=requested_tags["value"]
        )
        if len(case_files) > 0:
            dto_result = []
            for each_casefile in list(case_files):
                dto = DTOCaseFile(properties=str(each_casefile))
                dto_result.append(dto)

            return dto_result
        else:
            return None

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
    def _get_casefile_inventory_by_organization(cls, organization):
        try:
            return CaseFile.objects.filter(organization__id=organization.pk) # pylint: disable=no-member
        except:
            return None
    
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