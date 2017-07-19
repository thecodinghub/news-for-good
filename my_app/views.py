from django.views.generic import TemplateView

class TestView(TemplateView):
    template_name = 'my_app/test.html'

class ThanksView(TemplateView):
    template_name = 'my_app/thanks.html'
