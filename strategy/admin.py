from django.contrib import admin

from strategy.models import Strategy, StrategySharing, UserStrategy

# Register your models here.

admin.site.register(Strategy)
admin.site.register(UserStrategy)
admin.site.register(StrategySharing)
