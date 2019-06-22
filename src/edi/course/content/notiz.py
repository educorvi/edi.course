# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class INotiz(model.Schema):
    """ Marker interface and Dexterity Python Schema for Notiz
    """
    
    notiz = schema.Text(title=u'Notiz')

    link = schema.URI(title=u'URL der Referenz')

@implementer(INotiz)
class Notiz(Item):
    """
    """
