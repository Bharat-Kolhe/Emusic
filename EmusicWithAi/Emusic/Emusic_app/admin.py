from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html

class MyAdminSite(AdminSite):
    site_header = "My Custom Admin"
    site_title = "Admin Dashboard"
    index_title = "Welcome to the Admin Dashboard"

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = 'admin_styles.css'
        return context

admin.site = MyAdminSite()
