from uuid import uuid4

import deform
import colander
from betahaus.pyracont.factories import createSchema
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from madetomeasure.views.base import BaseView

from madetomeasure.interfaces import IOrganisation
from madetomeasure import security

from m2m_groups.interfaces import IGroups
from . import m2m_groups_tsf as _


@view_defaults(name = "groups", context = IOrganisation)
class GroupsView(BaseView):

    @reify
    def groups(self):
        return self.request.registry.getAdapter(self.context, IGroups)
    
    @view_config(renderer = "templates/listing.pt")
    def list_view(self):
        self.response['groups'] = self.groups
        self.response['can_manage'] = self.can_manage
        return self.response

    @reify
    def is_org_mngr(self):
        return self.context_has_permission(self.context, security.MANAGE_ORGANISATION)

    def can_manage(self, name):
        group = self.groups.get(name, {})
        managers = group.get('managers', ())
        return self.is_org_mngr or self.userid in managers

    def get_form(self, buttons):
        schema = createSchema('GroupSchema')
        schema = schema.bind(context = self.context, request = self.request)
        return deform.Form(schema, buttons = buttons)

    @view_config(request_param = "action=add", renderer = "madetomeasure:views/templates/form.pt")
    def add(self):
        if self.userid is None:
            return HTTPForbidden()
        form = self.get_form(('add',))
        self.response['form_resources'] = form.get_widget_resources()
        if 'add' in self.request.POST:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            name = unicode(uuid4())
            self.groups[name] =  appstruct
            url = self.request.resource_url(self.context, 'groups', query = {'action': 'view', 'name': name})
            return HTTPFound(location = url)
        self.response['form'] = form.render()
        return self.response

    @view_config(request_param = "action=edit", renderer = "madetomeasure:views/templates/form.pt")
    def edit(self):
        name = self.request.GET.get('name')
        if not self.can_manage(name):
            return HTTPForbidden()
        form = self.get_form(('save',))
        self.response['form_resources'] = form.get_widget_resources()
        if name not in self.groups:
            self.add_flash_message(_(u"Couldn't find any group with id '${name}'",
                                     mapping = {'name': name}))
            url = self.request.resource_url(self.context, 'groups')
            return HTTPFound(location = url)
        if 'save' in self.request.POST:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            #FIXME: check that the person posting is a group manager or server amdin!
            self.groups[name].update(appstruct)
            url = self.request.resource_url(self.context, 'groups', query = {'action': 'view', 'name': name})
            return HTTPFound(location = url)
        self.response['form'] = form.render(appstruct = self.groups[name])
        return self.response

    @view_config(request_param = "action=view", renderer = "templates/view.pt")
    def view(self):
        name = self.request.GET.get('name')
        if not self.can_manage(name):
            return HTTPForbidden()
        self.response['group'] = self.groups.get(name)
        self.response['group_name'] = name
        return self.response

    @view_config(request_param = "action=delete", renderer = "madetomeasure:views/templates/form.pt")
    def delete(self):
        name = self.request.GET.get('name')
        self.response['group'] = self.groups.get(name)
        schema = colander.Schema(title = _(u"Really delete this group?"),
                                 description = self.groups[name]['title'])
        schema = schema.bind(context = self.context, request = self.request)
        form = deform.Form(schema, buttons = ('cancel', 'delete'))
        if self.request.method == 'POST':
            if 'delete' in self.request.POST:
                del self.groups[name]
            url = self.request.resource_url(self.context, 'groups')
            return HTTPFound(location = url)
        self.response['form'] = form.render()
        return self.response
