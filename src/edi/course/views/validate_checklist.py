# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api as ploneapi
from edi.course.persistance import getCourse
from edi.course.mongoutil import get_mongo_client

class ValidateChecklist(BrowserView):

    def calculate_summe(self):
        summe = 0
        factordict ={}
        for i in self.context.optionen:
            factordict[i.get('option')] = i.get('faktor')
        for k in self.context.aussagen:
            eingabe = self.request.form.get(str(self.context.aussagen.index(k)))
            ergebnis = factordict.get(eingabe, 0)
            summe += ergebnis
        return summe

    def __call__(self):
        kurs = getCourse(self.context)
        mongoclient = get_mongo_client()
        cdb = mongoclient[kurs.id]
        clc = cdb.checklist_collection
        studentid = ploneapi.user.get_current().getId()
        summe = None
        if self.context.summe:
            summe = self.calculate_summe()
        if self.request.form:
            checklistpost = {'studentid':studentid, 
                             'checkliste':self.context.UID(), 
                             'data': self.request.form,
                             'summe': summe}
            clc_id = clc.insert_one(checklistpost).inserted_id
            if clc_id:
                ploneapi.portal.show_message(message='Ihre Eingaben zu dieser Checkliste wurden erfolgreich gespeichert.', 
                                             request=self.request,
                                             type='info')
        url = self.context.absolute_url()
        return self.request.response.redirect(url)
