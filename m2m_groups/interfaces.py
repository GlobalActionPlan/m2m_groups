from zope.interface import Attribute
from zope.interface import Interface


class IGroups(Interface):
    """ Groups adapter """

    def __init__(context):
        """ Context to adapt. """

    def keys():
        """ Regular dict api. """

    def __iter__():
        """ Regular dict api. """

    def values():
        """ Regular dict api. """

    def items():
        """ Regular dict api. """

    def __len__():
        """ Regular dict api. """

    def __nonzero__():
        """ Important for Zope objects - don't remove this! """

    def __getitem__(name):
        """ Regular dict api. """

    def get(name, default=None):
        """ Regular dict api. """

    def __contains__(name):
        """ Regular dict api. """

    def __setitem__(name, value):
        """ Regular dict api. """

    def __delitem__(name):
        """ Regular dict api. """

    def __repr__():
        """ Usefull for debugging """
