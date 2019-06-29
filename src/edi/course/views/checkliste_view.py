# -*- coding: utf-8 -*-
import pymongo
from edi.course import _
from Products.Five.browser import BrowserView
from plone import api as ploneapi
from edi.course.persistance import getCourse
from edi.course.persistance import mongoclient

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ChecklisteView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('checkliste_view.pt')

    def get_data(self):
        data = {}
        kurs = getCourse(self.context)
        cdb = mongoclient[kurs.id]
        clc = cdb.checklist_collection
        studentid = ploneapi.user.get_current().getId()
        formdata = clc.find_one({'studentid':studentid, 'checkliste':self.context.UID()}, sort=[( '_id', pymongo.DESCENDING )])

        if formdata:
            data = formdata.get('data')
        print data
        return data

    def form_url(self):
        return self.context.absolute_url() + '/validate-checklist'

    def __call__(self):
        self.msg = _(u'A small message')
        return self.index()
