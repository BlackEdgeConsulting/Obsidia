import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.DTOModels import DTOOrganization
from CaseManagement.models import Organization



class OrganizationModelsGetTestCase(TestCase):
    range_of_entries = range(1,1000)
    fixtures = ["obsidia-fixtures-organization"]

    def setUp(self):
        self.client = Client()

    def test_organization_GET_org_by_id_should_succeed(self):
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

    def test_organization_GET_current_organization_should_succeed(self):
        response = self.client.get("/organization/", content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("UTF-8"), '{"name": "Fivespan100775", "users": "[{\'name\': \'jrykert0\', \'roleId\': 6368}, {\'name\': \'wfearne1\', \'roleId\': 3684}, {\'name\': \'ncouche2\', \'roleId\': 2558}]", "adminUsers": "[{\'name\': \'dzaple0\', \'roleId\': 4249}, {\'name\': \'lsalterne1\', \'roleId\': 6994}]", "dateCreated": "2024-06-13 14:45:41+00:00", "dateLastModified": "2024-01-29 19:03:40+00:00"}')


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

    def test_organization_inventory_GET_get_all_org_inventory_should_succeed(self):
        pass

    def test_organization_inventory_tags_GET_get_all_tags_in_org_should_succeed(self):
        pass