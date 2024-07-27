import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.models import CaseFile, TargetOfInterest

class OrganizationStoriesTestCase(TestCase):
    def test_organization_user_story_create_new(self):
        """As a user I want to create a new Organization.
        """
    
    def test_organization_user_story_add_new_users(self):
        """As a user I want to add new users to my Organization.
        """
    
    def test_organization_user_story_add_new_admins(self):
        """As a user I want to add a new admin user for management.
        """
    
    def test_organization_user_story_delete(self):
        """As a user I want to delete an Organization.
        """