from zope.interface import implementer
from zope.component import adapter
from BTrees.OOBTree import OOBTree
from persistent import Persistent
from madetomeasure.interfaces import IOrganisation

from .interfaces import IGroups
from . import m2m_groups_tsf as _


@adapter(IOrganisation)
@implementer(IGroups)
class Groups(object):
    
    def __init__(self, context):
        self.context = context

    @property
    def _data(self):
        try:
            return self.context.field_storage['m2m_groups_data']
        except KeyError:
            self.context.field_storage['m2m_groups_data'] = OOBTree()
            return self.context.field_storage['m2m_groups_data']

    def keys(self):
        return self._data.keys()

    def __iter__(self):
        return iter(self.keys())

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __len__(self):
        return len(self._data)

    def __nonzero__(self):
        return True

    def __getitem__(self, name):
        return self._data[name]

    def get(self, name, default=None):
        return self._data.get(name, default)

    def __contains__(self, name):
        return self._data.has_key(name)

    def __setitem__(self, name, value):
        if not isinstance(name, basestring):
            raise TypeError("Name must be a string rather than a %s" %
                            name.__class__.__name__)
        if not name:
            raise TypeError("Name must not be empty")
        name = unicode(name)
        if name in self:
            raise KeyError('An object named %s already exists' % name)
        if not isinstance(value, dict):
            raise TypeError("Value, Ie the data stored must be a dict")
        self._data[name] = OOBTree(value)

    def __delitem__(self, name):
        del self._data[name]

    def __repr__(self):
        return u'<Groups adapter containing %s group(s)>' % len(self)

def includeme(config):
    config.registry.registerAdapter(Groups)
