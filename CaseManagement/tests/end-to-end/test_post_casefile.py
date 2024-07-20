import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.DTOModels import DTOOrganization
from CaseManagement.models import Organization, CaseFile

class OrganizationModelsPostTestCase(TestCase):
    range_of_entries = range(1,1000)
    fixtures = ["obsidia-fixtures-organization"]

    def setUp(self):
        self.client = Client()

    def test_organization_POST_create_new_casefile_missing_properties_should_fail(self):
        """Test the cases in which a Casefile POST should fail"""
        payloads = [
            {
                "caseIdentifier": "",
                "organization": 1
            },
            {
                "caseIdentifier": "asdqweasdqw123213",
                "organization": None
            },
            {
                "caseIdentifier": None,
                "organization": 2
            },
        ]

        for each_payload in payloads:
            response = self.client.post("/organization/new", data=each_payload, content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            self.assertEqual(response.status_code, 400)

    def test_organization_POST_create_new_casefile_BASIC_should_succeed(self):
        """Test that we can adequately post to create a new organization."""
        payloads = [
            {
                "caseIdentifier": "asdgadfdst3423e123eewqq",
                "organization": 1
            },
            {
                "caseIdentifier": "asd234ewqe1234rsarqweasd",
                "organization": 2
            },
            {
                "caseIdentifier": "asd213ewae21easd",
                "organization": 2,
                "status": "ACTIVE"                
            },
            {
                "caseIdentifier": "asd213ewae21easd321321321312",
                "organization": 2,
                "status": "ARCHIVE"                
            },
            {
                "caseIdentifier": "awrdshgdjggd123",
                "organization": 2,
                "status": "LONGTERM MONITOR"                
            },
            {
                "caseIdentifier": "awrdshgdjggd2ewq211asd123",
                "organization": 2,
                "status": "DECEASED"                
            },
        ]

        for each_payload in payloads:
            response = self.client.post("/organization/casefile", data=each_payload, content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            self.assertEqual(response.status_code, 201)

    def test_casefile_POST_casefile_by_index_should_fail(self):
        for each_casefile_id in range(1,100):
            response = self.client.post(f"/organization/casefile/{each_casefile_id}")
            self.assertEqual(response.status_code, 400)

    def test_casefile_POST_casefile_all_should_fail(self):
        response = self.client.post(f"/organization/inventory/casefile")
        self.assertEqual(response.status_code, 404)

    def test_casefile_POST_casefile_with_tags(self):
        payloads = [
            {
                "caseIdentifier": "oiadf8739lk",
                "organization": 1,
                "tags": [
                    {
                        "key": "something",
                        "value": "asdh76"
                    }
                ]
            },
            {
                "caseIdentifier": "ojdsf973rhiohifh",
                "organization": 1,
                "status": "ACTIVE",
                "tags": [
                    {
                        "key": "something",
                        "value": "asdh76"
                    },
                    {
                        "key": "somethingElse",
                        "value": "ihsdf7893"
                    }
                ]
            },
        ]

        for each_payload in payloads:
            response = self.client.post("/organization/casefile", data=each_payload, content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content.decode("UTF-8"), "Created the new casefile!")
        

    def test_casefile_POST_casefile_with_full_and_partial_target(self):
        payloads = [
            {
                "name": "test with full target",
                "payload": {
                    "caseIdentifier": "ojdsf973rhiohifh",
                    "organization": 1,
                    "status": "ACTIVE",
                    "tags": [
                        {
                            "key": "something",
                            "value": "asdh76"
                        },
                        {
                            "key": "somethingElse",
                            "value": "ihsdf7893"
                        }
                    ],
                    "targetOfInterest": {
                        "firstName": "Abby",
                        "middleNames": "Ethelbert",
                        "lastName": "Luthwood",
                        "fullName": "Ethelbert Luthwood",
                        "additionalNames": "vestibulum rutrum rutrum neque aenean auctor gravida sem praesent id massa id",
                        "dateOfBirth": "1977-09-28T07:44:46Z",
                        "currentAddress": "39913 Charing Cross Point",
                        "previousAddresses": [
                            "39233 Charing Cross Point"
                        ],
                        "associatedAddresses": [
                            "39913 Charing Cross Point",
                            "39233 Charing Cross Point"
                        ],
                        "targetJustification": "In congue. Etiam justo. Etiam pretium iaculis justo.\n\nIn hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus.\n\nNulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi.",
                        "socialSecurityNumber": "114-41-3171",
                        "driversLicenseNumber": "DL654321",
                        "governmentIssueId": "ID987654",
                        "additionalIdentifications": "tortor id nulla ultrices aliquet maecenas leo odio condimentum",
                    }
                },
                "expect": {}
            },
            {
                "name": "test w/ Partial Target",
                "payload": {
                    "caseIdentifier": "qwioklasjdo973",
                    "organization": 1,
                    "status": "ACTIVE",
                    "tags": [
                        {
                            "key": "something",
                            "value": "asdh76"
                        }
                    ],
                    "targetOfInterest": {
                        "firstName": "Abby",
                        "middleNames": "Kary",
                        "lastName": "Prowting",
                        "previousAddresses": ["8065 Carberry Center"],
                        "targetJustification": "Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio.\n\nCras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
                        "additionalIdentifications": "accumsan felis"
                    }
                },
                "expect": {}
            }
        ]

        for each_payload in payloads:
            response = self.client.post(
                "/organization/casefile",
                data=each_payload["payload"],
                content_type="application/json",
                HTTP_X_REQUESTED_WITH="XMLHttpRequest"
            )
            posted_casefile = CaseFile.objects.get(caseIdentifier=each_payload["payload"]["caseIdentifier"])
            self.assertEqual(response.content.decode("UTF-8"), "Created the new casefile!")
            self.assertEqual(response.status_code, 201)

    def test_casefile_POST_casefile_with_no_correct_properties(self):
        payloads = [
            {
                "name": "test with full target",
                "payload": {
                    "caseIdentifier": "ojdsf973rhiohifh",
                    "organization": 1,
                    "status": "ACTIVE",
                    "tags": [
                        {
                            "key": "something",
                            "value": "asdh76"
                        },
                        {
                            "key": "somethingElse",
                            "value": "ihsdf7893"
                        }
                    ],
                    "targetOfInterest": {
                        "FirStName": "Abby",
                        "miDDlENames": "Ethelbert",
                        "last": "Luthwood",
                        "fUlMAne": "Ethelbert Luthwood",
                        "adDDitionalNames": "vestibulum rutrum rutrum neque aenean auctor gravida sem praesent id massa id",
                        "DoB": "1977-09-28T07:44:46Z",
                        "curRent": "39913 Charing Cross Point",
                        "previusAddresses": [
                            "39233 Charing Cross Point"
                        ],
                        "associasastedAddresses": [
                            "39913 Charing Cross Point",
                            "39233 Charing Cross Point"
                        ],
                        "targetJustifasdffication": "In congue. Etiam justo. Etiam pretium iaculis justo.\n\nIn hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus.\n\nNulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi.",
                        "sociaa2aslSecurityNumber": "114-41-3171",
                        "driversLidasdcenseNumber": "DL654321",
                        "governmentIsfasdsueId": "ID987654",
                        "additionaasdasfdflIdentifications": "tortor id nulla ultrices aliquet maecenas leo odio condimentum",
                    }
                },
            }
        ]

        for each_payload in payloads:
            response = self.client.post(
                "/organization/casefile",
                data=each_payload["payload"],
                content_type="application/json",
                HTTP_X_REQUESTED_WITH="XMLHttpRequest"
            )
            self.assertEqual(response.status_code, 400)