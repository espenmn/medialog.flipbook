# -*- coding: utf-8 -*-
from medialog.flipbook.testing import MEDIALOG_FLIPBOOK_FUNCTIONAL_TESTING
from medialog.flipbook.testing import MEDIALOG_FLIPBOOK_INTEGRATION_TESTING
from medialog.flipbook.browser.static.lib.flipbook_view import IFlipbookView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_FLIPBOOK_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_flipbook_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='flipbook-view'
        )
        self.assertTrue(IFlipbookView.providedBy(view))

    def test_flipbook_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='flipbook-view'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IFlipbookView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = MEDIALOG_FLIPBOOK_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
