from django.db import models

DEFAULT_FIELD_LENGTH = 300

class Organization(models.Model):
    name: str = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    users = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    adminUsers = models.CharField(max_length=DEFAULT_FIELD_LENGTH)
    dateCreated = models.DateTimeField("date created")
    dateLastModified = models.DateTimeField("date last modified")

    def __str__(self) -> str:
        return str(self.name)

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

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        return str(self.fullName)