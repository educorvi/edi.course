# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from plone import api as ploneapi
from edi.course.persistance import getCourse
from edi.course.persistance import mongoclient


class ValidateChecklist(BrowserView):

    def __call__(self):
        kurs = getCourse(self.context)
        cdb = mongoclient[kurs.id]
        clc = cdb.checklist_collection
        studentid = ploneapi.user.get_current().getId()
        import pdb;pdb.set_trace()
