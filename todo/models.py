from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class DateTime(models.Model):
    list_display = ["datetime"]
    datetime = models.DateTimeField(auto_now_add=True)
    
    def response_add(self, request, obj, post_url_continue="../%s/"):
        """Determines the HttpResponse for the add_view stage. """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = "Item(s) were added successfully."
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + " " + 
                    "You may edit it again below."
                    )
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse(
                    '<script type="text/javascript">',
                    'opener.dismissAddAnotherPopup(window, "%s", "%s");'
                    '</script>' % (escape(pj_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (
                _("You may add another %s below.") % force_unicode(opts.verbose_name)
                ))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            for item in Item.objects.filter(created=obj):
                if not item.user:
                    item.user = request.user
                    item.save()

            return HttpResponseRedirect(reverse("admin:todo_item_changelist"))
    
    def __unicode__(self):
        return unicode(self.datetime.strftime("%b %d, %Y, %I:%M %p"))

class Item(models.Model):
    name = models.CharField(max_length=60)
    created = models.ForeignKey(DateTime)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    done = models.BooleanField(default=False)
    onhold = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True)
    
    def return_progress(self):
        return "<div style='width: 100px; border: 1px solid #ccc; '>" + \
            "<div style='height: 4px; width: %dpx;" % self.progress + \
            "background: #555; '></div></div>"

    def toggle_hold(self):
        if self.onhold:
            link = "On Hold"
        else:
            link = "Off Hold"
        return "<a href='%s'>%s</a>" % (
            reverse("todo.views.item_action", args=["onhold", self.pk]), link
            )

    def mark_done(self):
        return "<a href='%s'>Done</a>" % reverse("todo.views.item_action", 
                                                 args=["done", self.pk])
    
    def delete(self):
        return "<a href='%s'>Delete</a>" % reverse("todo.views.item_action", 
                                                   args=["delete", self.pk])

    delete.allow_tags = True
    mark_done.allow_tags = True
    toggle_hold.allow_tags = True
    return_progress.allow_tags = True

class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "difficulty", "user", "created", 
                    "return_progress", "toggle_hold", "mark_done",  "done", "delete",]
    list_filter = ["priority", "difficulty", "done"]
    search_fields = ["name"]

class ItemInline(admin.TabularInline):
    model = Item

class DateAdmin(admin.ModelAdmin):
    list_display = ["datetime"]
    inlines = [
            ItemInline,
            ]

admin.site.register(DateTime, DateAdmin)
admin.site.register(Item, ItemAdmin)
