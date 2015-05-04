# -*- coding: utf-8 -*-

# Global Imports:
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('devaluationapp.views',

        # Calculate the exchange rates
        url(r'^$', 'devaluation_calc', name='devaluation_calc'),

        ##
        # Static pages

        # Notes:
        url(r'^notes/$',
            TemplateView.as_view(template_name='devaluation_notes.html'),
            name='devaluation_notes'),
        # About:
        url(r'^about/$',
            TemplateView.as_view(template_name='devaluation_about.html'),
            name='devaluation_about'),

        )
