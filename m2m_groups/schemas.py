import colander
from betahaus.pyracont.decorators import schema_factory

from . import m2m_groups_tsf as _

class MembersSchema(colander.SequenceSchema):
    members = colander.SchemaNode(colander.String(),
                                  title = _(u"Member emails"),
                                  description = _(u"Add one address per field"),
                                  validator = colander.Email())

class ManagersSchema(colander.SequenceSchema):
    managers = colander.SchemaNode(colander.String(),
                                  title = _(u"Managers UserIDs"),
                                  description = _(u"Add one per field"))


@schema_factory('GroupSchema')
class GroupSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                title = _(u"Group name"),)
    description = colander.SchemaNode(colander.String(),
                                      title = _(u"Description"))
    members = MembersSchema()
    managers = ManagersSchema()
