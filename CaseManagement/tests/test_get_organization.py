import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.DTOModels import DTOOrganization
from CaseManagement.models import Organization



class OrganizationModelsTestCase(TestCase):
    range_of_entries = range(1,1000)
    fixtures = ["obsidia-fixtures-organization"]

    def setUp(self):
        self.client = Client()

    def test_organization_GET_org_dto_should_succeed(self):
        """Test"""
        for each_org_id in list(self.range_of_entries):
            # As a user we get the org id
            response = self.client.get(f"/organization/{each_org_id}")
            response_org = response.content.decode("UTF-8")
            
            # Grab the DTO straight from database for comparison
            org_obj: Organization = Organization.objects.get(pk=each_org_id) # pylint: disable=E1101
            dto_org = org_obj.get_dto()
            
            # Assertions
            # Also assert that the DTO object as a dict matches response_org
            self.assertEqual(response.status_code, 200)
            self.assertEqual(str(dto_org), response_org)

    def test_each_org_in_db_has_keys_should_succeed(self):
        """Test that organization converted to string should succeed"""
        for each_org_id in list(self.range_of_entries):
            # Grab the DTO straight from database for comparison
            org_obj: Organization = Organization.objects.get(pk=each_org_id) # pylint: disable=E1101
            keys_to_have = [
                "name",
                "users",
                "adminUsers",
                "dateCreated",
                "dateLastModified"
            ]

            for each_key in keys_to_have:
                dict_org = org_obj.get_dict()
                self.assertIn(each_key, dict_org)