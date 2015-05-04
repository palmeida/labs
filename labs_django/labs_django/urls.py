# -*- coding: utf-8 -*-

# Global Imports:
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
        # Index:
        url(r'^$',
            TemplateView.as_view(template_name='index.html'),
            name='index'),

        # hcapp
        (r'^hc/', include('hcapp.urls')),

        # exchangeapp
        (r'^exchange/', include('exchangeapp.urls')),

        # devaluationapp
        (r'^devaluation/', include('devaluationapp.urls')),

        # About:
        url(r'^about/$',
            TemplateView.as_view(template_name='about.html'),
            name='about'),

        )
