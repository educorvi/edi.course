# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView


class ValidateNotizen(BrowserView):
    def __call__(self):
        template = '''<li class="heading" i18n:translate="">
          Sample View
        </li>'''
        return template