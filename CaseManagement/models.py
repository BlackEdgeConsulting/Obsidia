import json
from django.db import models

DEFAULT_FIELD_LENGTH = 300

class Organization(models.Model):
    name: str = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    users = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    adminUsers = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    dateCreated = models.DateTimeField("date created")
    dateLastModified = models.DateTimeField("date last modified")
    

    def __str__(self) -> str:
        organization_properties = {
            "name" : self.name,
            "users" : self.users,
            "adminUsers" : self.adminUsers,
            "dateCreated" : self.dateCreated,
            "dateLastModified" : self.dateLastModified
        }   

        return json.dumps(organization_properties)


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

    @classmethod
    def get_default_pk(cls):
        tag, created = cls.objects.get_or_create( # pylint: disable=no-member
            organization=1, 
            defaults=dict(dateCreated="1111-12-16 22:12", dateLastModified="1111-12-16 22:12", createdBy="None", lastModifiedBy="None", caseIdentifier="None"),
        )
        return tag.pk
        
    # TODO: ASK CHUCK ABOUT THIS ONE. Make a dictionary containing all the properties on this model listed above
        # and return the json.dumps() of that. e.g. { "name": self.name, ... }
    def __str__(self) -> str:
        # TODO: AND THIS ONE This isn't a great way to do it. Example of identifier `OBSID-0001` with this:
        # OBSID-00012024-04-19 21:02:50+00:00
        return json.dumps(case_file_dictionary)

class Tag(models.Model):
    key = models.CharField(
        max_length=DEFAULT_FIELD_LENGTH,
    )
    value = models.CharField(
        max_length=DEFAULT_FIELD_LENGTH,
    )
    casefile = models.ForeignKey("CaseFile", on_delete=models.CASCADE, default=CaseFile.get_default_pk)

    @classmethod
    def get_default_pk(cls):
        tag, created = cls.objects.get_or_create( # pylint: disable=no-member
            key="name", 
            defaults=dict(key="name", value=""),
        )
        return tag.pk
    
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

    def __str__(self) -> str:

        target_properties = {
            "firstname": self.firstName ,
            "middleNames": self.middleNames ,
            "lastName":self.lastName , 
            "fullName":self.fullName ,
            "additionalNames": self.additionalNames ,
            "dateOfBirth": self.dateOfBirth ,
            "currentAddress": self.currentAddress , 
            "previousAddress": self.previousAddresses ,
            "associatedAddresses": self.associatedAddresses , 
            "targetJustification": self.targetJustification , 
            "socialSecurityNumber": self.socialSecurityNumber , 
            "driversLicenseNumber": self.driversLicenseNumber , 
            "governmentIssueId": self.governmentIssueId ,
            "additionalIdentifications": self.additionalIdentifications
        }


        return json.dumps(target_properties)
