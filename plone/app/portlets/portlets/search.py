# -*- coding: utf-8 -*-
from plone import api
from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implementer


class ISearchPortlet(IPortletDataProvider):
    """ A portlet displaying a (live) search box
    """

    enableLivesearch = schema.Bool(
        title=_(u"Enable LiveSearch"),
        description=_(u"Enables the LiveSearch feature, which shows "
                      u"live results if the browser supports "
                      u"JavaScript."),
        default=True,
        required=False)


@implementer(ISearchPortlet)
class Assignment(base.Assignment):

    def __init__(self, enableLivesearch=True):
        self.enableLivesearch = enableLivesearch

    @property
    def title(self):
        return _(u"Search")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('search.pt')
    action = '@@search'
    livesearch_action = 'livesearch_reply'

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        portal_state = getMultiAdapter(
            (context, request), name='plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()

    def enable_livesearch(self):
        return self.data.enableLivesearch

    def search_action(self):
        return '{0}/{1}'.format(self.navigation_root_url, self.action)

    def navigation_root_url(self):
        return api.portal.get_navigation_root()


class AddForm(base.AddForm):
    schema = ISearchPortlet
    label = _(u"Add Search Portlet")
    description = _(u"This portlet shows a search box.")

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    schema = ISearchPortlet
    label = _(u"Edit Search Portlet")
    description = _(u"This portlet shows a search box.")
