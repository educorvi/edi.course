# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer

class ILerneinheit(model.Schema):
    """ Marker interface for Lerneinheit
    """

    effort = schema.Float(title=u"Zeitbedarf für diese Lerneinheit in Stunden",
                          required=True)

    goals = RichText(title=u"Lernziel der Einheit",
                     description=u"Kurze Beschreibung welches Lernziel mit dieser Einzeit erreicht werden soll.",
                     required=False)

@implementer(ILerneinheit)
class Lerneinheit(Container):
    """ Content-Klasse der Lerneinheit
    """
