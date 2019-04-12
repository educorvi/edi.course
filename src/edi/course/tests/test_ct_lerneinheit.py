# -*- coding: utf-8 -*-
from edi.course.testing import EDI_COURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class LerneinheitIntegrationTest(unittest.TestCase):

    layer = EDI_COURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Kurs',
            self.portal,
            'lerneinheit',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_lerneinheit_schema(self):
        fti = queryUtility(IDexterityFTI, name='Lerneinheit')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Lerneinheit')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_lerneinheit_fti(self):
        fti = queryUtility(IDexterityFTI, name='Lerneinheit')
        self.assertTrue(fti)

    def test_ct_lerneinheit_factory(self):
        fti = queryUtility(IDexterityFTI, name='Lerneinheit')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_lerneinheit_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Lerneinheit',
            id='lerneinheit',
        )


    def test_ct_lerneinheit_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Lerneinheit')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_lerneinheit_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Lerneinheit')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'lerneinheit_id',
            title='Lerneinheit container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
