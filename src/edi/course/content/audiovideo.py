# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobFile, NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

class IAudioVideo(model.Schema):
    """ Marker interface and Dexterity Python Schema for Audio Video
    """

    vortext = RichText(title=u"Strukturierter Text vor dem Audio oder Video", 
                       required=False)

    datei = NamedBlobFile(title=u"Audio- oder Video-Datei",
                          description=u"Möglichkeit zum Hochladen einer Audiodatei im *.mp3 Format oder Videodatai im *.mp4 Format.",
                          required=False)

    poster = NamedBlobImage(title=u"Vorschaubild für Video-Datei",
                        description=u"Möglichkeit zum Hochladen eines Vorschaubildes für das Video.",
                        required=False)

    embed = schema.Text(title=u"Einbettungscode einer Videoplattform",
                        description=u"Als Alternative zur Datei kann hier ein Einbettungscode einer Videoplattform\
                                    z.B. YouTube, Vimeo eingetragen werden.",
                        required=False)

    nachtext = RichText(title=u"Strukturierter Text nach dem Audio oder Video",
                        required=False)
  

@implementer(IAudioVideo)
class Audiovideo(Item):
    """
    """
