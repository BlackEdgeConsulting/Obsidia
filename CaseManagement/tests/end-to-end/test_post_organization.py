import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.DTOModels import DTOOrganization
from CaseManagement.models import Organization

class OrganizationModelsPostTestCase(TestCase):
    range_of_entries = range(1,1000)
    fixtures = ["obsidia-fixtures-organization"]

    def setUp(self):
        self.client = Client()

    def test_organization_POST_create_new_org_missing_properties_should_fail(self):
        """Test the cases in which a POST should fail"""
        payloads = [
            {
                "name": "",
                "users": [
                    {
                        "name": "jrykert0",
                        "roleId": 6368
                    }
                ],
                "adminUsers": [
                    {
                        "name": "jrykert0",
                        "roleId": 6368
                    }
                ]
            },
            {
                "name": "SixSixTheBlakRock10009897987",
                "users": [
                    {
                        "name": "jrykert0",
                        "roleId": 6368
                    }
                ],
            }
        ]

        for each_payload in payloads:
            response = self.client.post("/organization/new", data=each_payload, content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            self.assertEqual(response.status_code, 400)

    def test_organization_POST_create_new_org_should_succeed(self):
        """Test that we can adequately post to create a new organization."""
        payloads = [
            {
                "name": "SixSevenTheBlakRock100775",
                "users": [
                    {
                        "name": "jrykert0",
                        "roleId": 6368
                    },
                    {
                        "name": "wfearne1",
                        "roleId": 3684
                    },
                    {
                        "name": "ncouche2",
                        "roleId": 2558
                    }
                ],
                "adminUsers": [
                    {
                        "name": "jrykert0",
                        "roleId": 6368
                    },
                    {
                        "name": "wfearne1",
                        "roleId": 3684
                    },
                    {
                        "name": "ncouche2",
                        "roleId": 2558
                    }
                ]
            },
            {
                "name": "SixSevenTheBlakRock54398",
                "users": [
                    {
                        "name": "ncouche2",
                        "roleId": 2558
                    }
                ],
                "adminUsers": [
                    {
                        "name": "jrykert0",
                        "roleId": 6368
                    },
                    {
                        "name": "ncouche2",
                        "roleId": 2558
                    }
                ]
            },
            {
                "name": "SixSevenTheBlakRock31208",
                "users": [
                    {
                        "name": "jrykert0",
                        "roleId": 6368
                    },
                    {
                        "name": "wfearne1",
                        "roleId": 3684
                    },
                    {
                        "name": "ncouche2",
                        "roleId": 2558
                    }
                ],
                "adminUsers": [
                    {
                        "name": "ncouche2",
                        "roleId": 2558
                    }
                ]
            }
        ]

        for each_payload in payloads:
            response = self.client.post("/organization/new", data=each_payload, content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            self.assertEqual(response.status_code, 201)