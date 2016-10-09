# -*- coding: utf-8 -*-

# django
from django.contrib import admin
from django.utils.datastructures import SortedDict


class StaffAdmin(admin.ModelAdmin):
    valid_lookups = ()

    def get_actions(self, request):
        """
        Overrides get_actions to limit what actions are shown to the user
        to only include actions that the user has the permissions to use.
        Permissions are set to _permissions by action_permissions_required decorator.
        """
        app_name = self.model._meta.app_label
        actions = super(StaffAdmin, self).get_actions(request)

        # Filter out action, if user doesn't have permission for it.
        actions = [
            v for k, v in actions.items() if (
                not hasattr(v[0], '_permissions') or request.user.has_perms(
                    [p if '.' in p else '{0}.{1}'.format(app_name, p) for p in v[0]._permissions]
                )
            )
            and (not hasattr(v[0], '_request_test_function') or v[0]._request_test_function(request))
        ]

        # Sort actions by name
        actions = SortedDict([
            (name, (func, name, desc))
            for func, name, desc in sorted(actions, key=lambda x: x[2])
        ])
        return actions
