# -*- coding: utf-8 -*-
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)

import medialog.flipbook


class MedialogFlipbookLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=medialog.flipbook)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'medialog.flipbook:default')


MEDIALOG_FLIPBOOK_FIXTURE = MedialogFlipbookLayer()


MEDIALOG_FLIPBOOK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIALOG_FLIPBOOK_FIXTURE,),
    name='MedialogFlipbookLayer:IntegrationTesting',
)


MEDIALOG_FLIPBOOK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIALOG_FLIPBOOK_FIXTURE,),
    name='MedialogFlipbookLayer:FunctionalTesting',
)
