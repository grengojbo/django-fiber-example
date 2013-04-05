# -*- mode: python; coding: utf-8; -*-
__author__ = 'jbo'

from django.shortcuts import render


def promo(request):
    return render(request, 'static/promo.html')
