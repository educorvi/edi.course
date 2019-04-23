# -*- coding: utf-8 -*-
from edi.course.content.video import IVideo  # NOQA E501
from edi.course.testing import EDI_COURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class VideoIntegrationTest(unittest.TestCase):

    layer = EDI_COURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Lerneinheit',
            self.portal,
            'video',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_video_schema(self):
        fti = queryUtility(IDexterityFTI, name='Video')
        schema = fti.lookupSchema()
        self.assertEqual(IVideo, schema)

    def test_ct_video_fti(self):
        fti = queryUtility(IDexterityFTI, name='Video')
        self.assertTrue(fti)

    def test_ct_video_factory(self):
        fti = queryUtility(IDexterityFTI, name='Video')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IVideo.providedBy(obj),
            u'IVideo not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_video_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Video',
            id='video',
        )

        self.assertTrue(
            IVideo.providedBy(obj),
            u'IVideo not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_video_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Video')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
