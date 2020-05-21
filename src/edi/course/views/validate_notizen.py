# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from edi.course.persistance import getCourse

class ValidateNotizen(BrowserView):

    def get_homefolder(self):
        pm = ploneapi.portal.get_tool(name='portal_membership')
        homefolder = pm.getHomeFolder()
        return homefolder


    def get_notizbuch(self, homefolder):
        kurs = getCourse(self.context)
        if not kurs.id in homefolder.keys():
            notizbuch = ploneapi.content.create(
                          type = 'Notizbuch',
                          id = kurs.id,
                          title = kurs.title,
                          container=homefolder)
        else:
            notizbuch = homefolder[kurs.id]
        return notizbuch


    def set_notiz(self, notizbuch, notiz):
        if not notiz['id'] in notizbuch.keys():
            notiz = ploneapi.content.create(
                type = 'Notiz',
                id = notiz['id'],
                title = notiz['title'],
                description = notiz['description'],
                notiz = notiz['data'],
                link = notiz['url'],
                container = notizbuch)
        else:
            notizbuch[notiz['id']].notiz = notiz['data']


    def __call__(self):
        normalizer = getUtility(IIDNormalizer)
        homefolder = self.get_homefolder() 
        if self.request.form:
            if hasattr(self.context.aq_inner, 'notizen'):
                if self.context.aq_inner.notizen:
                    for notiz in self.context.notizen:
                        notizid = normalizer.normalize(notiz['title'])
                        notiz['data'] = self.request.get(notizid)
                        notiz['id'] = notizid
                        notiz['url'] = self.context.absolute_url()
                        if notiz['data']:
                            notizbuch = self.get_notizbuch(homefolder)
                            notiz = self.set_notiz(notizbuch, notiz)
                            message = u"Die Notiz wurde erfolgreich gespeichert."
                            ploneapi.portal.show_message(message = message, request = self.request, type = "info")
        return self.request.response.redirect(self.context.absolute_url())
