from django.contrib import admin

# core/admin.py
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class CustomAdminSite(AdminSite):
    site_header = _("استور، کاستوم")  # تغییر عنوان سایت
    site_title = _("پنل مدیریت استور")
    index_title = _("خوش آمدید")

    def each_context(self, request):
        context = super().each_context(request)
        context['site_header'] = self.site_header
        context['site_title'] = self.site_title
        context['index_title'] = self.index_title
        return context

# ایجاد یک نمونه از کلاس سفارشی
custom_admin_site = CustomAdminSite(name='customadmin')
