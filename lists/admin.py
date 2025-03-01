from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseModelAdminMixin
from lists.models import List
from .registry import ComponentRegistry


@admin.register(List)
class ListTabsAdmin(BaseModelAdminMixin):
    list_display = ('name', 'id', 'owner', 'count_all', 'created_at', 'updated_at', 'view_items_link')
    list_filter = ('owner',)
    list_display_links = ('name',)

    actions = ['view_list_items_action']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/details/',
                self.admin_site.admin_view(self.view_list_details),
                name='list-details',
            ),
            path(
                '<path:object_id>/items/',
                self.admin_site.admin_view(self.view_list_items),
                name='list-items',
            ),
        ]
        return custom_urls + urls

    def view_items_link(self, obj):
        """Add a link to view all items in the list"""
        url = reverse(
            f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
            args=[obj.pk]
        )
        return format_html(
            '<a href="{}" class="btn btn-info btn-sm">{}</a>',
            f'{url}items/',
            _('View Items')
        )
    view_items_link.short_description = _('Items')

    def get_changelist_url(self):
        """Helper to get the changelist URL"""
        return reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')

    def get_details_url(self, obj_id):
        """Helper to get the details URL for a list"""
        return reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
            args=[obj_id]
        )

    def get_items_url(self, obj_id):
        """Helper to get the items URL for a list"""
        return reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
            args=[obj_id]
        ) + 'items/'

    def view_list_details(self, request, object_id):
        """Show list details with tabs"""
        # Extract the list ID from the object_id
        object_id = object_id.partition('/')[0]
        list_obj = self.get_object(request, object_id)

        # Use Django's default change_view but with our custom template
        response = self.changeform_view(
            request,
            object_id=object_id,
            form_url='',
            extra_context={
                'show_tabs': True,
                'active_tab': 'details',
                'items_url': self.get_items_url(list_obj.id),
                'details_url': self.get_details_url(list_obj.id),
                'list_obj': list_obj,
            }
        )
        return response

    def view_list_items(self, request, object_id):
        """Show list items with tabs"""
        # Extract the list ID from the object_id
        object_id = object_id.partition('/')[0]
        list_obj = self.get_object(request, object_id)

        # Handle POST request to remove items
        if request.method == 'POST' and 'action' in request.POST and request.POST['action'] == 'remove_item':
            component_type = request.POST.get('component_type')
            component_id = request.POST.get('component_id')

            if component_type and component_id:
                items_to_remove = [{'component_type': component_type, 'component_id': component_id}]
                list_obj.remove_items_bulk(items_to_remove)
                self.message_user(request, f"Item removed successfully from {list_obj.name}")

                # Redirect to refresh the page after removing an item
                return HttpResponseRedirect(request.path)

        # Get all items from the list
        all_items = list_obj.get_all_items()

        # Prepare items for display
        formatted_items = []
        for item in all_items:
            component = item.component
            component_type = item.component_type

            # Get the admin URL for this component
            app_label = component._meta.app_label
            model_name = component._meta.model_name
            admin_url = reverse(f'admin:{app_label}_{model_name}_change', args=[component.id])

            formatted_items.append({
                'id': item.id,
                'component_id': component.id,
                'component_type': component_type,
                'component_type_display': component_type.replace('_', ' ').title(),
                'component_name': f"{component.manufacturer} {component.model}",
                'admin_url': admin_url,
                'added_at': item.added_at,
            })

        context = {
            **self.admin_site.each_context(request),
            'title': f'Items in {list_obj.name}',
            'list_obj': list_obj,
            'items': formatted_items,
            'opts': self.model._meta,
            'original': list_obj,
            'has_change_permission': True,
            'show_tabs': True,
            'active_tab': 'items',
            'items_url': self.get_items_url(list_obj.id),
            'details_url': self.get_details_url(list_obj.id)
        }

        return render(
            request,
            'admin/lists/list/tabs_list_items.html',
            context
        )

    def view_list_items_action(self, request, queryset):
        """Admin action to view items for a selected list"""
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one list to view items", level='error')
            return

        list_obj = queryset.first()
        return HttpResponseRedirect(self.get_items_url(list_obj.id))

    view_list_items_action.short_description = _("View items in selected list")

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Override change_view to add our tabbed interface"""
        extra_context = extra_context or {}
        list_obj = self.get_object(request, object_id)

        extra_context.update({
            'show_tabs': True,
            'active_tab': 'details',
            'items_url': self.get_items_url(list_obj.id),
            'details_url': self.get_details_url(list_obj.id),
            'list_obj': list_obj,
        })

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )