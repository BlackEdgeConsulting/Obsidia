import json
from django.test import TestCase, Client
from datetime import date, datetime
from CaseManagement.models import CaseFile, TargetOfInterest

class CaseFileStoriesTestCase(TestCase):
    def test_casefile_user_story_create_new(self):
        """As a user I want to create a new CaseFile based on a target I found.
        """
        pass
    
    def test_casefile_user_story_search_by_name(self):
        """As a user I want to search for a CaseFile based on a name.
        """
        pass
    
    def test_casefile_user_story_search_by_target_data(self):
        """As a user I want to search for a CaseFile based on a some of the target of interest data.
        """
        pass
    
    def test_casefile_user_story_archive_old(self):
        """As a user I want to archive a CaseFile that I'm not interested in anymore.
        """
        pass
    
    def test_casefile_user_story_bulk_upload(self):
        """As a user I want to create bulk CaseFiles based on my phone contacts.
        """
        pass