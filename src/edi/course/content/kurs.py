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
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.navtree import NavtreeStrategyBase
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy, DefaultNavtreeStrategy

# from edi.course import _

class IKurs(model.Schema):
    """ Marker interface and Dexterity Python Schema for Kurs
    """

    titleimage = NamedBlobImage(title = u"Titelbild für den Kurs",
                               description = u"Das Titelbild wird in allen Kursübersichten angezeigt.",
                               required = True)

    logoimage = NamedBlobImage(title = u"Logo der Bildungseinrichtung",
                              required = False)

    institution = schema.TextLine(title = u"Name der Bildungseinrichtung",
                                  required = True)

    url = schema.URI(title = u"Link zur Homepage der Bildungseinrichtung",
                     required = True)

    about = RichText(title = u"Über diesen Kurs",
                     description = u"Beschreibung der Inhalte des Online-Kurses.",
                     required = False)

    goals = RichText(title = u"Lernziele im Kurs",
                     description = u"Beschreibung was der Kursteilnehmer lernen kann.",
                     required = False)

    ccreators = schema.List(title = u"Autoren des Kurses",
                     description = u"Bitte hier nur den Anmeldenamen des Autors eintragen. Die Daten werden\
                       aus dem individuellen Benutzerprofil des Kursautors gelesen.",
                     value_type = schema.TextLine(),
                     required = True)

    length = schema.TextLine(title = u"Dauer des Kurses",
                             required = True)

    effort = schema.TextLine(title = u"Zeitbedarf für die Teilnehmer",
                             required = True)


    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )


@implementer(IKurs)
class Kurs(Container):
    """
    """

    def getCourseItemsInOrder(self):
        """
            Create a flattened out list of portal_catalog queried items in their natural depth first navigation order.
            @param root: Content item which acts as a navigation root
            @param query: Dictionary of portal_catalog query parameters
            @return: List of catalog brains
        """
        root = self
        query = {'portal_type':['Kurs', 'Kursabschluss', 'Lerneinheit', 'Document', 'Aufgabe', 'Audiovideo']}

        # Navigation tree base portal_catalog query parameters
        applied_query=  {
            'path' : '/'.join(root.getPhysicalPath()),
            'sort_on' : 'getObjPositionInParent'
        }

        # Apply caller's filters
        applied_query.update(query)

        # Set the navigation tree build strategy
        # - use navigation portlet strategy as base
        #strategy = DefaultNavtreeStrategy(root)
        strategy = NavtreeStrategyBase()
        strategy.rootPath = '/'.join(root.getPhysicalPath())
        strategy.showAllParents = False
        strategy.bottomLevel = 999
        # This will yield out tree of nested dicts of
        # item brains with retrofitted navigational data
        tree = buildFolderTree(root, root, query, strategy=strategy)

        items = []

        def flatten(children):
            """ Recursively flatten the tree """
            for c in children:
                # Copy catalog brain object into the result
                items.append(c["item"])
                children = c.get("children", None)
                if children:
                    flatten(children)

        flatten(tree["children"])
        return items
