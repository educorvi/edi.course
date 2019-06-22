# -*- coding: utf-8 -*-

from edi.course import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.supermodel import model
from plone.autoform import directives as form
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


class IKursnotizMarker(Interface):
    pass

class INotizData(model.Schema):

    title = schema.TextLine(
        title=u'Titel der Notiz im Notizbuch')

    description = schema.Text(
        title=u'Frage, These oder Aufgabe zu der sich der Lernende eine Notiz machen soll')


@provider(IFormFieldProvider)
class IKursnotiz(model.Schema):
    """
    """

    model.fieldset(
        'notizen',
        label=u"Notizen zum Inhalt",
        fields=['notizen',]
    )

    form.widget('notizen', DataGridFieldFactory)
    notizen = schema.List(title=u'Fragen, Thesen oder Aufgaben für Notizen',
        description=u'Gib hier Fragen, Thesen oder Aufgaben zu denen sich der Lernende Notizen machen soll.',
        value_type = DictRow(title=u'Optionen', schema=INotizData))

