# -*- coding: utf-8 -*-
from edi.course.behaviors.kursnotiz import IKursnotizMarker
from edi.course.testing import EDI_COURSE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class KursnotizIntegrationTest(unittest.TestCase):

    layer = EDI_COURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_kursnotiz(self):
        behavior = getUtility(IBehavior, 'edi.course.kursnotiz')
        self.assertEqual(
            behavior.marker,
            IKursnotizMarker,
        )
