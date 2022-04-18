from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages, auth





def index(request):
    return render(request, 'index/index.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        data_content = [subject, name]
        send_mail(data_content, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        messages.success(request, 'Contact request submitted successfully.')
    else:
        print('i dont get it')
        
        # messages.error(request, 'Invalid form submission.')
        

    return render(request, 'contact/contact.html')

# Create your views here.
