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

    def test_organization_POST_create_new_casefile_should_succeed(self):
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