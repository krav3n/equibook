# -*- coding: utf-8 -*-

# zoneui imports
from horsebook.admin import StaffAdmin
from horsebook.site import site
from horsebook.student.models import Student


class StudentAdmin(StaffAdmin):
    actions = []
    list_display = ('name', 'phone', 'email')
    list_filter = []
    list_max_show_all = 25
    list_per_page = 25
    search_fields = []

    def __init__(self, *args, **kwargs):
        super(StudentAdmin, self).__init__(*args, **kwargs)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# Register admin on main site
site.register(Student, StudentAdmin)
