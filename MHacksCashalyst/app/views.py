# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

def home(request):
    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/index.html',
        RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

#class LineChartJSONView(BaseLineChartView):
#    def get_labels(self):
#        """Return 7 labels."""
#        return ["January", "February", "March", "April", "May", "June", "July"]
#    def get(self,request,*args,**kwargs):
#        a =  request.GET.get('foo',1)
#        return [[a,a*2,a*3]]
     
    #def get_data(self):
    #    """Return 3 dataset to plot."""
    #    a =  request.GET.get('foo',1)

    #    return [[a,a*2,a*3]]
#def line_chart(request):
     
#     line_chart = TemplateView.as_view(template_name='line_chart.html')
#     return render(LineChartJSONView.as_view())

#def get_quote(request):
#    form = StockQuoteForm()
#    return render(request, 'name.html', {'form': form})

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
