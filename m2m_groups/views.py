from uuid import uuid4

import deform
from betahaus.pyracont.factories import createSchema
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from madetomeasure.views.base import BaseView

from madetomeasure.interfaces import IOrganisation

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
        return self.response

    def get_form(self, buttons):
        schema = createSchema('GroupSchema')
        schema = schema.bind(context = self.context, request = self.request)
        return deform.Form(schema, buttons = buttons)

    @view_config(request_param = "action=add", renderer = "madetomeasure:views/templates/form.pt")
    def add(self):
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
        form = self.get_form(('save',))
        self.response['form_resources'] = form.get_widget_resources()
        name = self.request.GET.get('name')
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
        self.response['group'] = self.groups.get(name)
        self.response['group_name'] = name
        return self.response
