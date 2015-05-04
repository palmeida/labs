# -*- coding: utf-8 -*-

# Global Imports:
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('exchangeapp.views',

        # Calculate the exchange rates
        url(r'^$', 'exchange_calc', name='exchange_calc'),

        ##
        # Static pages

        # Notes:
        url(r'^notes/$',
            TemplateView.as_view(template_name='exchange_notes.html'),
            name='exchange_notes'),
        # About:
        url(r'^about/$',
            TemplateView.as_view(template_name='exchange_about.html'),
            name='exchange_about'),

        )
