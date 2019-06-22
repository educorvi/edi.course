# -*- coding: utf-8 -*-
from edi.course.content.notizbuch import INotizbuch  # NOQA E501
from edi.course.testing import EDI_COURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class NotizbuchIntegrationTest(unittest.TestCase):

    layer = EDI_COURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_notizbuch_schema(self):
        fti = queryUtility(IDexterityFTI, name='Notizbuch')
        schema = fti.lookupSchema()
        self.assertEqual(INotizbuch, schema)

    def test_ct_notizbuch_fti(self):
        fti = queryUtility(IDexterityFTI, name='Notizbuch')
        self.assertTrue(fti)

    def test_ct_notizbuch_factory(self):
        fti = queryUtility(IDexterityFTI, name='Notizbuch')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            INotizbuch.providedBy(obj),
            u'INotizbuch not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_notizbuch_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Notizbuch',
            id='notizbuch',
        )

        self.assertTrue(
            INotizbuch.providedBy(obj),
            u'INotizbuch not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_notizbuch_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Notizbuch')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_notizbuch_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Notizbuch')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'notizbuch_id',
            title='Notizbuch container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
