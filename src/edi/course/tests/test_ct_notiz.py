# -*- coding: utf-8 -*-
from edi.course.content.notiz import INotiz  # NOQA E501
from edi.course.testing import EDI_COURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class NotizIntegrationTest(unittest.TestCase):

    layer = EDI_COURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Notizbuch',
            self.portal,
            'notiz',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_notiz_schema(self):
        fti = queryUtility(IDexterityFTI, name='Notiz')
        schema = fti.lookupSchema()
        self.assertEqual(INotiz, schema)

    def test_ct_notiz_fti(self):
        fti = queryUtility(IDexterityFTI, name='Notiz')
        self.assertTrue(fti)

    def test_ct_notiz_factory(self):
        fti = queryUtility(IDexterityFTI, name='Notiz')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            INotiz.providedBy(obj),
            u'INotiz not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_notiz_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Notiz',
            id='notiz',
        )

        self.assertTrue(
            INotiz.providedBy(obj),
            u'INotiz not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_notiz_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Notiz')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
