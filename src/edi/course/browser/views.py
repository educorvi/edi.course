# -*- coding: utf-8 -*-
import tempfile
import hashlib
from plone import api as ploneapi
from Products.Five import BrowserView
from edi.course.pdfgen import createpdf
from edi.course.persistance import einschreiben, getStudentData, resetUserData, getFinalData
from edi.course.persistance import getGlobalStats, resetComplete

def sizeof_fmt(num, suffix='Byte'):
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)

class TestView(BrowserView):

    def test(self):
        """Return a catalog search result of sessions to show."""


class CourseView(BrowserView):
    """Die Ansicht der Startseite eines Online-Kurses."""

    def checkStudentData(self):
        """Holt die Daten des Studenten aus der MongoDB"""
        studentid = ploneapi.user.get_current().getId()
        data = getStudentData(self.context, studentid)
        return data

    def getStartButton(self):
        """Setzt den Startbutton je nach Lernfortschritt"""
        button = {}
        button['class'] = 'btn btn-success'
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
            button['class'] = 'btn btn-warning'
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
        if self.context.ccreators:
            for i in self.context.ccreators:
                creator = {}
                author = ploneapi.user.get(username = i)
                if author:
                    creator['fullname'] = author.getProperty('fullname')
                    creator['email'] = author.getProperty('email')
                    creator['biography'] = ''
                    biography = author.getProperty('description')
                    if biography:
                        creator['biography'] = biography
                    userid = author.getId()
                    pm = ploneapi.portal.get_tool(name='portal_membership')
                    creator['image'] = pm.getPersonalPortrait(id=userid).absolute_url()
                    creators.append(creator)
        return creators

    def getLerneinheiten(self):
        """liest die Lerneinheiten aus dem aktuellen Kurs zur
           Abbildung eines Inhaltsverzeichnisses
        """
        einheiten = []
        for i in self.context.getFolderContents():
            if i.portal_type == "Lerneinheit":
                einheit = {'title':i.Title,
                           'url':i.getURL()}
                einheiten.append(einheit)
        return einheiten

    def getSkills(self):
        """liest die Skills aus dem aktuellen Kurs zur
           Abbildung eines Inhaltsverzeichnisses
        """
        skills = []
        for i in self.context.getFolderContents():
            if i.portal_type == "Skill":
                skill = {'title':i.Title,
                         'url':i.getURL()}
                skills.append(skill)
        return skills

    def getZertifikat(self):
        cert = {}
        cert['cert'] = self.context.zertifikat
        cert['max'] = self.context.getMaxPunkte()
        cert['quorum'] = self.context.quorum
        return cert 

    def getSumAufwand(self):
        return self.context.getEffort()


class UnitView(BrowserView):
    """Viewklasse fuer die Lerneinheit"""

    def folderContents(self):
        glyphclasses = {'Document':'glyphicon glyphicon-bookmark',
                        'Aufgabe':'glyphicon glyphicon-check',
                        'Checkliste':'glyphicon glyphicon-ok',
                        'Audiovideo':'glyphicon glyphicon-play-circle'}

        fontsizes = {'Document':'font-size:110%;',
                     'Aufgabe':'font-size:110%;',
                     'Checkliste':'font-size:110%',
                     'Audiovideo':'font-size:110%;'}

        showtypes = ['Document', 'Aufgabe', 'Audiovideo', 'Checkliste']
        retlist = []
        for i in self.context.getFolderContents():
            if i.portal_type in showtypes:
                content = {}
                content['glyph'] = glyphclasses.get(i.portal_type)
                content['fontsize'] = fontsizes.get(i.portal_type)
                content['title'] = i.Title
                content['url'] = i.getURL()
                retlist.append(content)
        return retlist

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
        buttonurl = ''
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
        quorum = self.context.aq_parent.quorum
        maxpunkte = self.context.aq_parent.getMaxPunkte()
        repeat = self.context.aq_parent.repeat
        if repeat:
            repeaturl = self.context.aq_parent.absolute_url() + '/@@reset'
        else:
            repeaturl = ''
        certfail = False
        if summe >= quorum and self.context.aq_parent.zertifikat:
            #be sure - you will never cheat the certprint
            user = ploneapi.user.get_current()
            fullname = user.getProperty('fullname')
            if not fullname:
                fullname = user.getId()
            hash_object = hashlib.md5(fullname.encode('utf-8'))
            urlid = hash_object.hexdigest()
            buttonurl = self.context.absolute_url() + '/@@printcert/?urlid=%s' %urlid
            button = True
        elif summe <= quorum and self.context.aq_parent.zertifikat:
            certfail = True
        return {'gesamtpunkte':summe, 
                'max':maxpunkte,
                'fail': certfail,
                'ergebnisse':ergebnisse,
                'button':button,
                'buttonurl':buttonurl,
                'repeat': repeaturl
                }
                

class PrintCertificate(BrowserView):
    """Druck des Zertifikats."""

    def __call__(self):
        
        #1st check if someone tries to cheat the certprint
        user = ploneapi.user.get_current()
        fullname = user.getProperty('fullname')
        if not fullname:
            fullname = user.getId()
        hash_object = hashlib.md5(fullname.encode('utf-8'))
        urlid = hash_object.hexdigest()

        gotid = self.request.get('urlid')
        
        if urlid != gotid:
            ploneapi.portal.show_message('Sie sind nicht zum Zertifikatsdruck berechtigt.', self.request, type='error')
            return self.request.response.redirect(self.context.absolute_url())

        image = u'%s/@@download/image/%s' %(self.context.absolute_url(), self.context.image.filename)
        data = {'imageurl': image}

        studentdata = getFinalData(self.context)
        data['print_datum'] = self.context.print_datum
        data['datum'] = studentdata.get('lastchange').strftime('%d.%m.%Y')
        data['datum_x'] = self.context.datum_x
        data['datum_y'] = self.context.datum_y
        data['datum_fontsize'] = self.context.datum_fontsize
        
        user = ploneapi.user.get_current()
        data['print_name'] = self.context.print_name
        data['name'] = user.getProperty('fullname')
        data['name_x'] = self.context.name_x
        data['name_y'] = self.context.name_y
        data['name_fontsize'] = self.context.name_fontsize

        kursid = self.context.aq_parent.id
        data['print_certid'] = self.context.print_certid
        certid = u'%s %s' %(kursid, user.getProperty('fullname'))
        data['certid'] = hashlib.md5(certid.encode('utf-8')).hexdigest()
        data['certid_x'] = self.context.certid_x
        data['certid_y'] = self.context.certid_y
        data['certid_fontsize'] = self.context.certid_fontsize

        filehandle = tempfile.TemporaryFile()

        pdf = createpdf(filehandle, data)
        pdf.seek(0)

        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-disposition', 'attachment; filename=zertifikat.pdf')
        return pdf.read()

class GlobalStatsView(BrowserView):

    def getCourseData(self):
        data = getGlobalStats(self.context)
        return data

class UserStatsView(BrowserView):

    def getUserData(self):
        studentid = self.request.get('user')
        data = getStudentData(self.context, studentid)
        entry = {}
        entry['studentid'] = studentid
        user = ploneapi.user.get(userid = studentid)
        entry['fullname'] = user.getProperty('fullname')
        entry['email'] = user.getProperty('email')
        visitedcontent = [ploneapi.content.get(UID=i) for i in data.get('visited')]
        entry['visited'] = [(i.title, i.absolute_url()) for i in visitedcontent]
        entry['lastchange'] = data.get('lastchange').strftime('%d.%m.%Y %H:%M')
        ergebnisse = []
        summe = 0
        tests = data.get('tests')
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
        entry['ergebnisse'] = ergebnisse
        entry['gesamtpunkte'] = summe
        return entry

class AudioVideoView(BrowserView):

    def getMedia(self):
        datei = {}
        if self.context.datei:
            datei = {}
            datei['url'] = "%s/@@download/datei/%s" %(self.context.absolute_url(), self.context.datei.filename)
            if self.context.datei.contentType.startswith('audio'):
                datei['contentType'] = 'audio/mpeg'
            else:
                datei['contentType'] = self.context.datei.contentType
            datei['size'] = sizeof_fmt(self.context.datei.size)
            datei['filename'] = self.context.datei.filename
        return datei

    def getEmbed(self):
        retcode = ''
        if self.context.embed:
            retcode = self.context.embed
        return retcode

    def getPoster(self):
        image = {}
        if self.context.poster:
            image['src'] = "%s/@@images/poster" % self.context.absolute_url()
            image['title'] = self.context.poster.filename
        return image
            

class ResetView(BrowserView):

    def __call__(self):
        message = u"Die Daten des Benutzers im aktuellen Kurs wurden gelöscht. Mit der Bearbeitung des Kurses kann erneut begonnen werden."
        errmessage = u"Beim Löschen der Benutzerdaten ist leider ein Fehler aufgetreten."
        studentid = ploneapi.user.get_current().getId()
        kurs = self.context
        update = resetUserData(kurs, studentid)
        if update:
            ploneapi.portal.show_message(message=message, request=self.request, type='info')
        else:
            ploneapi.portal.show_message(message=errmessage, request=self.request, type='error')
        return self.request.response.redirect(self.context.absolute_url())

class ResetCompleteView(BrowserView):

    def __call__(self):
        message = u"Sie haben die ALLE Benutzerdaten zurückgesetzt."
        studentid = ploneapi.user.get_current().getId()
        kurs = self.context
        update = resetComplete(kurs, studentid)
        ploneapi.portal.show_message(message=message, request=self.request, type='info')
        return self.request.response.redirect(self.context.absolute_url())

class setFloat(BrowserView):

    def __call__(self):
        message = u"Es wurden alle Lerneinheiten korrigiert."
        brains = ploneapi.content.find(portal_type="Lerneinheit")
        for i in brains:
            obj = i.getObject()
            obj.effort = 1.0
        ploneapi.portal.show_message(message=message, request=self.request, type='info')
        return self.request.response.redirect(self.context.absolute_url())
