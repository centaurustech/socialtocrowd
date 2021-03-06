from django.contrib.auth.decorators import login_required as lr
from django.conf.urls import patterns, include, url
from project import views

urlpatterns = patterns('',
    url(r'^near/$', views.near, name="near"),
    url(r'^near/(?P<projectslug>[-\w]+)/$', views.nearproject, name="nearproject"),
    url(r'^donear/$', views.donear, name="donear"),
    url(r'^parseaddr/$', views.parseaddr, name="parseaddr"),
    url(r'^things/$', views.things, name="things"),
    url(r'^ongs/$', views.ongs, name="ongs"),
    url(r'^ong/(?P<ongslug>[-\w]+)/$', views.ong, name="ong"),
    url(r'^detail/(?P<projectslug>[-\w]+)/$', views.detail, name="detail"),
    url(r'^donate/(?P<projectslug>[-\w]+)/$', views.donate, name="donate"),
    url(r'^donate/remove/(?P<pk>\d+)/$', views.donate_remove, name="donate_remove"),
    url(r'^cooperate/(?P<projectslug>[-\w]+)/$', views.cooperate, name="cooperate"),
    url(r'^create/ong/$', lr(views.CreateONG.as_view()), name="create_ong"),
    url(r'^edit/ong/(?P<pk>\d+)/$', lr(views.UpdateONG.as_view()), name="edit_ong"),
    url(r'^create/project/(?P<ongslug>[-\w]+)/$', lr(views.CreateProject.as_view()), name="create_project"),
    url(r'^edit/project/(?P<projectslug>[-\w]+)/$', lr(views.UpdateProject.as_view()), name="edit_project"),
    url(r'^create/thing/(\d+)/$', lr(views.CreateThing.as_view()), name="create_thing"),
    url(r'^edit/thing/(?P<pk>\d+)/$', lr(views.UpdateThing.as_view()), name="update_thing"),
    url(r'^remove/thing/(?P<pk>\d+)/$', lr(views.RemoveThing.as_view()), name="remove_thing"),
    url(r'^create/direction/(\d+)/$', lr(views.CreateDirection.as_view()), name="create_direction"),
    url(r'^edit/direction/(?P<pk>\d+)/$', lr(views.UpdateDirection.as_view()), name="update_direction"),
    url(r'^remove/direction/(?P<pk>\d+)/$', lr(views.RemoveDirection.as_view()), name="remove_direction"),
    url(r'^create/objective/(\d+)/$', lr(views.CreateProjectObjective.as_view()), name="create_objective"),
    url(r'^edit/objective/(?P<pk>\d+)/$', lr(views.UpdateProjectObjective.as_view()), name="update_objective"),
    url(r'^remove/objective/(?P<pk>\d+)/$', lr(views.RemoveProjectObjective.as_view()), name="remove_objective"),

    # AJAX
    url(r'^thing/description/$', views.thing_description, name="thing_description"),

)
