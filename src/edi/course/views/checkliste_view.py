# -*- coding: utf-8 -*-

from edi.course import _
from Products.Five.browser import BrowserView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ChecklisteView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('checkliste_view.pt')

    def form_url(self):
        return self.context.absolute_url() + '/validate-checklist'

    def __call__(self):
        self.msg = _(u'A small message')
        return self.index()
