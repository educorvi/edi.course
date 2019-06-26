# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.autoform import directives as form
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from zope import schema
from zope.interface import implementer


class IAussagen(model.Schema):

    aussage = schema.TextLine(title=u"Aussage oder Punkt auf der Checkliste",
                        required=True)

class IOptionen(model.Schema):

    option = schema.TextLine(title=u"Antwortoption",
                        required=True)
    faktor = schema.Int(title=u"Punkte",
                        default=1,
                        required=True)

class ICheckliste(model.Schema):
    """ Marker interface and Dexterity Python Schema for Checkliste
    """

    text = RichText(
        title=u'Text',
        required=False
    )

    form.widget('aussagen', DataGridFieldFactory)
    aussagen = schema.List(title=u'Aussagen für die Checkliste',
        description=u'Gib hier die Aussagen ein, die der Lernende mit den nachfolgenden Optionen beantworten soll.',
        value_type = DictRow(title=u'Aussagen', schema=IAussagen))

    summe = schema.Bool(title=u"Auswertung der Checkliste",
                        description=u"Nur bei gesetztem Haken findet eine Punkte Auswertung der Checkliste statt.",
                        default=True)

    form.widget('optionen', DataGridFieldFactory)
    optionen = schema.List(title=u'Antwortoptionen für die Checkliste',
        description=u'Gib hier die Antwortoptionen und die entsprechende Punktzahl ein. Die Punkte werden ignoriert wenn die Auswertung der\
                      Checkliste deaktiviert wurde.',
        value_type = DictRow(title=u'Antwortoptionen', schema=IOptionen))


@implementer(ICheckliste)
class Checkliste(Item):
    """
    """
