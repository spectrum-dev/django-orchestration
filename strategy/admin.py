from django.contrib import admin

from strategy.models import Strategy, StrategySharing, UserStrategy


admin.site.register(Strategy)
admin.site.register(UserStrategy)
admin.site.register(StrategySharing)
