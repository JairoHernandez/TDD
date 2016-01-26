from django.shortcuts import redirect, render
from lists.models import Item

# Create your views here.

def home_page(request):
	if request.method == 'POST': # The if statement is used to get unit test to pass(pg 55)
		Item.objects.create(text=request.POST['item_text'])	# I think create also does save() execution
		return redirect('/')

	items = Item.objects.all()
	return render(request, 'home.html', {'items': items}) # Instead of building an HttpResponse, we now use the Django render function

	#item = Item()
	#item.text = request.POST.get('item_text','')
	#item.save()
	#return render(request, 'home.html', {'new_item_text': request.POST.get('item_text', ''), }) 



