import json
from django.http import HttpResponse
from CaseManagement.DTOModels import DTOCaseFile
from CaseManagement.models import CaseFile, Organization, TagSet, Tag, TargetOfInterest

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
                for each_casefile in list(casefiles):
                    dto = DTOCaseFile(properties=str(each_casefile))
                    try:
                        targetOfInterest = TargetOfInterest.objects.get(casefile=each_casefile)
                        dto.targetOfInterest = str(targetOfInterest)
                    except:
                        raise Exception("Failed to build Target of Interest")
                    result.append(str(dto))
            else:
                return result
        elif requested_tags:
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
                result.append(str(dto))

        return result
    
    @classmethod
    def create_new_casefile(cls, request):
        try:
            try:
                decoded_request: str = request.body.decode("UTF-8")
                loaded_request: dict = json.loads(decoded_request) # Simply try to interpret it before moving on
            except:
                decoded_request: str = json.dumps({})
            new_casefile = cls._create_new_casefile(decoded_request=decoded_request)            
        except:
            return HttpResponse("Failed to create new casefile!", status=400)
        return HttpResponse("Created the new casefile!", status=201)
    
    @classmethod
    def _create_new_casefile(cls, decoded_request) -> CaseFile:
        dto_casefile = DTOCaseFile(properties=decoded_request)
        org = Organization.objects.get(pk=dto_casefile.organization)

        new_casefile = CaseFile(
            organization=org,
            caseIdentifier=dto_casefile.caseIdentifier,
            status=dto_casefile.status
        )
        try:
            new_casefile.save()
        except:
            return HttpResponse("Failed to save the new casefile! Invalid casefile request", status=400)
        

        new_target = cls._create_new_target(new_casefile_id=new_casefile.pk, casefile_dto=dto_casefile)
        try:
            new_target.save()
        except:
            return HttpResponse("Failed to save the target! Invalid tagset request", status=400)

        new_tagset = cls._create_new_tagset(casefile_id=new_casefile.pk)
        try:
            new_tagset.save()
        except:
            return HttpResponse("Failed to save the tagset! Invalid tagset request", status=400)

        if dto_casefile.tags is not None and isinstance(dto_casefile.tags, list) and len(dto_casefile.tags) > 0:
            new_tags: list = cls._create_new_tags(new_tagset.pk, dto_casefile.tags)
            try:
                if isinstance(new_tags, list) and len(new_tags) > 0:
                    map(lambda t: t.save(), new_tags)
                else:
                    raise Exception("Failed to save tags to Database")
            except:
                return HttpResponse("Failed to save the new tags! Invalid tag request", status=400)

        return new_casefile

    @classmethod
    def _create_new_target(cls, new_casefile_id: int, casefile_dto: DTOCaseFile):
        # FIXME: Sometimes the DoB ends up as `None` and the db doesn't like that.
        # Need to fix it
        casefile = CaseFile.objects.get(pk=new_casefile_id)
        target_properties = casefile_dto.targetOfInterest
        return TargetOfInterest(casefile=casefile, **target_properties)
    
    @classmethod
    def _create_new_tagset(cls, casefile_id):
        casefile = CaseFile.objects.get(pk=casefile_id)
        return TagSet(
            casefile=casefile
        )

    @classmethod
    def _create_new_tags(cls, tagset_id: int, tags):
        tagSet = TagSet.objects.get(pk=tagset_id)
        tag_objects = []
        for each_tag in tags:
            tag_objects.append(
                Tag(
                    key=each_tag["key"],
                    value=each_tag["value"],
                    tagSet=tagSet
                )
            )
        return tag_objects
    
    @classmethod
    def _get_casefile_by_id(cls, casefile_id: int|str, organization_id: int|str) -> list|None:
        casefiles = CaseFile.objects.filter(pk=casefile_id, organization__id=organization_id) # pylint: disable=no-member
        if len(casefiles) > 0:
            return casefiles
        else:
            return None
        
    @classmethod
    def _get_casefile_by_tags(cls, organization_id, requested_tags: list[dict] = []):
        case_files: str = CaseFile.objects.filter(
            organization__id=organization_id,
            tagset__tag__key=requested_tags["key"],
            tagset__tag__value__icontains=requested_tags["value"]
        )
        if len(case_files) > 0:
            dto_result = []
            for each_casefile in list(case_files):
                tags = Tag.objects.filter(
                    tagSet__casefile=each_casefile
                )
                dto = DTOCaseFile(properties=str(each_casefile))
                dto.tags = list(map(lambda t: json.loads(str(t)),tags))
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