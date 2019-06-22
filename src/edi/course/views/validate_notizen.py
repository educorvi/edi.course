# -*- coding: utf-8 -*-
import transaction
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from edi.course.persistance import getCourse

class ValidateNotizen(BrowserView):

    def get_homefolder(self):
        portal = ploneapi.portal.get()
        membersfolder = portal['Members']
        pm = getToolByName(portal, 'portal_membership')
        homeurl = pm.getHomeUrl()
        folderid = homeurl.split('/')[-1]
        homefolder = membersfolder[folderid]
        return homefolder


    def get_notizbuch(self, homefolder):
        kurs = getCourse(self.context)
        if not kurs.id in homefolder.keys():
            notizbuch = ploneapi.content.create(
                          type = 'Notizbuch',
                          id = kurs.id,
                          title = kurs.title,
                          container=homefolder)
            transaction.commit()
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
            transaction.commit()
        else:
            notizbuch[notiz['id']].notiz = notiz['data']


    def __call__(self):
        normalizer = getUtility(IIDNormalizer)
        homefolder = self.get_homefolder() 
        if self.request.form:
            if hasattr(self.context, 'notizen'):
                if self.context.notizen:
                    for notiz in self.context.notizen:
                        notiz['data'] = self.request.get(normalizer.normalize(notiz['title']))
                        notiz['id'] = normalizer.normalize(notiz['title'])
                        notiz['url'] = self.context.absolute_url()
                        if notiz['data']:
                            notizbuch = self.get_notizbuch(homefolder)
                            notiz = self.set_notiz(notizbuch, notiz) 
