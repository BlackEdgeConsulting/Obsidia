# Release Notes

## v0.01
This adds all the basic functionality for creating and reading Organizations and Casefiles. The following functionalities are available by their corresponding API endpoint

### Organization
#### Reading
- Reading a single Organization by it's ID.
`curl --location "<address>/organization/{ID}"`

- Reading current user's Organization (no auth in place yet)  
`curl --location "<address>/organization/"`

- Read current Organization's inventory, e.g. Casefiles, Tags, Organization, etc.  
`curl --location "<address>/organization/inventory"`

- Read current Organization's inventory of tag keys in use, useful for searching.  
`curl --location "<address>/organization/inventory/tags"`

#### Creating
- Create a new Organization
```sh
# Create new organization
curl --location '<address>/organization/new' \
--header 'Content-Type: application/json' \
--data '{
    "name": "someOrg",
    "users": [
        "someUser"
    ],
    "adminUsers": [
        "someUser"
    ]
}'
```

### CaseFile
#### Reading


#### Creating
- Create a new CaseFile
```sh
# Create new CaseFile
curl --location '<address>/organization/casefile' \
--header 'Content-Type: application/json' \
--data '{
    "caseIdentifier": "asd213ewae21easd321321321312",
    "organization": 1,
    "status": "ARCHIVE"
}'

# Create new CaseFile with partial target
curl --location '<address>/organization/casefile' \
--header 'Content-Type: application/json' \
--data '{
    "caseIdentifier": "asd213ewae21easd321321321312",
    "organization": 1,
    "status": "ARCHIVE"
    "targetOfInterest": {
        "firstName": "",
        "lastName": "",
        "dateOfBirth": "",
        "targetJustification": ""
    }
}'

# Create new CaseFile with full target
curl --location '<address>/organization/casefile' \
--header 'Content-Type: application/json' \
--data '{
    "caseIdentifier": "asd213ewae21easd321321321312",
    "organization": 1,
    "status": "ARCHIVE"
    "targetOfInterest": {
        "firstName": "",
        "middleNames": "",
        "lastName": "",
        "fullName": "",
        "additionalNames": "",
        "dateOfBirth": "",
        "currentAddress": "",
        "previousAddresses": [],
        "associatedAddresses": [],
        "targetJustification": "",
        "socialSecurityNumber": "",
        "driversLicenseNumber": "",
        "governmentIssueId": "",
        "additionalIdentifications": ""
    }
}'
```