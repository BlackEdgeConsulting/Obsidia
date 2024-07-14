import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.DTOModels import DTOOrganization
from CaseManagement.models import Organization



class OrganizationModelsGetTestCase(TestCase):
    range_of_entries = range(1,1000)
    fixtures = [
        "obsidia-fixtures-organization.json",
        "obsidia-fixtures-casefile.json",
        "obsidia-fixtures-tag.json",
        "obsidia-fixtures-tagset.json"
    ]

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
        response = self.client.get("/organization/inventory", content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        inventory = json.loads(response.content.decode("UTF-8"))

        self.assertEqual(response.status_code, 200)
        current_organization = json.loads(self.client.get("/organization/", content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest").content.decode("UTF-8"))
        current_organization_name = current_organization["name"]
        
        self.assertIn("organization", inventory.keys())
        self.assertIn(current_organization_name, inventory["organization"])
        
        self.assertIn("properties", inventory["organization"][current_organization_name].keys())
        self.assertIn("inventory", inventory["organization"][current_organization_name].keys())

        self.assertIn("name", inventory["organization"][current_organization_name]["properties"].keys())
        self.assertIn("users", inventory["organization"][current_organization_name]["properties"])
        self.assertIn("adminUsers", inventory["organization"][current_organization_name]["properties"])
        self.assertIn("dateCreated", inventory["organization"][current_organization_name]["properties"])
        self.assertIn("dateLastModified", inventory["organization"][current_organization_name]["properties"])

        self.assertIn("casefile_inventory", inventory["organization"][current_organization_name]["inventory"])
        self.assertIsInstance(inventory["organization"][current_organization_name]["inventory"]["casefile_inventory"], list)


    def test_organization_inventory_tags_GET_get_all_tags_in_org_should_succeed(self):
        """Test that as a user we can get all the tags currently in use in the org.
        """
        expect = ["faucibus", "nunc", "rutrum", "cubilia", "morbi", "sed", "sollicitudin", "nec", "at", "in", "etiam", "vulputate", "luctus", "sagittis", "mauris", "tincidunt", "at", "porttitor", "in", "ultrices", "sapien", "et", "eu", "tortor", "auctor", "sodales", "hac", "amet", "facilisi", "felis", "felis", "posuere", "consectetuer", "ante", "sapien", "sem", "erat", "interdum", "sagittis", "eleifend", "vulputate", "ut", "vel", "fermentum", "a", "blandit", "sem", "euismod", "faucibus", "nulla", "turpis", "praesent", "pulvinar", "mi", "ante", "nibh", "auctor", "fusce", "luctus", "vestibulum", "amet", "justo", "feugiat", "morbi", "mauris", "justo", "justo", "curae", "aliquam", "integer", "pellentesque", "felis", "aliquam", "dui", "in", "sit", "vel", "turpis", "tempus", "vivamus", "mauris", "maecenas", "nisl", "vestibulum", "aenean", "amet", "libero", "libero", "non", "nonummy", "erat", "sapien", "vestibulum", "arcu", "quam", "nullam", "faucibus", "sapien", "mi", "pretium", "metus", "pellentesque", "arcu", "venenatis", "nulla", "cubilia", "lacinia", "nam", "curabitur", "ut", "dapibus", "donec", "nisi", "amet", "congue", "suspendisse", "ante", "ut", "turpis", "fusce", "morbi", "ac", "consequat", "vestibulum", "arcu", "quis", "tristique", "erat", "et", "mattis", "eleifend", "nulla", "massa", "laoreet", "sapien", "at", "nullam", "nascetur", "congue", "primis", "integer", "erat", "purus", "pellentesque", "luctus", "amet", "ac", "sit", "convallis", "orci", "eu", "quam", "pede", "potenti", "massa", "aenean", "justo", "ipsum", "dui", "pellentesque", "orci", "justo", "sapien", "non", "sit", "rhoncus", "curabitur", "id", "in", "mauris", "nulla", "nisi", "elementum", "sed", "natoque", "cubilia", "in", "volutpat", "mattis", "nisl", "orci", "lacinia", "gravida", "pretium", "vitae", "vel", "non", "est", "erat", "semper", "curae", "ligula", "platea", "potenti", "mauris", "fusce", "tortor", "phasellus", "massa", "ut", "natoque", "condimentum", "posuere", "morbi", "pede", "ac", "nascetur", "rutrum", "placerat", "sapien", "aliquam", "erat", "vestibulum", "ligula", "viverra", "aenean", "imperdiet", "a", "quis", "luctus", "aenean", "quam", "augue", "vehicula", "neque", "at", "ultrices", "rhoncus", "nisl", "in", "vivamus", "blandit", "vestibulum", "pulvinar", "blandit", "at", "dapibus", "phasellus", "amet", "natoque", "nunc", "dictumst", "volutpat", "interdum", "nec", "ipsum", "vehicula", "consequat", "vulputate", "pellentesque", "amet", "purus", "feugiat", "nibh", "in", "morbi", "placerat", "tortor", "luctus", "sapien", "mauris", "elit", "amet", "maecenas", "quis", "donec", "eleifend", "vel", "aliquet", "nisl", "donec", "ut", "ac", "adipiscing", "molestie", "in", "venenatis", "vestibulum", "hac", "sed", "volutpat", "diam", "massa", "molestie", "vel", "ut", "leo", "libero", "enim", "vestibulum", "justo", "vivamus", "elit", "ut", "quis", "placerat", "tempor", "erat", "elementum", "dictumst", "sit", "erat", "dolor", "nec", "non", "justo", "faucibus", "amet", "nam", "ante", "odio", "lacus", "porttitor", "sit", "fusce", "et", "cubilia", "ligula", "commodo", "vestibulum", "ultrices", "hac", "cubilia", "dictumst", "odio", "at", "platea", "pellentesque", "condimentum", "tempor", "neque", "vestibulum", "justo", "elementum", "dui", "quam", "curae", "et", "vel", "dapibus", "in", "ante", "erat", "phasellus", "in", "interdum", "vestibulum", "mattis", "ipsum", "cras", "orci", "at", "dui", "lacus", "nullam", "venenatis", "id", "nulla", "aliquam", "ut", "posuere", "ligula", "tristique", "vestibulum", "aenean", "quam", "imperdiet", "tellus", "nec", "vulputate", "volutpat", "in", "dolor", "eu", "ut", "molestie", "hac", "arcu", "magnis", "ultricies", "pede", "ac", "hendrerit", "leo", "sed", "amet", "metus", "justo", "cubilia", "curae", "et", "semper", "porttitor", "primis", "sapien", "morbi", "posuere", "imperdiet", "eleifend", "tincidunt", "potenti", "ut", "augue", "aliquam", "ultrices", "libero", "sed", "tempor", "morbi", "rutrum", "eu", "a", "ipsum", "magnis", "eu", "dui", "justo", "amet", "enim", "odio", "pellentesque", "id", "rutrum", "eu", "sit", "sagittis", "eu", "sit", "nulla", "adipiscing", "ante", "in", "diam", "nullam", "nisl", "eros", "ac", "imperdiet", "eget", "interdum", "elementum", "fusce", "luctus", "dolor", "sit", "dui", "ipsum", "fusce", "primis", "semper", "adipiscing", "justo", "tellus", "urna", "habitasse", "potenti", "fermentum", "leo", "semper", "eget", "nonummy", "mus", "nulla", "eu", "vestibulum", "velit", "quis", "consectetuer", "pellentesque", "eros", "volutpat", "posuere", "in", "blandit", "leo", "diam", "egestas", "ligula", "arcu", "in", "aenean", "luctus", "nulla", "phasellus", "nam", "in", "felis", "suspendisse", "lorem", "maecenas", "vehicula", "amet", "id", "magnis", "curae", "velit", "vestibulum", "sed", "vestibulum", "vulputate", "donec", "quisque", "non", "ligula", "tortor", "adipiscing", "placerat", "molestie", "eget", "vel", "a", "lobortis", "duis", "consequat", "mattis", "eget", "tellus", "at", "condimentum", "eget", "ante", "potenti", "adipiscing", "in", "nunc", "condimentum", "nulla", "cras", "phasellus", "viverra", "vivamus", "aliquam", "platea", "quis", "venenatis", "orci", "turpis", "ipsum", "nulla", "sapien", "consequat", "pede", "rutrum", "eleifend", "nulla", "magna", "porttitor", "consequat", "augue", "et", "eget", "porta", "habitasse", "adipiscing", "libero", "placerat", "nunc", "donec", "augue", "curae", "blandit", "phasellus", "pede", "accumsan", "justo", "nulla", "justo", "vulputate", "tincidunt", "eu", "maecenas", "maecenas", "in", "eget", "ultrices", "vestibulum", "in", "auctor", "dictumst", "elit", "lacinia", "sit", "id", "lacus", "eget", "morbi", "gravida", "neque", "volutpat", "convallis", "leo", "quam", "ut", "eget", "libero", "tristique", "sit", "fusce", "fusce", "ut", "quis", "fermentum", "ut", "dui", "enim", "amet", "molestie", "penatibus", "nisl", "erat", "aliquet", "nulla", "ultrices", "eu", "amet", "donec", "fusce", "donec", "nascetur", "tempus", "consequat", "posuere", "nascetur", "ac", "leo", "eu", "morbi", "purus", "donec", "sociis", "quisque", "dignissim", "amet", "ut", "elementum", "nulla", "nibh", "consequat", "id", "magna", "sapien", "dis", "at", "bibendum", "mattis", "elementum", "varius", "et", "ut", "erat", "morbi", "eu", "ligula", "commodo", "sed", "in", "ultrices", "quisque", "ultricies", "donec", "diam", "non", "nullam", "ipsum", "condimentum", "metus", "lacinia", "dictumst", "congue", "eget", "vel", "sagittis", "feugiat", "nibh", "luctus", "nulla", "porttitor", "ipsum", "curabitur", "tincidunt", "pretium", "eu", "volutpat", "odio", "orci", "montes", "quisque", "morbi", "quisque", "urna", "dolor", "in", "turpis", "morbi", "sapien", "aliquet", "nec", "tellus", "mauris", "risus", "ullamcorper", "ut", "consequat", "mauris", "cubilia", "luctus", "rutrum", "id", "integer", "augue", "nulla", "vivamus", "vel", "nullam", "duis", "non", "ut", "duis", "lobortis", "nulla", "luctus", "fusce", "diam", "nulla", "turpis", "mauris", "nulla", "vel", "tincidunt", "volutpat", "mauris", "fringilla", "vel", "tempus", "nam", "at", "vitae", "dui", "luctus", "phasellus", "ut", "in", "amet", "nisl", "tincidunt", "sem", "in", "in", "dui", "in", "nulla", "erat", "arcu", "lorem", "odio", "sem", "elit", "porta", "ut", "turpis", "a", "dapibus", "justo", "orci", "quam", "maecenas", "sapien", "purus", "faucibus", "curae", "in", "donec", "neque", "sapien", "in", "aenean", "lacus", "nibh", "platea", "tristique", "aliquet", "cum", "mi", "eleifend", "phasellus", "augue", "nulla", "amet", "sem", "quisque", "aliquet", "tincidunt", "gravida", "risus", "nulla", "luctus", "elementum", "quam", "diam", "metus", "eros", "enim", "id", "convallis", "vel", "vulputate", "nulla", "et", "sed", "dui", "felis", "accumsan", "duis", "donec", "vestibulum", "convallis", "dapibus", "ligula", "curae", "eget", "pretium", "nulla", "ultrices", "suspendisse", "arcu", "sit", "eu", "sed", "penatibus", "sagittis", "nibh", "interdum", "enim", "in", "varius", "in", "tincidunt", "morbi", "sit", "sapien", "interdum", "erat", "ac", "dui", "placerat", "integer", "eu", "nullam", "suscipit", "sociis", "in", "vel", "convallis", "sed", "elit", "sed", "vestibulum", "vitae", "mollis", "consequat", "maecenas", "ante", "pellentesque", "curae", "id", "massa", "in", "massa", "eu", "nec", "cubilia", "placerat", "est", "non", "vestibulum", "vestibulum", "tincidunt", "luctus", "morbi", "ut", "turpis", "non", "vestibulum", "vestibulum", "quam", "pede", "nisl", "nunc", "nec", "vel", "quis", "semper", "consequat", "sed", "sit", "sapien", "tristique", "lobortis", "velit", "molestie", "venenatis", "sapien", "fermentum", "mauris", "nisl", "ultrices", "tristique", "vivamus", "cras", "egestas", "a", "vel", "tellus", "tristique", "nulla", "in", "venenatis", "mauris", "tristique", "sollicitudin", "consequat", "nisi", "vel", "condimentum", "in", "blandit", "iaculis", "ligula", "bibendum", "non", "quam", "eu", "sapien", "consequat", "viverra", "pede", "varius", "odio", "congue", "bibendum", "consequat", "ultrices", "tristique", "proin", "varius", "nulla", "id", "nullam", "amet", "quis", "phasellus", "suspendisse", "nisi", "cursus", "integer", "turpis", "proin", "diam", "ultrices", "consequat", "semper", "nisi", "mattis", "primis", "nulla", "turpis", "in", "ac", "faucibus", "ac", "integer", "accumsan", "in", "lacus", "dapibus", "lacinia", "nisi", "lacinia", "morbi", "vel", "libero", "sapien", "in", "volutpat", "in", "elementum", "vestibulum", "fusce", "diam", "donec", "lacus", "sapien", "nibh", "sapien", "ultrices", "quam", "ac", "arcu", "at", "imperdiet"]

        response = self.client.get("/organization/inventory/tags", content_type="application/json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        tag_keys = json.loads(response.content.decode("UTF-8"))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(tag_keys, expect)
