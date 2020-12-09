# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView

from plone.z3cform import layout
from plone.supermodel import model
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

class IEdiCourseSettings(model.Schema):
    """ Define settings data structure """

    dbuser = schema.TextLine(title=u"Datenbank-Benutzer zum Schreiben von Kursdaten")
    dbpassword = schema.Password(title=u"Passwort für den Datenbank-Benutzer")

class CourseSettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IEdiCourseSettings
    label = u"Einstellungen edi.course"

EdiCourseSettingsView = layout.wrap_form(CourseSettingsEditForm, ControlPanelFormWrapper)
EdiCourseSettingsView.label = u"Einstellungen edi.course"
