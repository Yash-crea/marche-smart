from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Owner, Customer


def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            return render(request, 'customer_login.html', {'error': 'Please provide both email and password.'})
        
        try:
            customer = Customer.objects.get(email=email)
            request.session['customer_id'] = customer.id
            request.session['customer_email'] = customer.email
            request.session['customer_name'] = customer.name
            return redirect('marche_smart:home')
        except Customer.DoesNotExist:
            return render(request, 'customer_login.html', {'error': 'Invalid email or password.'})
    
    return render(request, 'customer_login.html')


def owner_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            return render(request, 'owner_login.html', {'error': 'Please provide both email and password.'})
        
        try:
            owner = Owner.objects.get(email=email)
            request.session['owner_id'] = owner.id
            request.session['owner_email'] = owner.email
            request.session['owner_name'] = owner.name
            return redirect('marche_smart:home')
        except Owner.DoesNotExist:
            return render(request, 'owner_login.html', {'error': 'Invalid email or password.'})
    
    return render(request, 'owner_login.html')


def home(request):
    q = request.GET.get('q', '').strip()
    if q:
        products = Product.objects.filter(name__icontains=q)
    else:
        products = Product.objects.all()[:12]

    context = {
        'products': products,
        'query': q,
    }
    return render(request, 'home.html', context)


def shop(request):
    # Get all products initially
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Search filter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)
    
    # Category filter
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Price range filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass
    
    # Get price range for the filter
    all_products = Product.objects.all()
    max_price_available = all_products.values_list('price', flat=True).order_by('-price').first() or 0
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'max_price_available': max_price_available,
    }
    return render(request, 'shop.html', context)


def search(request):
    # simple search endpoint that reuses home template
    return home(request)


def owner_dashboard(request):
    # placeholder — in a real app you'd verify permissions
    # Provide dummy analytics context for frontend display
    context = {
        'sales_total': 12345.67,
        'orders_count': 78,
        'top_products': Product.objects.order_by('-price')[:5],
    }
    return render(request, 'base.html', context)


def customer_dashboard(request):
    # placeholder customer view
    sample_customer = Customer.objects.first()
    context = {
        'customer': sample_customer,
        'current_purchase_total': 42.50,
        'orders': [],
    }
    return render(request, 'base.html', context)


def about(request):
    # render a dedicated About page
    return render(request, 'about.html')
from django.shortcuts import render

# Create your views here.
