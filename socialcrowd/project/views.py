from django.db import models
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime

from .forms import ThingFormSet, DirectionFormSet
from .models import Project
from .models import Organization
from .models import Thing, Shipping, Donation
from .models import ShippingCompany
from .models import Direction


class Near(TemplateView):
    template_name = 'project/near.html'
near = Near.as_view()


class Things(TemplateView):
    template_name = 'project/search.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(Things, self).get_context_data(*args, **kwargs)
        ctx['title'] = _('Donate')
        ctx['placeholder'] = _('Search things to donate')

        q = self.request.GET.get('search', '')
        # default
        query = Project.objects.filter(ong__status="actived")
        complexq = Q()
        if q:
            complexq = complexq & Q(name__icontains=q)
            complexq = complexq | Q(description__icontains=q)
            complexq = complexq | Q(ong__name__icontains=q)
            complexq = complexq | Q(ong__description__icontains=q)
            complexq = complexq | Q(things__name__icontains=q)
            complexq = complexq | Q(things__description__icontains=q)

        query = query.filter(complexq).distinct()

        # TODO paginate
        ctx['projects'] = query
        ctx['listtemplate'] = 'project/projects.html'
        return ctx
things = Things.as_view()


class ONGs(TemplateView):
    template_name = 'project/search.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(ONGs, self).get_context_data(*args, **kwargs)
        ctx['title'] = _('ONGs')
        ctx['placeholder'] = _('Search ONG to donate')

        q = self.request.GET.get('search', '')
        # default
        query = Organization.objects.filter(status="actived")
        complexq = Q()
        if q:
            complexq = complexq & Q(name__icontains=q)
            complexq = complexq | Q(description__icontains=q)
            complexq = complexq | Q(projects__name__icontains=q)
            complexq = complexq | Q(projects__description__icontains=q)
            complexq = complexq | Q(city__icontains=q)
            complexq = complexq | Q(province__icontains=q)

        query = query.filter(complexq).distinct()

        # TODO paginate
        ctx['ongs'] = query
        ctx['listtemplate'] = 'project/ongs.html'
        return ctx
ongs = ONGs.as_view()


class CreateONG(CreateView):
    model = Organization
    fields = ['name', 'description', 'img', 'city', 'province']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.add_message(self.request, messages.INFO,
            'Administrators will review the organization as soon as possible')
        return redirect("/project/ong/%i" % obj.id)


class UpdateONG(UpdateView):
    model = Organization
    fields = ['name', 'description', 'img', 'city', 'province']
    success_url = '/'

    def get_context_data(self, **kwargs):
        ctx = super(UpdateONG, self).get_context_data(**kwargs)
        ctx['edit'] = True
        return ctx


class ONG(TemplateView):
    template_name = 'project/ong-detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(ONG, self).get_context_data(*args, **kwargs)
        ong = get_object_or_404(Organization, pk=self.args[0])
        if ong.status == "actived" or self.request.user == ong.user:
            ctx['ong'] = ong
        else:
            messages.add_message(self.request, messages.ERROR,
                'Organization deleted or not actived')
        return ctx
ong = ONG.as_view()


class Detail(TemplateView):
    template_name = 'project/project-detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(Detail, self).get_context_data(*args, **kwargs)
        project = get_object_or_404(Project, pk=self.args[0])
        ctx['project'] = project
        return ctx
detail = Detail.as_view()


class CreateProject(CreateView):
    model = Project
    fields = ['name', 'description', 'img']

    def get_context_data(self, *args, **kwargs):
        context = super(CreateProject, self).get_context_data(*args, **kwargs)
        ong = get_object_or_404(Organization, pk=self.args[0])
        if (self.request.user != ong.user):
            messages.add_message(self.request, messages.ERROR,
                'Insufficient permissions')
        context['ong'] = ong
        if self.request.POST:
            context['thing_form'] = ThingFormSet(self.request.POST)
            context['direction_form'] = DirectionFormSet(self.request.POST)
        else:
            context['thing_form'] = ThingFormSet()
            context['direction_form'] = DirectionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        obj = form.save(commit=False)
        obj.ong = context['ong']
        obj.save()
        thing_form = context['thing_form']
        direction_form = context['direction_form']
        if thing_form.is_valid() and direction_form.is_valid():
            self.object = form.save()
            thing_form.instance = self.object
            thing_form.save()
            direction_form.instance = self.object
            direction_form.save()
            messages.add_message(self.request, messages.INFO,
                'Project created successful')
            return redirect("/project/detail/%i" % obj.id)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class UpdateProject(UpdateView):
    model = Project
    fields = ['name', 'description', 'img']
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateProject, self).get_context_data(*args, **kwargs)
        context['edit'] = True
        return context


class CreateThing(CreateView):
    model = Thing
    fields = ['name', 'description', 'quantity']

    def get_context_data(self, *args, **kwargs):
        context = super(CreateThing, self).get_context_data(*args, **kwargs)
        project = get_object_or_404(Project, pk=self.args[0])
        if (self.request.user != project.ong.user):
            messages.add_message(self.request, messages.ERROR,
                'Insufficient permissions')
        context['project'] = project
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        obj = form.save(commit=False)
        obj.project = context['project']
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        context = self.get_context_data()
        return '/project/edit/project/%i' % context['project'].id


class UpdateThing(UpdateView):
    model = Thing
    fields = ['name', 'description', 'quantity']

    def get_context_data(self, **kwargs):
        ctx = super(UpdateThing, self).get_context_data(**kwargs)
        ctx['edit'] = True
        return ctx

    def get_success_url(self):
        context = self.get_context_data()
        return '/project/edit/project/%i' % context['thing'].project.id


class RemoveThing(DeleteView):
    model = Thing
    fields = ['name', 'description', 'quantity']

    def get_context_data(self, **kwargs):
        ctx = super(RemoveThing, self).get_context_data(**kwargs)
        ctx['edit'] = True
        return ctx

    def get_success_url(self):
        context = self.get_context_data()
        return '/project/edit/project/%i' % context['thing'].project.id


class CreateDirection(CreateView):
    model = Direction
    fields = ['description', 'pos', 'timetable', 'phone']

    def get_context_data(self, *args, **kwargs):
        context = super(CreateDirection, self).get_context_data(*args, **kwargs)
        project = get_object_or_404(Project, pk=self.args[0])
        if (self.request.user != project.ong.user):
            messages.add_message(self.request, messages.ERROR,
                'Insufficient permissions')
        context['project'] = project
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        obj = form.save(commit=False)
        obj.project = context['project']
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        context = self.get_context_data()
        return '/project/edit/project/%i' % context['project'].id


class UpdateDirection(UpdateView):
    model = Direction
    fields = ['description', 'pos', 'timetable', 'phone']

    def get_context_data(self, **kwargs):
        ctx = super(UpdateDirection, self).get_context_data(**kwargs)
        ctx['edit'] = True
        return ctx

    def get_success_url(self):
        context = self.get_context_data()
        return '/project/edit/project/%i' % context['direction'].project.id


class RemoveDirection(DeleteView):
    model = Direction
    fields = ['description', 'pos', 'timetable', 'phone']

    def get_context_data(self, **kwargs):
        ctx = super(RemoveDirection, self).get_context_data(**kwargs)
        ctx['edit'] = True
        return ctx

    def get_success_url(self):
        context = self.get_context_data()
        return '/project/edit/project/%i' % context['direction'].project.id


def donate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    checks = []
    for c in request.GET.getlist('checks[]'):
        checks.append(int(c))
    ships_project = Shipping.objects.filter(project=project, user=request.user)
    for ship_project in ships_project:
        if not ship_project.donations.all():
            break
        ship_project = None
    if not ships_project or not ship_project:
        ship_project = Shipping(project=project, user=request.user)
        ship_project.save()
    ctx = {}
    ctx['project'] = project
    ctx['things_checks'] = checks
    ctx['ship'] = ship_project
    ctx['today'] = datetime.today()
    return render(request, 'project/donate-t1.html', ctx)


def shipping(request, pk):
    if request.POST:
        ship_project = get_object_or_404(Shipping, pk=pk)
        donations = []
        for thing in ship_project.project.things.all():
            strid = str(thing.id)
            if request.POST.get('quantity[' + strid + ']') and\
                    int(request.POST.get('quantity[' + strid + ']')) > 0:
                quantity = request.POST.get('quantity[' + strid + ']')
                info = request.POST.get('info[' + strid + ']')
                donation = Donation(thing=thing, shipping=ship_project,
                        quantity=quantity, info=info)
                donation.save()
                donations.append(donation)
        if donations:
            ship_project.comment = request.POST.get('comment')
            ship_project.direction = get_object_or_404(Direction, pk=request.POST.get('direction'))
            hour = request.POST.get('delivery_hour')
            date = request.POST.get('delivery_date')
            if date and hour:
                delivery = datetime(int(date[:4]), int(date[5:7]),
                        int(date[8:]), int(hour[:2]), int(hour[3:5]))
            elif date:
                delivery = datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
            else:
                delivery = None
            ship_project.delivery = delivery
            if request.POST.get('show') == 'on':
                ship_project.show = True
            else:
                ship_project.show = False
            ship_project.save()
            ctx = {}
            ctx['ship'] = ship_project
            ctx['donations'] = donations
            ctx['companies'] = ShippingCompany.objects.all()
            return render(request, 'project/shipping.html', ctx)
        else:
            messages.add_message(request, messages.ERROR,
                'You should mark something for donate')
            return redirect('/project/donate/%i' % ship_project.project.id)

