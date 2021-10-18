from django.contrib import admin

from strategy.models import UserStrategy, Strategy, StrategySharing

# Register your models here.

admin.site.register(Strategy)
admin.site.register(UserStrategy)
admin.site.register(StrategySharing)
