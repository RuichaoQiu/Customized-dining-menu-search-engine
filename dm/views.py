from dm.models import Restaurant
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import query

l = []
loc = "Phoenix"
myaddr = ""
station_list = []
class menulist:
    def __init__(self):
        self.name = ""
        self.fav = 5.0
mc = [menulist()]

class IndexView(generic.ListView):
    template_name = 'dm/index.html'
    context_object_name = 'menucount'

    def get_queryset(self):
        global mc
        return mc


def searchquery(request):
    global l
    global mc
    global loc
    global station_list
    l = query.queryresult(mc,loc)
    station_list = []
    for item in l:
        station = Restaurant.objects.raw('SELECT * FROM dm_restaurant WHERE business_id = %s', (item[0],))
        for tmpit in station:
            tmpit.stars = '%.1f'%(item[1])
            station_list.append(tmpit)
    return render(request, 'dm/searchquery.html', {'query_list': station_list})

def review(request, choice):
    global l
    
    index = int(choice)-1

    return render(request, 'dm/review.html', {'review_list': l[index][2]})

def route(request, choice):
    global station_list
    index = int(choice)-1
    tmp = station_list[index].full_address
    tmp = tmp.replace("\n",", ")
    curi = len(tmp)-1
    while (tmp[curi] >= '0' and tmp[curi] <= '9') or tmp[curi] == " ":
        curi -= 1
    tmp = tmp[:curi+1]
    station_list[index].full_address = tmp
    return render(request, 'dm/route.html', {'rest': station_list[index], 'mycuraddr': myaddr})

@csrf_exempt
def recordmanager(request):
	#c = Car.objects.get(pk=request.POST['choice']).delete()
	#c.save()
    if 'add' in request.POST:
        global mc
        for i in xrange(len(mc)):
            st = 'dish'+str(i+1)
            mc[i].name = request.POST[st]
            st = 'fav'+str(i+1)
            mc[i].fav = float(request.POST[st])
        global loc
        global myaddr
        loc = request.POST["location"]
        myaddr = request.POST["myaddr"]
        return HttpResponseRedirect(reverse('dm:searchquery'))
    if 'edit' in request.POST:
        global mc
        for i in xrange(len(mc)):
            st = 'dish'+str(i+1)
            mc[i].name = request.POST[st]
            st = 'fav'+str(i+1)
            mc[i].fav = float(request.POST[st])
        mc.append(menulist())
        return HttpResponseRedirect(reverse('dm:index'))
    if 'delete' in request.POST:
        global mc
        for i in xrange(len(mc)):
            st = 'dish'+str(i+1)
            mc[i].name = request.POST[st]
            st = 'fav'+str(i+1)
            mc[i].fav = float(request.POST[st])
        if 'choice' in request.POST:
            del mc[int(request.POST['choice'])-1]
        return HttpResponseRedirect(reverse('dm:index'))
    if 'review' in request.POST:
        global l
        if 'choice' in request.POST:
            return HttpResponseRedirect(reverse('dm:review', args=(request.POST['choice'],)))
        return HttpResponseRedirect(reverse('dm:searchquery'))

    if 'route' in request.POST:
        global l
        if 'choice' in request.POST:
            return HttpResponseRedirect(reverse('dm:route', args=(request.POST['choice'],)))
        return HttpResponseRedirect(reverse('dm:searchquery'))
	return HttpResponseRedirect(reverse('dm:index'))


