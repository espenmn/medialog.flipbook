# -*- coding: utf-8 -*-

# from medialog.flipbook import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from plone import api

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IFlipbookView(Interface):
    """ Marker Interface for IFlipbookView"""


@implementer(IFlipbookView)
class FlipbookView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('flipbook_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()

    def get_images(self):
        """Get all images from the current folder"""
        context = self.context
        catalog = api.portal.get_tool('portal_catalog')
        
        # Query for images in the current folder
        images = catalog(
            path={'query': '/'.join(context.getPhysicalPath()), 'depth': 1},
            portal_type='Image',
            sort_on='getObjPositionInParent'
        )
        
        image_data = []
        for brain in images:
            obj = brain.getObject()
            image_data.append({
                'url': obj.absolute_url(),
                'title': brain.Title,
                'description': brain.Description
            })
        
        return image_data