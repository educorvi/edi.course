# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer

class NotizViewlet(ViewletBase):

    def get_action(self):
        return self.context.absolute_url() + '/validate_notizen'
   

    def get_notizen(self):
        normalizer = getUtility(IIDNormalizer)
        if hasattr(self.context, 'notizen'):
            if self.context.notizen:
                notizen = []
                for i in self.context.notizen:
                    i['name'] = normalizer.normalize(i['title'])
                    notizen.append(i)
                return notizen
        return []

    def render(self):
        if self.get_notizen():
            return super(NotizViewlet, self).render()
        return ''
