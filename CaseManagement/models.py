import json
import random
import uuid
from django.db import models
from datetime import datetime
from CaseManagement.DTOModels import DTOOrganization, DTOCaseFile

DEFAULT_FIELD_LENGTH = 300

class Organization(models.Model):
    name: str = models.CharField(max_length=DEFAULT_FIELD_LENGTH, unique=True)
    users = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    adminUsers = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    dateCreated = models.DateTimeField("date created")
    dateLastModified = models.DateTimeField("date last modified")

    def __str__(self) -> str:
        # TODO: Make a dictionary containing all the properties on this model listed above
        # and return the json.dumps() of that. e.g. { "name": self.name, ... }
        return json.dumps(self.get_dict())
    
    def get_dto(self) -> DTOOrganization:
        return DTOOrganization(properties=str(self))
    
    def get_dict(self) -> dict:
        return {
            "name": str(self.name),
            "users": str(self.users),
            "adminUsers": str(self.adminUsers),
            "dateCreated": str(self.dateCreated),
            "dateLastModified": str(self.dateLastModified)
        }

class CaseFile(models.Model):
    STATUS_ACTIVE = "ACTIVE"
    STATUS_ARCHIVE = "ARCHIVE"
    STATUS_LONGTERM_MONITOR = "LONGTERM MONITOR"
    STATUS_DECEASED = "DECEASED"
    CASE_FILE_STATUS_CHOICES = {
        STATUS_ACTIVE: "Active",
        STATUS_ARCHIVE: "Archive",
        STATUS_LONGTERM_MONITOR: "Longterm Monitor",
        STATUS_DECEASED: "Deceased"
    }

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField("date created", blank=True)
    dateLastModified = models.DateTimeField("date last modified", blank=True)
    createdBy = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    lastModifiedBy = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    status = models.CharField(
        max_length=20,
        choices=CASE_FILE_STATUS_CHOICES,
        default=STATUS_ACTIVE
    )
    caseIdentifier = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)

    def __str__(self) -> str:
        return json.dumps(self.get_dict())
    
    def get_dict(self) -> dict:
        return {
            "caseIdentifier": str(self.caseIdentifier),
            "organization": json.loads(str(self.organization)),
            "dateCreated": str(self.dateCreated),
            "dateLastModified": str(self.dateLastModified),
            "createdBy": str(self.createdBy),
            "status": str(self.status)
        }
    
    def get_dto(self) -> DTOOrganization:
        return DTOCaseFile(properties=str(self))

# class Tag(models.Model):
#     key = models.CharField(
#         max_length=DEFAULT_FIELD_LENGTH,
#     )
#     value = models.CharField(
#         max_length=DEFAULT_FIELD_LENGTH,
#     )
#     # casefile = models.ForeignKey("CaseFile", on_delete=models.CASCADE, default=CaseFile.get_default_pk)
#     casefile = models.ForeignKey("CaseFile",    
#                        on_delete=models.CASCADE,
#                        default=get_sentinel_casefile_id
#                  )
    
#     def __str__(self):
#         return json.dumps({
#             "key": str(self.key),
#             "value": str(self.value)
#         })

class TargetOfInterest(models.Model):
    casefile = models.OneToOneField(
        CaseFile,
        on_delete=models.CASCADE
    )
    firstName = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    middleNames = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    lastName = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    fullName = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    additionalNames = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    dateOfBirth = models.DateTimeField("Date of Birth", blank=True)
    currentAddress = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    previousAddresses = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    associatedAddresses = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    targetJustification = models.TextField(max_length=1000, blank=True)
    socialSecurityNumber = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    driversLicenseNumber = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    governmentIssueId = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    additionalIdentifications = models.TextField(max_length=DEFAULT_FIELD_LENGTH, blank=True)

    # TODO: Make a dictionary containing all the properties on this model listed above
    # and return the json.dumps() of that. e.g. { "name": self.name, ... }
    def __str__(self) -> str:
        return str(self.fullName)
