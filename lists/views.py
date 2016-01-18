from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
	#return HttpResponse('<html><title>To-Do lists</title></html>')
	return render(request, 'home.html') # Instead of building an HttpResponse, we now use the Django render function

