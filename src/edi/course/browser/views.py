# -*- coding: utf-8 -*-
from plone import api as ploneapi
from Products.Five import BrowserView
from edi.course.persistance import einschreiben, getStudentData, resetUserData

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
        if len(courseitems) > 1:
            button['buttonurl'] = self.context.getCourseItemsInOrder()[1].getURL()
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
