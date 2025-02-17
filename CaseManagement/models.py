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
    dateCreated = models.DateTimeField("date created", auto_now_add=True)
    dateLastModified = models.DateTimeField("date last modified", auto_now=True)

    def __str__(self) -> str:
        # TODO: Make a dictionary containing all the properties on this model listed above
        # and return the json.dumps() of that. e.g. { "name": self.name, ... }
        return json.dumps(self.get_dict())
    
    def get_dto(self) -> DTOOrganization:
        return DTOOrganization(properties=str(self))
    
    @classmethod
    def convert_from_dto(cls, dto: DTOOrganization):
        cls.name = dto.name
        cls.users = dto.users
        cls.adminUsers = dto.adminUsers
        # cls.dateLastModified = models.DateTimeField.auto_now()
        # cls.dateCreated = datetime.now()
        return cls
    
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
    STATUS_INACTIVE = "INACTIVE"
    STATUS_LONGTERM_MONITOR = "LONGTERM MONITOR"
    STATUS_DECEASED = "DECEASED"
    STATUS_PENDING = "PENDING"
    CASE_FILE_STATUS_CHOICES = {
        STATUS_ACTIVE: "Active",
        STATUS_ARCHIVE: "Archive",
        STATUS_LONGTERM_MONITOR: "Longterm Monitor",
        STATUS_DECEASED: "Deceased",
        STATUS_INACTIVE: "Inactive",
        STATUS_PENDING: "Pending"
    }

    caseIdentifier = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField("date created", auto_now_add=True)
    dateLastModified = models.DateTimeField("date last modified", auto_now=True)
    createdBy = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    lastModifiedBy = models.CharField(max_length=DEFAULT_FIELD_LENGTH, blank=True)
    status = models.CharField(
        max_length=20,
        choices=CASE_FILE_STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

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

class TagSet(models.Model):
    casefile = models.OneToOneField(CaseFile, on_delete=models.CASCADE)

class Tag(models.Model):
    key = models.CharField(
        max_length=DEFAULT_FIELD_LENGTH,
    )
    value = models.CharField(
        max_length=DEFAULT_FIELD_LENGTH,
    )
    tagSet = models.ForeignKey(TagSet, on_delete=models.CASCADE)

    def __str__(self):
        return json.dumps({
            "key": str(self.key),
            "value": str(self.value)
        })
    

class TargetOfInterest(models.Model):
    casefile = models.OneToOneField(
        CaseFile,
        on_delete=models.CASCADE
    )
    firstName = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    middleNames = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    lastName = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    fullName = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    additionalNames = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    dateOfBirth = models.DateTimeField("Date of Birth", default="1536-08-26T15:13:46Z")
    currentAddress = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    previousAddresses = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    associatedAddresses = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    targetJustification = models.TextField(max_length=1000, default="")
    socialSecurityNumber = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    driversLicenseNumber = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    governmentIssueId = models.CharField(max_length=DEFAULT_FIELD_LENGTH, default="")
    additionalIdentifications = models.TextField(max_length=DEFAULT_FIELD_LENGTH, default="")

    # TODO: Current task. Fix so the datetime is str
    def __str__(self) -> str:
        return json.dumps(self.get_dict())
    
    def get_dict(self) -> dict:
        return {
            "firstName": str(self.firstName),
            "middleNames": str(self.middleNames),
            "lastName": str(self.lastName),
            "fullName": str(self.fullName),
            "additionalNames": str(self.additionalNames),
            "dateOfBirth": str(self.dateOfBirth),
            "currentAddress": str(self.currentAddress),
            "previousAddresses": str(self.previousAddresses),
            "associatedAddresses": str(self.associatedAddresses),
            "targetJustification": str(self.targetJustification),
            "socialSecurityNumber": str(self.socialSecurityNumber),
            "driversLicenseNumber": str(self.driversLicenseNumber),
            "governmentIssueId": str(self.governmentIssueId),
            "additionalIdentifications": str(self.additionalIdentifications)
        }

