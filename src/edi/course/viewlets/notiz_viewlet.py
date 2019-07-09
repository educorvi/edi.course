# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone import api as ploneapi
from edi.course.persistance import getCourse
from Products.CMFPlone.utils import getToolByName

class NotizViewlet(ViewletBase):

    def get_action(self):
        return self.context.absolute_url() + '/validate-notizen'

    def get_homefolder(self):
        portal = ploneapi.portal.get()
        membersfolder = portal['Members']
        pm = getToolByName(portal, 'portal_membership')
        homeurl = pm.getHomeUrl()
        if homeurl:
            folderid = homeurl.split('/')[-1]
            homefolder = membersfolder[folderid]
            return homefolder
        return None


    def get_notizbuch(self, homefolder):
        kurs = getCourse(self.context)
        if kurs:
            if kurs.id in homefolder.keys():
                return homefolder[kurs.id]
        return ''


    def get_notizen(self):
        homefolder = self.get_homefolder()
        if not homefolder:
            return []
        notizbuch = self.get_notizbuch(homefolder)
        normalizer = getUtility(IIDNormalizer)
        if hasattr(self.context, 'notizen'):
            if self.context.notizen:
                notizen = []
                for i in self.context.notizen:
                    notizid = normalizer.normalize(i['title'])
                    if not i.has_key('fieldformat'):
                        i['fieldformat'] = u'Text'
                    fieldformat = i['fieldformat']
                    if fieldformat != u'Zeile':
                        i['fieldformat'] = u'Text'
                    i['name'] = notizid
                    i['data'] = ''
                    if notizbuch:
                        if notizid in notizbuch.keys():
                            i['data'] = notizbuch[notizid].notiz
                    notizen.append(i)
                return notizen
        return []

    def render(self):
        if self.get_notizen():
            return super(NotizViewlet, self).render()
        return ''
