from django.db import models
from django.contrib import admin

class DateTime(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return unicode(self.datetime)

class Item(models.Model):
    name = models.CharField(max_length=60)
    created = models.ForeignKey(DateTime)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    done = models.BooleanField(default=False)

class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "difficulty", "created", "done"]
    search_fields = ["name"]

class ItemInline(admin.TabularInline):
    model = Item

class DateAdmin(admin.ModelAdmin):
    list_display = ["datetime"]
    inlines = [ItemInline]

admin.site.register(DateTime, DateAdmin)
admin.site.register(Item, ItemAdmin)
