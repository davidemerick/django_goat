from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    #defining items as all objects
    items = Item.objects.all()

    # Passing items object to our home page
    return render(request, 'home.html', {'items': items})
