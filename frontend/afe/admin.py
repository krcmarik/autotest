"""Django 1.0 admin interface declarations."""

from django.contrib import admin
from django.db import models as dbmodels

from autotest_lib.frontend import settings
from autotest_lib.frontend.afe import model_logic, models


class SiteAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(SiteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if (db_field.rel and
                issubclass(db_field.rel.to, model_logic.ModelWithInvalid)):
            model = db_field.rel.to
            field.choices = model.valid_objects.all().values_list(
                    'id', model.name_field)
        return field


class AtomicGroupAdmin(SiteAdmin):
    list_display = ('name', 'description', 'max_number_of_machines')

    def queryset(self, request):
        return models.AtomicGroup.valid_objects

admin.site.register(models.AtomicGroup, AtomicGroupAdmin)


class LabelAdmin(SiteAdmin):
    list_display = ('name', 'kernel_config')

    def queryset(self, request):
        return models.Label.valid_objects

admin.site.register(models.Label, LabelAdmin)


class UserAdmin(SiteAdmin):
    list_display = ('login', 'access_level')
    search_fields = ('login',)

admin.site.register(models.User, UserAdmin)


class HostAdmin(SiteAdmin):
    # TODO(showard) - showing platform requires a SQL query for
    # each row (since labels are many-to-many) - should we remove
    # it?
    list_display = ('hostname', 'platform', 'locked', 'status')
    list_filter = ('labels', 'locked', 'protection')
    search_fields = ('hostname', 'status')
    filter_horizontal = ('labels',)

    def queryset(self, request):
        return models.Host.valid_objects

admin.site.register(models.Host, HostAdmin)


class TestAdmin(SiteAdmin):
    fields = ('name', 'author', 'test_category', 'test_class',
              'test_time', 'sync_count', 'test_type', 'path',
              'dependencies', 'experimental', 'run_verify',
              'description')
    list_display = ('name', 'test_type', 'description', 'sync_count')
    search_fields = ('name',)
    filter_horizontal = ('dependency_labels',)

admin.site.register(models.Test, TestAdmin)


class ProfilerAdmin(SiteAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(models.Profiler, ProfilerAdmin)


class AclGroupAdmin(SiteAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('users', 'hosts')

admin.site.register(models.AclGroup, AclGroupAdmin)


if settings.FULL_ADMIN:
    class JobAdmin(SiteAdmin):
        list_display = ('id', 'owner', 'name', 'control_type')
        filter_horizontal = ('dependency_labels',)

    admin.site.register(models.Job, JobAdmin)

    class IneligibleHostQueueAdmin(SiteAdmin):
        list_display = ('id', 'job', 'host')

    admin.site.register(models.IneligibleHostQueue, IneligibleHostQueueAdmin)

    class HostQueueEntryAdmin(SiteAdmin):
        list_display = ('id', 'job', 'host', 'status',
                        'meta_host')

    admin.site.register(models.HostQueueEntry, HostQueueEntryAdmin)

    admin.site.register(models.AbortedHostQueueEntry)
