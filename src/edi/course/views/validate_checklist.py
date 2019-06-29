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
        print self.request.form
        if self.request.form:
            checklistpost = {'studentid':studentid, 
                             'checkliste':self.context.UID(), 
                             'data': self.request.form}
            clc_id = clc.insert_one(checklistpost).inserted_id
            if clc_id:
                ploneapi.portal.show_message(message='Ihre Eingaben zu dieser Checkliste wurden erfolgreich gespeichert.', 
                                             request=self.request,
                                             type='info')
        url = self.context.absolute_url()
        return self.request.response.redirect(url)
