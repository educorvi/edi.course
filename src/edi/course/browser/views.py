# -*- coding: utf-8 -*-
import tempfile
from plone import api as ploneapi
from Products.Five import BrowserView
from edi.course.pdfgen import createpdf
from edi.course.persistance import einschreiben, getStudentData, resetUserData, getFinalData

class TestView(BrowserView):

    def test(self):
        """Return a catalog search result of sessions to show."""

        import pdb;pdb.set_trace()

class CourseView(BrowserView):
    """Die Ansicht der Startseite eines Online-Kurses."""

    def checkStudentData(self):
        """Holt die Daten des Studenten aus der MongoDB"""
        studentid = ploneapi.user.get_current().getId()
        data = getStudentData(self.context, studentid)
        return data

    def getStartButton(self):
        """Setzt den Startbutton je nach Lernfortschritt"""
        #import pdb;pdb.set_trace()
        button = {}
        courseitems = self.context.getCourseItemsInOrder()
        if courseitems:
            button['buttonurl'] = self.context.getCourseItemsInOrder()[0].getURL()
        else:
            button['buttonurl'] = self.context.absolute_url()
        button['buttonvalue'] = u"Fortsetzen"
        studentdata = self.checkStudentData()
        if not studentdata:
            button['buttonurl'] = self.context.absolute_url() + '/@@einschreiben'
            button['buttonvalue'] = u"Einschreiben"
            return button
        if not studentdata.get('visited'):
            button['buttonvalue'] = u"Start"
            return button
        lastchange = ploneapi.content.get(UID=studentdata.get('visited')[-1])
        if lastchange:
            button['buttonurl'] = lastchange.absolute_url()
        return button

    def getStartEnde(self):
        start = self.context.effective().strftime('%d.%m.%Y')
        ende = self.context.expires().strftime('%d.%m.%Y')
        return (start, ende)

    def getCreators(self):
        creators = []
        for i in self.context.ccreators:
            creator = {}
            author = ploneapi.user.get(userid = i)
            if author:
                creator['fullname'] = author.getProperty('fullname')
                creator['email'] = author.getProperty('email')
                creator['biography'] = ''
                biography = author.getProperty('description')
                if biography:
                    creator['biography'] = biography
                pm = ploneapi.portal.get_tool(name='portal_membership')
                creator['image'] = pm.getPersonalPortrait(id=i).absolute_url()
                creators.append(creator)
        return creators


class UnitView(BrowserView):
    """Viewklasse fuer die Lerneinheit"""

    def folderContents(self):
        return self.context.getFolderContents()


class EinschreibenView(BrowserView):

    def __call__(self):
        message = u"Sie wurden erfolgreich in den Kurs eingeschrieben."
        studentid = ploneapi.user.get_current().getId()
        ret = einschreiben(self.context, studentid)
        if ret:
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
        else:
            ploneapi.portal.show_message(message=errmessage, request=self.request, type='error')
        return self.request.response.redirect(self.context.absolute_url())


class AbschlussView(BrowserView):
    """Die Ansicht der Startseite eines Online-Kurses."""

    def getTestData(self):
        tests = {}
        ergebnisse = []
        summe = 0
        button = False
        studentdata = getFinalData(self.context)
        if studentdata:
            tests = studentdata.get('tests')
        if tests:
            for i in tests.values():
                result = {}
                result['title'] = i.get('title')
                testergebnis = i['outputs']['result']
                result['result'] = u"falsch"
                result['punkte'] = 0
                if testergebnis == True:
                    result['result'] = u"richtig"
                    result['punkte'] = i.get('punkte')
                    summe += i.get('punkte')
                ergebnisse.append(result)
        if summe >= self.context.punkte:
            button = True
        return {'gesamtpunkte':summe, 'ergebnisse':ergebnisse, 'button':button}
                
class PrintCertificate(BrowserView):
    """Druck des Zertifikats."""

    def __call__(self):

        image = u'%s/@@download/image/%s' %(self.context.absolute_url(), self.context.image.filename)

        data = {'imageurl': image}

        studentdata = getFinalData(self.context)
        data['datum'] = studentdata.get('lastchange').strftime('%d.%m.%Y')
        data['datum_x'] = self.context.datum_x
        data['datum_y'] = self.context.datum_y
        
        user = ploneapi.user.get_current()
        data['name'] = user.getProperty('fullname')
        data['name_x'] = self.context.name_x
        data['name_y'] = self.context.name_y

        filehandle = tempfile.TemporaryFile()

        pdf = createpdf(filehandle, data)
        pdf.seek(0)

        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-disposition', 'attachment; filename=zertifikat.pdf')
        return pdf.read()

class ResetView(BrowserView):

    def __call__(self):
        message = u"Sie haben die Benutzerdaten zurückgesetzt."
        studentid = ploneapi.user.get_current().getId()
        kurs = self.context
        update = resetUserData(kurs, studentid)
        if update:
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
        else:
            ploneapi.portal.show_message(message=errmessage, request=self.request, type='error')
        return self.request.response.redirect(self.context.absolute_url())
