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
        # TODO: Make a dictionary containing all the properties on this model listed above
        # and return the json.dumps() of that. e.g. { "name": self.name, ... }
        return str(self.name)

class Tag(models.Model):
    key = models.CharField(
        max_length=DEFAULT_FIELD_LENGTH,
        unique=True
    )
    value = models.CharField(
        max_length=DEFAULT_FIELD_LENGTH,
    )

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
    dateCreated = models.DateTimeField("date created")
    dateLastModified = models.DateTimeField("date last modified")
    createdBy = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    lastModifiedBy = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    status = models.CharField(
        max_length=20,
        choices=CASE_FILE_STATUS_CHOICES,
        default=STATUS_ACTIVE
    )
    caseIdentifier = models.CharField(max_length=DEFAULT_FIELD_LENGTH)

    # TODO: Make a dictionary containing all the properties on this model listed above
        # and return the json.dumps() of that. e.g. { "name": self.name, ... }
    def __str__(self) -> str:
        # TODO: This isn't a great way to do it. Example of identifier `OBSID-0001` with this:
        # OBSID-00012024-04-19 21:02:50+00:00
        return str(self.caseIdentifier) + str(self.dateCreated)

class TargetOfInterest(models.Model):
    casefile = models.OneToOneField(
        CaseFile,
        on_delete=models.CASCADE
    )
    firstName = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    middleNames = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    lastName = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    fullName = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    additionalNames = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    dateOfBirth = models.DateTimeField("Date of Birth")
    currentAddress = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    previousAddresses = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    associatedAddresses = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    targetJustification = models.TextField(max_length=1000)
    socialSecurityNumber = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    driversLicenseNumber = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    governmentIssueId = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    additionalIdentifications = models.TextField(max_length=DEFAULT_FIELD_LENGTH)

    # TODO: Make a dictionary containing all the properties on this model listed above
    # and return the json.dumps() of that. e.g. { "name": self.name, ... }
    def __str__(self) -> str:
        return str(self.fullName)