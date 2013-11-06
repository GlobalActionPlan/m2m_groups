import unittest

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from madetomeasure.models.organisation import Organisation

from m2m_groups.interfaces import IGroups


class GroupsTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from m2m_groups.models import Groups
        return Groups

    def test_verify_class(self):
        self.failUnless(verifyClass(IGroups, self._cut))

    def test_verify_object(self):
        self.failUnless(verifyObject(IGroups, self._cut(Organisation())))

    def test_add(self):
        obj = self._cut(Organisation())
        obj['hello'] = {1: 'world'}
        self.assertEqual(dict(obj['hello']), {1: 'world'})
