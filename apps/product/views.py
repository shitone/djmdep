from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required()
def tmp(request):
    return render(request, 'product/tmp.html')


def tmpc(request):
    return render(request, 'product/tmp_c.html', {'child_page': 1})


@login_required()
def wind(request):
    return render(request, 'product/wind.html')


def windc(request):
    return render(request, 'product/wind_c.html', {'child_page': 1})
