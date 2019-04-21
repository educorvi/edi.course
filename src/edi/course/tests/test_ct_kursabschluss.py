# -*- coding: utf-8 -*-
from edi.course.content.kursabschluss import IKursabschluss  # NOQA E501
from edi.course.testing import EDI_COURSE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class KursabschlussIntegrationTest(unittest.TestCase):

    layer = EDI_COURSE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Kurs',
            self.portal,
            'kursabschluss',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_kursabschluss_schema(self):
        fti = queryUtility(IDexterityFTI, name='Kursabschluss')
        schema = fti.lookupSchema()
        self.assertEqual(IKursabschluss, schema)

    def test_ct_kursabschluss_fti(self):
        fti = queryUtility(IDexterityFTI, name='Kursabschluss')
        self.assertTrue(fti)

    def test_ct_kursabschluss_factory(self):
        fti = queryUtility(IDexterityFTI, name='Kursabschluss')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IKursabschluss.providedBy(obj),
            u'IKursabschluss not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_kursabschluss_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Kursabschluss',
            id='kursabschluss',
        )

        self.assertTrue(
            IKursabschluss.providedBy(obj),
            u'IKursabschluss not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_kursabschluss_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Kursabschluss')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
