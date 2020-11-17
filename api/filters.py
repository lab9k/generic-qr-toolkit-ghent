from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class HasRedirectFilter(admin.SimpleListFilter):
    title = _('has redirect')
    parameter_name = 'redirect_url'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', _('yes')),
            ('no', _('no')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'yes':
            return queryset.exclude(redirect_url__exact='')
        if self.value() == 'no':
            return queryset.filter(redirect_url__exact='')
        else:
            return queryset.all()


class HasFormFilter(admin.SimpleListFilter):
    title = _('has form')
    parameter_name = 'form_url'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', _('yes')),
            ('no', _('no')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'yes':
            return queryset.exclude(form_url__exact='')
        if self.value() == 'no':
            return queryset.filter(form_url__exact='')
        else:
            return queryset.all()


class HasBasicInfoFilter(admin.SimpleListFilter):
    title = _('has basic info')
    parameter_name = 'basic_info'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', _('yes')),
            ('no', _('no')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'yes':
            return queryset.exclude(basic_info__exact='')
        if self.value() == 'no':
            return queryset.filter(basic_info__exact='')
        else:
            return queryset.all()


class DepartmentFilter(admin.SimpleListFilter):
    title = _('on department')
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        pass

    def queryset(self, request, queryset):
        pass


