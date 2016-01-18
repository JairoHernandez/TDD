from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
	#return HttpResponse('<html><title>To-Do lists</title></html>')
	if request.method == 'POST': # The if statement is used to get unit test to pass(pg 55)
		return HttpResponse(request.POST['item_text'])
	return render(request, 'home.html', {'new_item_text': request.POST.get('item_text', ''), }) # Instead of building an HttpResponse, we now use the Django render function



