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

    option = schema.TextLine(title=u"Option zur Auswahl durch den Benutzer",
                        required=True)
    faktor = schema.Int(title=u"Die Option geht mit dem Faktorwert in die Berechnung ein.",
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

    form.widget('optionen', DataGridFieldFactory)
    optionen = schema.List(title=u'Antwortoptione für die Checkliste',
        description=u'Gib hier die Antwortoptionen ein, mit denen der Lernende die Punkte der Checkliste beantworten soll.',
        value_type = DictRow(title=u'Antwortoptionen', schema=IOptionen))


@implementer(ICheckliste)
class Checkliste(Item):
    """
    """
