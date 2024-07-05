import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.models import CaseFile

class CaseFileModelsTestCase(TestCase):
    range_of_entries = range(1,1000)
    fixtures = ["obsidia-fixtures-organization.json", "obsidia-fixtures-casefile.json"]
    
    def setUp(self):
        self.client = Client()

    def test_casefile_GET_dto_should_succeed(self):
        """Test that GETting the casefile should match the DTO."""
        for each_casefile_id in list(self.range_of_entries):
            response = self.client.get(f"/organization/casefile/{each_casefile_id}")
            response_casefile = response.content.decode("UTF-8")

            casefile_obj: CaseFile = CaseFile.objects.get(pk=each_casefile_id)
            dto_casefile = casefile_obj.get_dto()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(str(dto_casefile), response_casefile)

    def test_each_casefile_in_db_to_string_should_succeed(self):
        """Test that organization converted to string should succeed"""
        for each_casefile_id in list(self.range_of_entries):
            # Grab the DTO straight from database for comparison
            casefile_obj: CaseFile = CaseFile.objects.get(pk=each_casefile_id) # pylint: disable=E1101
            keys_to_have = [
                "caseIdentifier",
                "organization",
                "dateCreated",
                "dateLastModified",
                "dateLastModified",
                "createdBy",
                "status"
            ]

            for each_key in keys_to_have:
                dict_org = casefile_obj.get_dict()
                self.assertIn(each_key, dict_org)

    def test_casefile_GET_all_casefiles_in_org_should_succeed(self):
        """Test that we can get all casefiles in an org."""
        response = self.client.get("/organization/inventory/casefiles")
        response_casefiles = response.content.decode("UTF-8")
        loaded_resp_casefiles = json.loads(response_casefiles)
        self.assertEqual(len(loaded_resp_casefiles), 1000)

    def test_casefile_GET_casefile_by_tags_should_succeed(self):
        pass

    def test_casefile_POST_casefile_by_index_should_fail(self):
        for each_casefile_id in range(1,100):
            response = self.client.post(f"/organization/casefile/{each_casefile_id}")
            self.assertEqual(response.status_code, 400)

    def test_casefile_POST_casefile_all_should_fail(self):
        response = self.client.post(f"/organization/inventory/casefile")
        self.assertEqual(response.status_code, 404)