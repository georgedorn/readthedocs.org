from django.test import TestCase

import os
import shutil

from django.contrib.admin.models import User

from projects.models import Project
from builds.models import Version
from projects import tasks

from rtd_tests.utils import make_test_git
from rtd_tests.tests.base import RTDTestCase

from tracking.models import DocView

class TestDocTracking(RTDTestCase):
    fixtures = ['eric.json']

    def setUp(self):
        repo = make_test_git()
        self.repo = repo
        super(TestDocTracking, self).setUp()
        self.eric = User.objects.get(username='eric')
        self.project = Project.objects.create(
            name="Test Project",
            repo_type="git",
            #Our top-level checkout
            repo=repo,
        )
        self.version = Version.objects.create(project=self.project,
                                              slug='latest')
        self.project.users.add(self.eric)

    def test_simple_docview_from_url(self):
        url = self.project.get_absolute_url()
        dv = DocView.from_url(url)
        self.assertEqual(dv.project, self.project)
        self.assertEqual(dv.version, self.version)
        self.assertEqual(dv.language, 'en')
        self.assertEqual(dv.sphinx_filename, 'index.html')