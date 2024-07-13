import json
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from CaseManagement.DTOModels import DTOOrganization, DTOCaseFile
from CaseManagement.models import CaseFile, Organization

class CaseFileService():
    @classmethod
    def get_casefile(cls, **kwargs):
        casefile_id: int = kwargs.get("casefile_id")
        organization_id: int = kwargs.get("current_organization_id")
        requested_tags: dict = kwargs.get("requested_tags")
        result = []
        if casefile_id:
            # If there's an ID then we only get one
            casefiles: list[CaseFile] = cls._get_casefile_by_id(casefile_id, organization_id)
            if casefiles is not None:
                # dto_result: list[DTOCaseFile] = []
                for each_casefile in list(casefiles):
                    dto = DTOCaseFile(properties=str(each_casefile))
                    result.append(str(dto))
                    # dto_result.append(dto)

                # result.append(*(list(map(lambda c: str(c), dto_result))))
            else:
                return result
        elif requested_tags:
            # TODO: Refactor, if there's tags then we get it by tags
            # requested_tags = {
            #     "key": "name",
            #     "value": "OBSID"
            # }
            casefiles = cls._get_casefile_by_tags(organization_id=organization_id, requested_tags=requested_tags)
            if casefiles is not None:
                result.append(*(list(map(lambda c: str(c), casefiles))))
            else:
                return None
        else:
            # If there's no specifier then we get all the casefiles in the org
            casefiles: list[CaseFile] = cls._get_casefile_inventory_by_organization(organization_id)
            if casefiles is None or len(casefiles) == 0:
                return result
            
            for each_casefile in casefiles:
                dto = DTOCaseFile(properties=str(each_casefile))
                # dto_result.append(dto)
                result.append(str(dto))

            # result.append(*(list(map(lambda c: str(c), dto_result))))

        return result
    
    @classmethod
    def create_new_casefile(cls, request):
        try:
            new_casefile = cls._create_new_casefile(request)
            new_casefile.save()
        except:
            return HttpResponse("Failed to create new casefile!", status=400)
        return HttpResponse("Created the new casefile!", status=201)
    
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
    def _get_casefile_by_id(cls, casefile_id: int|str, organization_id: int|str) -> list|None:
        casefiles = CaseFile.objects.filter(pk=casefile_id, organization__id=organization_id) # pylint: disable=no-member
        if len(casefiles) > 0:
            # dto_result = []
            # for each_casefile in list(casefiles):
            #     dto = DTOCaseFile(properties=str(each_casefile))
            #     dto_result.append(dto)

            # return dto_result
            return casefiles
        else:
            return None
        
    @classmethod
    def _get_casefile_by_tags(cls, organization_id, requested_tags: list[dict] = []):
        # case_files = CaseFile.objects.filter(organization__id=organization.pk, tagSet__key=requested_tags["key"], tagSet__value__contains=requested_tags["value"]) # pylint: disable=no-member
        case_files: str = CaseFile.objects.filter(
            organization__id=organization_id,
            tagset__tag__key=requested_tags["key"],
            tagset__tag__value__icontains=requested_tags["value"]
        )
        if len(case_files) > 0:
            dto_result = []
            for each_casefile in list(case_files):
                dto = DTOCaseFile(properties=str(each_casefile))
                dto_result.append(dto)

            return dto_result
        else:
            return None
        
    @classmethod
    def _get_casefile_inventory_by_organization(cls, organization_id):
        try:
            return CaseFile.objects.filter(organization__id=organization_id) # pylint: disable=no-member
        except:
            return None