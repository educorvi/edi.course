# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import edi.course


class EdiCourseLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=edi.course)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edi.course:default')


EDI_COURSE_FIXTURE = EdiCourseLayer()


EDI_COURSE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDI_COURSE_FIXTURE,),
    name='EdiCourseLayer:IntegrationTesting',
)


EDI_COURSE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDI_COURSE_FIXTURE,),
    name='EdiCourseLayer:FunctionalTesting',
)


EDI_COURSE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EDI_COURSE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EdiCourseLayer:AcceptanceTesting',
)
