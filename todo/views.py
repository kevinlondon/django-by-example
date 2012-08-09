from todo.models import *
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def mark_done(request, pk):
    item = Item.objects.get(pk=pk)
    item.done = True
    item.save()
    return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

@staff_member_required
def delete(request, pk):
    item = Item.objects.get(pk=pk)
    item.delete()
    item.save()
    return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

