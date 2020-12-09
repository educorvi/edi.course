# -*- coding: utf-8 -*-
import pymongo
from edi.course import _
from Products.Five.browser import BrowserView
from plone import api as ploneapi
from edi.course.persistance import getCourse
from edi.course.mongoutil import get_mongo_client

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ChecklisteView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('checkliste_view.pt')

    def get_aussagen(self):
        if self.context.table:
            default = [{u'aussage':u'Aussagen', u'fieldformat':u'keine'}]
            return default + self.context.aussagen
        return self.context.aussagen

    def get_optionen(self):
        optionen = []
        for i in self.context.optionen:
            optionen.append(i.get('option'))
        return optionen

    def get_class(self):
        if len(self.context.optionen) <= 2:
            return 'col-6'
        elif len(self.context.optionen) == 3:
            return 'col-4'
        else:
            return 'col-3'

    def get_bclass(self):
        if len(self.context.optionen) == 1:
            return 'checkbox'
        return 'radio'

    def get_data(self):
        data = {}
        kurs = getCourse(self.context)
        mongoclient = get_mongo_client()
        cdb = mongoclient[kurs.id]
        clc = cdb.checklist_collection
        studentid = ploneapi.user.get_current().getId()
        formdata = clc.find_one({'studentid':studentid, 'checkliste':self.context.UID()}, sort=[( '_id', pymongo.DESCENDING )])
        if formdata:
            data = formdata.get('data')
            data['summe'] = formdata.get('summe')
        return data

    def form_url(self):
        return self.context.absolute_url() + '/validate-checklist'

    def __call__(self):
        self.msg = _(u'A small message')
        return self.index()
