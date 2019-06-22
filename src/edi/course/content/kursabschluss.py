# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.interface import invariant


class IKursabschluss(model.Schema):
    """ Marker interface and Dexterity Python Schema for Kursabschluss
    """

    text = RichText(title=u"Haupttext zur Beendigung des Online-Kurses.",
                    required=True)

    misserfolg = schema.Text(title=u"Text bei Misserfolg",
                             default=u"Leider liegt ihr Ergebnis unterhalb der Mindestanforderung für die Erlangung eines\
                                      Zertifikates. Sie haben jedoch die Möglichkeit, den Kurs zu wiederholen. Wir wünschen\
                                      Ihnen dabei viel Erfolg.",
                             required=False)

    image = NamedBlobImage(title=u"Bild des Zertifikats",
                           description=u"Das Bild bildet den Hintergrund des PDF-Dokuments mit dem\
                           Zertifikat",
                           required=False)

    #punkte = schema.Int(title=u"Notwendige Punktzahl für das Zertifikat",
    #                    description=u"Angabe, welche Punktzahl für den Druck eines Zertifikats erreicht\
    #                    werden musste. 0 Punkte heisst - das Zertifikat wird ohne Bedingungen am Ende des Kurses\
    #                    zum Ausdruck angeboten.",
    #                    default=0,
    #                    required=True)

    print_name = schema.Bool(title=u"Aktivieren, wenn der Name auf das Zertifikat gedruckt werden soll.",
                             description=u"Das Feld wird nur berücksichtigt, wenn der Zertifikatsdruck aktiviert wurde.")

    name_x = schema.Float(title=u"X-Koordinate für den Druck des Namens in cm.",
                          description=u"Angabe der X-Koordinate für den Druck des Namens auf das Zertifikat.\
                          Bitte vom linken unteren Blattrand aus messen (virtueller 0-Punkt des Koordinatensystems).",
                          default=7.0)

    name_y = schema.Float(title=u"Y-Koordinate für den Druck des Namens in cm.",
                          description=u"Angabe der Y-Koordinate für den Druck des Namens auf das Zertifikat.\
                          Bitte vom linken unteren Blattrand aus messen (virtueller 0-Punkt des Koordinatensystems).",
                          default=14.0)

    name_fontsize = schema.Int(title=u"Schriftgröße in pt für den Druck des Namens auf das Zertifikat.",
                               default=30)

    print_datum = schema.Bool(title=u"Aktivieren, wenn das Datum auf das Zertifikat gedruckt werden soll.",
                             description=u"Das Feld wird nur berücksichtigt, wenn der Zertifikatsdruck aktiviert wurde.")

    datum_x = schema.Float(title=u"X-Koordinate für den Druck des Datums in cm.",
                          description=u"Angabe der X-Koordinate für den Druck des Datums auf das Zertifikat.\
                          Bitte vom linken unteren Blattrand aus messen (virtueller 0-Punkt des Koordinatensystems).",
                          default=5.0)

    datum_y = schema.Float(title=u"Y-Koordinate für den Druck des Datums in cm.",
                          description=u"Angabe der Y-Koordinate für den Druck des Datums auf das Zertifikat.\
                          Bitte vom linken unteren Blattrand aus messen (virtueller 0-Punkt des Koordinatensystems).",
                          default=8.0)

    datum_fontsize = schema.Int(title=u"Schriftgröße in pt für den Druck des Datums auf das Zertifikat.",
                                default=14)


    print_certid = schema.Bool(title=u"Aktivieren, wenn eine auf das Zertifikats-ID gedruckt werden soll.",
                             description=u"Das Feld wird nur berücksichtigt, wenn der Zertifikatsdruck aktiviert wurde.")

    certid_x = schema.Float(title=u"X-Koordinate für den Druck der Zertifikats-ID in cm.",
                          description=u"Angabe der X-Koordinate für den Druck der Zertifikats-ID auf das Zertifikat.\
                          Bitte vom linken unteren Blattrand aus messen (virtueller 0-Punkt des Koordinatensystems).",
                          default=5.0)

    certid_y = schema.Float(title=u"Y-Koordinate für den Druck der Zertifikats-ID in cm.",
                          description=u"Angabe der Y-Koordinate für den Druck der Zertifikats-ID auf das Zertifikat.\
                          Bitte vom linken unteren Blattrand aus messen (virtueller 0-Punkt des Koordinatensystems).",
                          default=6.0)

    certid_fontsize = schema.Int(title=u"Schriftgröße in pt für den Druck der Zertifikats-ID auf das Zertifikat.",
                                default=14)


    #@invariant
    #def zertifikat_invariant(data):
    #    if data.zertifikat:
    #        if not data.image:
    #            raise Invalid(u'Für den Druck des Zertifikats wird ein Hintergrundbild benötigt.')

    @invariant
    def name_invariant(data):
        if data.print_name: 
            if not data.name_x or not data.name_y or not data.name_fontsize:
                raise Invalid(u'Bitte machen Sie alle notwendigen Angaben für den Druck des Namens.')

    @invariant
    def name_invariant(data):
        if data.print_datum: 
            if not data.datum_x or not data.datum_y or not data.datum_fontsize:
                raise Invalid(u'Bitte machen Sie alle notwendigen Angaben für den Druck des Datums.')


@implementer(IKursabschluss)
class Kursabschluss(Item):
    """
    """
