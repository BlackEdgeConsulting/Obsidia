import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.models import CaseFile, TargetOfInterest

class CaseFileModelsTestCase(TestCase):
    range_of_entries = range(1,1000)
    fixtures = [
        "obsidia-fixtures-organization.json",
        "obsidia-fixtures-casefile.json",
        "obsidia-fixtures-target-of-interest.json",
        "obsidia-fixtures-tagset.json",
        "obsidia-fixtures-tag.json"
    ]
    
    def setUp(self):
        self.client = Client()

    def test_casefile_GET_dto_should_succeed(self):
        """Test that GETting the casefile should match the DTO."""
        for each_casefile_id in list(self.range_of_entries):
            response = self.client.get(f"/organization/casefile/{each_casefile_id}")
            response_casefile = response.content.decode("UTF-8")

            casefile_obj: CaseFile = CaseFile.objects.get(pk=each_casefile_id)
            target_of_interest: TargetOfInterest = TargetOfInterest.objects.get(casefile=each_casefile_id)
            dto_casefile = casefile_obj.get_dto()
            dto_casefile.targetOfInterest = str(target_of_interest)


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

    def test_casefile_inventory_GET_all_casefiles_in_org_should_succeed(self):
        """Test that we can get all casefiles in an org."""
        response = self.client.get("/organization/inventory/casefiles")
        response_casefiles = response.content.decode("UTF-8")
        loaded_resp_casefiles = json.loads(response_casefiles)
        self.assertEqual(len(loaded_resp_casefiles), 1000)

    def test_casefile_GET_casefile_by_tags_should_fail(self):
        # response = self.client.get("/organization/casefiles")
        pass

    def test_casefile_GET_inventory_casefile_by_tags_should_succeed(self):
        payloads = [
            {
                "tag_payload": {
                    "key": "vestibulum",
                    "value": "Synchronised intangible array"
                },
                "expect": {
                    "caseIdentifier": "prizziellodn247325",
                    "organization": {
                        "name": "Fivespan100775",
                        "dateCreated": "2024-06-13 14:45:41+00:00",
                        "dateLastModified": "2024-01-29 19:03:40+00:00",
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
                                "name": "dzaple0",
                                "roleId": 4249
                            },
                            {
                                "name": "lsalterne1",
                                "roleId": 6994
                            }
                        ],
                    },
                    "status": "PENDING",
                    "tags": [
                        {
                            "key": "vestibulum",
                            "value": "Synchronised intangible array"
                        }
                    ],
                    "targetOfInterest": {
                        "firstName": "",
                        "middleNames": "",
                        "lastName": "",
                        "fullName": "",
                        "additionalNames": "",
                        "dateOfBirth": "1536-08-26T15:13:46Z",
                        "currentAddress": "",
                        "previousAddresses": [],
                        "associatedAddresses": [],
                        "targetJustification": "",
                        "socialSecurityNumber": "",
                        "driversLicenseNumber": "",
                        "governmentIssueId": "",
                        "additionalIdentifications": ""
                    }
                }
            }
        ]

        for each_payload in payloads:
            response = self.client.get("/organization/inventory/casefiles", each_payload["tag_payload"])
            decoded_response = json.loads(response.content.decode("UTF-8"))
            
            self.assertIsInstance(decoded_response, list)
            self.assertEqual(len(decoded_response), 1) # Check that there's one element
            
            clean_casefile: list = json.loads(decoded_response[0])
            clean_casefile["organization"]["users"] = json.loads(clean_casefile["organization"]["users"].replace("'", "\""))
            clean_casefile["organization"]["adminUsers"] = json.loads(clean_casefile["organization"]["adminUsers"].replace("'", "\""))

            self.assertEqual(clean_casefile, each_payload["expect"])
            