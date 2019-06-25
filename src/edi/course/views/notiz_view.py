# -*- coding: utf-8 -*-

from urlparse import urlparse
from plone import api as ploneapi
from edi.course import _
from Products.Five.browser import BrowserView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NotizView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('notiz_view.pt')

    def get_contextobj(self):
        url = self.context.link
        portalid = ploneapi.portal.get().getId()
        obj = None
        if url:
            elements = urlparse(url)
            pfad = "/%s%s" %(portalid, elements.path)
            obj = ploneapi.content.get(path=pfad)
            return obj
        return obj

    def get_content(self):
        contextobj = self.get_contextobj()
        content = {}
        content['title'] = contextobj.title
        content['description'] = contextobj.description
        content['text'] = ''
        if contextobj.portal_type == 'Audiovideo':
            html = ''
            if contextobj.vortext:
                html += contextobj.vortext.output
            if contextobj.nachtext:
                html += contextobj.nachtext.output
            content['text'] = html
        return content        
