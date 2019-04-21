# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


# from edi.course import _


class IKursabschluss(model.Schema):
    """ Marker interface and Dexterity Python Schema for Kursabschluss
    """

    text = RichText(title=u"Haupttext zur Beendigung des Online-Kurses.",
                    required=True)

    zertifikat = schema.Bool(title=u"Aktivieren, wenn ein Zertifikatsdruck gewünscht ist.")

    image = NamedBlobImage(title=u"Bild des Zertifikats",
                           description=u"Das Bild bildet den Hintergrund des PDF-Dokuments mit dem\
                           Zertifikat",
                           required=False)

    punkte = schema.Int(title=u"Notwendige Punktzahl für das Zertifikat",
                        description=u"Angabe, welche Punktzahl für den Druck eines Zertifikats erreicht\
                        werden musste.",
                        required=False)

    name_x = schema.Float(title=u"X-Koordinate für den Druck des Namens in cm.",
                          description=u"Angabe der X-Koordinate für den Druck des Namens auf das Zertifikat.")

    name_y = schema.Float(title=u"Y-Koordinate für den Druck des Namens in cm.",
                          description=u"Angabe der Y-Koordinate für den Druck des Namens auf das Zertifikat.")

    datum_x = schema.Float(title=u"X-Koordinate für den Druck des Datums in cm.",
                          description=u"Angabe der X-Koordinate für den Druck des Datums auf das Zertifikat.")

    datum_y = schema.Float(title=u"Y-Koordinate für den Druck des Datums in cm.",
                          description=u"Angabe der Y-Koordinate für den Druck des Datums auf das Zertifikat.")

    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IKursabschluss)
class Kursabschluss(Item):
    """
    """
