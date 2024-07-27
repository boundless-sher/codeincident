from django.shortcuts import render

# Create your views here.
def home(request):
    if(request.method == 'POST'):
        if(request.POST.get('handle') != None):
            if not request.session.exists(request.session.session_key):
                request.session.create()
            request.session['handle'] = request.POST.get('handle')
            print(request.session['handle'])
        else:
            request.session['handle'] = 'anonymous user' 
    
    return render(request, 'base/home.html') 