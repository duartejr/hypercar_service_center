from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import json
from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import json
from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import json


class WelcomeView(View):
    template = 'welcome_template.html'

    def get(self, request, *args, **kwargs):
        return redirect('/menu')


class MenuView(View):
    template = "menu_template.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {"menu_template": self.template})


class GetTicket(View):
    template = "get_ticket.html"
    service = None

    def get(self, request, *args, **kwargs):
        settings.COUNTER += 1
        if self.service == "change_oil":
            time = len(settings.LINE_OF_CARS["change_oil"]) * 2
        elif self.service == "inflate_tires":
            time = len(settings.LINE_OF_CARS["change_oil"]) * 2 + \
                   len(settings.LINE_OF_CARS["inflate_tires"]) * 5
        else:
            time = len(settings.LINE_OF_CARS["change_oil"]) * 2 + \
                   len(settings.LINE_OF_CARS["inflate_tires"]) * 5 + \
                   len(settings.LINE_OF_CARS["diagnostic"]) * 30

        settings.LINE_OF_CARS[self.service].append(settings.COUNTER)

        return render(request, self.template, context={"op": self.service,
                                                       "counter": settings.COUNTER,
                                                       "time_to_wait": time})


class ProcessingView(View):
    template = "processing.html"

    def get(self, request, *args, **kwargs):
        n_change_oil = len(settings.LINE_OF_CARS["change_oil"])
        n_inflate_tires = len(settings.LINE_OF_CARS["inflate_tires"])
        n_diagnostic = len(settings.LINE_OF_CARS["diagnostic"])
        for work in settings.LINE_OF_CARS:
            print(work)
        return render(request, self.template, context={"change_oil": n_change_oil,
                                                       "inflate_tires": n_inflate_tires,
                                                       "diagnostic": n_diagnostic})

    def post(self, request, *args, **kwargs):
        settings.TICKET = 0
        if len(settings.LINE_OF_CARS):
            for work in settings.LINE_OF_CARS:
                if len(settings.LINE_OF_CARS[work]):
                    settings.TICKET = settings.LINE_OF_CARS[work].pop(0)
                    break
        return redirect('/next')


class NextView(View):
    template = 'next.html'

    def get(self, request):
        context = {'ticket': settings.TICKET}
        return render(request, self.template, context)