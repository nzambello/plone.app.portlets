from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.app.component.hooks import setHooks, setSite

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.portlets.login import LoginPortletAssignment
from plone.app.portlets.portlets.login import LoginPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from plone.app.portlets.tests.base import PortletsTestCase

class TestLoginPortlet(PortletsTestCase):

    def afterSetUp(self):
        setHooks()
        setSite(self.portal)

    def testPortletTypeRegistered(self): 
        portlet = getUtility(IPortletType, name='portlets.Login')
        self.assertEquals(portlet.addview, 'portlets.Login')

    def testInterfaces(self): 
        portlet = LoginPortletAssignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='portlets.Login')
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        
        adding = getMultiAdapter((mapping, request,), name='+')
        addview = getMultiAdapter((adding, request), name=portlet.addview)
        
        # This is a NullAddForm - calling it does the work
        addview()
        
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], LoginPortletAssignment))
        
    def testInvokeEditView(self): 
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        
        mapping['foo'] = LoginPortletAssignment()
        editview = queryMultiAdapter((mapping['foo'], request), name='edit.html', default=None)
        self.failUnless(editview is None)

    def testRenderer(self): 
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = LoginPortletAssignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, LoginPortletRenderer))
        
class TestLoginPortletRenderer(PortletsTestCase):
    
    def afterSetUp(self):
        setHooks()
        setSite(self.portal)
    
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = assignment or LoginPortletAssignment()

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
    
    def testAvailable(self): 
        r = self.renderer()
        self.assertEquals(True, r.available())
        self.portal.acl_users._delObject('credentials_cookie_auth')
        self.assertEquals(False, r.available())

    def testShow(self): 
        r = self.renderer()
        self.assertEquals(False, r.show())
        self.logout()
        self.assertEquals(True, r.show())
        
        request = self.folder.REQUEST
        request['URL'] = self.portal.absolute_url() + '/login_form'
        self.assertEquals(False, self.renderer(request=request).show())
        
        request['URL'] = self.portal.absolute_url() + '/join_form'
        self.assertEquals(False, self.renderer(request=request).show())
        
    # TODO: Add more detailed tests here
    
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLoginPortlet))
    suite.addTest(makeSuite(TestLoginPortletRenderer))
    return suite