from plone.app.layout.viewlets import common as base
from Products.CMFCore.interfaces import ISiteRoot
from plone import api as ploneapi
from edi.course.persistance import updateVisitedData

class CourseWayViewlet(base.ViewletBase):

    def getAcquisitionChain(self, object):
        inner = object.aq_inner
        iter = inner
        while iter is not None:
            yield iter
            if ISiteRoot.providedBy(iter):
                break
            if not hasattr(iter, "aq_parent"):
                raise RuntimeError("Parent traversing interrupted by object: " + str(parent))
            iter = iter.aq_parent

    def getCourse(self):
        """ get the CourseObject
        """
        parentobjects = self.getAcquisitionChain(self.context)
        for i in parentobjects:
            if i.portal_type == "Kurs":
                return i
        return ""

    def getCourseWay(self):
        course = self.getCourse()
        current = (self.context.title, self.context.absolute_url())
        vorgaenger = ()
        nachfolger = ()
        if course:
            way = [course] + [i.getObject() for i in course.getCourseItemsInOrder()]
            currentindex = way.index(self.context)
            if currentindex != 0 and currentindex != (len(way) - 1):
                vorgaenger = (way[currentindex-1].title, way[currentindex-1].absolute_url())
                nachfolger = (way[currentindex+1].title, way[currentindex+1].absolute_url())
            if currentindex == (len(way) -1):
                vorgaenger = (way[currentindex-1].title, way[currentindex-1].absolute_url())
        return {'current':current, 'vorgaenger':vorgaenger, 'nachfolger':nachfolger}

    def cookiegetter(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        return session.get("qrdata", {})

    def updateData(self):
        """ Aktualisiert die persistierten Daten des Benutzers
        """
        coursetests = ['Aufgabe']
        if self.context.portal_type != u"Kurs":
            userid = ploneapi.user.get_current().getId()
            kurs = self.getCourse()
            uid = self.context.UID()
            retdict = {}
            finished = False
            if self.context.portal_type in coursetests and 'validate' in self.request.getURL():
                if self.context.art == 'benotet':
                    retdict = self.cookiegetter()
            if self.context.portal_type == 'Kursabschluss':
                finished = True
            update = updateVisitedData(kurs, userid, uid, retdict, finished)

    def render(self):
        """ Render viewlet only if it is enabled.
        """
        if "folder_contents" in self.request.getURL():
            return ""
        if "sharing" in self.request.getURL():
            return ""
        if self.context.portal_type == "Kurs":
            return ""
        parentobjects = self.getAcquisitionChain(self.context)
        for i in parentobjects:
            if i.portal_type == "Kurs":
                self.updateData()
                return super(CourseWayViewlet, self).render()
        return ""
