# -*- coding: utf-8 -*-
from edi.course.content.videoseite import IVideoseite  # NOQA E501
from edi.course.testing import EDI_COURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class VideoseiteIntegrationTest(unittest.TestCase):

    layer = EDI_COURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Lerneinheit',
            self.portal,
            'videoseite',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_videoseite_schema(self):
        fti = queryUtility(IDexterityFTI, name='Videoseite')
        schema = fti.lookupSchema()
        self.assertEqual(IVideoseite, schema)

    def test_ct_videoseite_fti(self):
        fti = queryUtility(IDexterityFTI, name='Videoseite')
        self.assertTrue(fti)

    def test_ct_videoseite_factory(self):
        fti = queryUtility(IDexterityFTI, name='Videoseite')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IVideoseite.providedBy(obj),
            u'IVideoseite not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_videoseite_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Videoseite',
            id='videoseite',
        )

        self.assertTrue(
            IVideoseite.providedBy(obj),
            u'IVideoseite not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_videoseite_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Videoseite')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
