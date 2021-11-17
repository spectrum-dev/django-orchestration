from django.contrib import admin

from authentication.models import AccountWhitelist, BasicAuthToken

# Register your models here.
admin.site.register(AccountWhitelist)
admin.site.register(BasicAuthToken)
