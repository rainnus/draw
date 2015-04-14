from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('draw.views',
    # Examples:
    # url(r'^$', 'drawProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^adminroot/', include(admin.site.urls)),

    url(r'^addUser/', 'addUser', name='addUser'),
    # url(r'^deleteUser/', 'deleteUser', name='deleteUser'),
    # url(r'^'),

    url(r'^$', 'drawView' ,name='home'),
    url(r'^draw/', 'drawView', name='draw'),

    url(r'^search/$','searchView',name='search'),

    url(r'^login/', 'loginView', name='login'),
    url(r'^logout/', 'logoutView', name='logout'),
    url(r'admin/', 'validate', name='validate'),
    url(r'adminView/(?P<message>\w*)$|adminView/$', 'adminView', name='validate'),

    url(r'^restartView/','restartView',name='restartView'),
    url(r'^restart/$','restart',name='restart'),

    url(r'^exportView/','exportView',name='exportView'),
    url(r'^export/','export',name='export'),
    # url(r'^importView/','importView',name='importView'),
    # url(r'^import/','myimport',name='import'),

    url(r'^test/','test',name='test'),
    url(r'^drawTest/', 'drawViewTest', name='draw'),
    url(r'^searchTest/$','searchViewTest',name='search'),
)
