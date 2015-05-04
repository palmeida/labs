# -*- coding: utf-8 -*-

# Global Imports:
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('hcapp.views',

        # Create the requested hemicycle
        url(r'^svg/$', 'svg_hemicycle', name='svg_hemicycle'),

        # Show election results
        url(r'^$', 'results', name='hc_results'),

        ##
        # Static pages

        # About:
        url(r'^about/$',
            TemplateView.as_view(template_name='hc_about.html'),
            name='hc_about'),

        # Notes:
        url(r'^notes/$',
            TemplateView.as_view(template_name='hc_notes.html'),
            name='hc_notes'),

        # Law:
        url(r'^law/$',
            TemplateView.as_view(template_name='hc_law.html'),
            name='hc_law'),
        )

