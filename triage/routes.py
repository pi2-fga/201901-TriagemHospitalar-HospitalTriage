from django.shortcuts import render
from boogie.router import Router

urlpatterns = Router()


@urlpatterns.route()
def welcome_page(request):
    return render(request, 'triage/welcome_page.html', {})
