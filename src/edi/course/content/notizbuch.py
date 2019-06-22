# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class INotizbuch(model.Schema):
    """ Marker interface and Dexterity Python Schema for Notizbuch
    """

@implementer(INotizbuch)
class Notizbuch(Container):
    """
    """
