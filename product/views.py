from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect


from django.shortcuts import redirect, render
from django.views import View
from .models.product import Product
from .models.category import Category
from.models.customers import Customer


class Signup(View):
    def get(self, request):
        return render(request, 'account/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        lastname = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        value = {
            'first_name': first_name,
        }
        print(first_name, lastname, phone, email, password)
        # validation

        error_message = None

        customer = Customer(first_name=first_name, last_name=lastname,
                            phone=phone, email=email, password=password)
        error_message = self.validateCustomer(customer)
        if not error_message:
            print(first_name, lastname, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('http://127.0.0.1:8000/product/login')
        else:
            data = {
                'error': error_message,
                'values': value

            }

        return render(request, 'account/signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if(not customer.first_name):
            error_message = 'firstname required'
        elif len(customer.first_name) < 5:
            error_message = 'firstname must be 5 char or more'

        elif len(customer.email) < 3:
            error_message = 'email must be 5 char or more'
        return error_message


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'account/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('http://127.0.0.1:8000/product/store')
            else:
                error_message = 'email or password invalid'
        else:
            error_message = 'email or password invalid'

        return render(request, 'account/login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('http://127.0.0.1:8000/product/store')

    def get(self, request):
        # print()
        return HttpResponseRedirect('http://127.0.0.1:8000/product/store')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['products'] = products
    data['category'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'products/collection.html', data)


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        product = Product.get_products_by_id(ids)

        return render(request, 'products/cart.html', {'product': product})
