def customer_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if not name or not email or not password:
            return render(request, 'customer_signup.html', {'error': 'All fields are required.'})
        if Customer.objects.filter(email=email).exists():
            return render(request, 'customer_signup.html', {'error': 'Email already registered.'})
        customer = Customer(name=name, email=email)
        customer.save()
        # Optionally, log the user in after signup
        request.session['customer_id'] = customer.id
        request.session['customer_email'] = customer.email
        request.session['customer_name'] = customer.name
        return redirect('marche_smart:customer_dashboard')
    return render(request, 'customer_signup.html')
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Owner, Customer
from django.views.decorators.http import require_POST


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

            # --- Cart merging logic (future-proof) ---
            from .models import Cart, CartItem, Product
            session_cart = request.session.get('cart', {})
            cart, created = Cart.objects.get_or_create(customer=customer)
            for product_id, item in session_cart.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                except Product.DoesNotExist:
                    continue
                cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not item_created:
                    cart_item.quantity += item.get('quantity', 1)
                else:
                    cart_item.quantity = item.get('quantity', 1)
                cart_item.save()
            # Clear session cart after merging
            if session_cart:
                request.session['cart'] = {}
                request.session['cart_count'] = 0
            # --- End cart merging logic ---

            return redirect('marche_smart:customer_dashboard')
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
            return redirect('marche_smart:owner_dashboard')
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
    return render(request, 'owner_dashboard.html', context)


def customer_dashboard(request):
    # placeholder customer view
    customer_id = request.session.get('customer_id')
    customer = None
    if customer_id:
        customer = Customer.objects.filter(id=customer_id).first()
    context = {
        'customer': customer,
        'current_purchase_total': 42.50,
        'orders': [],
    }
    return render(request, 'customer_dashboard.html', context)


def about(request):
    # render a dedicated About page
    return render(request, 'about.html')


def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Initialize cart in session if it doesn't exist
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        cart = request.session['cart']
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            cart[product_id_str]['quantity'] += quantity
        else:
            try:
                product = Product.objects.get(id=product_id)
                cart[product_id_str] = {
                    'name': product.name,
                    'price': str(product.price),
                    'quantity': quantity,
                    'image_url': product.image_url,
                }
            except Product.DoesNotExist:
                return redirect('marche_smart:shop')
        
        # Update cart count in session
        total_items = sum(item['quantity'] for item in cart.values())
        request.session['cart_count'] = total_items
        request.session.modified = True
        
        return redirect('marche_smart:cart')
    
    return redirect('marche_smart:shop')


def cart(request):
    """Display shopping cart"""
    cart_items = request.session.get('cart', {})
    
    # Calculate totals
    subtotal = 0
    total_items = 0
    
    for item in cart_items.values():
        item_total = float(item['price']) * item['quantity']
        subtotal += item_total
        total_items += item['quantity']
    
    tax = subtotal * 0.1  # 10% tax
    total = subtotal + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': f"{subtotal:.2f}",
        'tax': f"{tax:.2f}",
        'total': f"{total:.2f}",
        'item_count': total_items,
    }
    
    return render(request, 'cart.html', context)

def checkout(request):
    # Only allow access if cart is not empty
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    return render(request, 'checkout.html')


def checkout(request):
    # Only allow access if cart is not empty
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    return render(request, 'checkout.html')

@require_POST
def remove_from_cart(request, product_id):
    """Remove product from cart"""
    if 'cart' in request.session:
        product_id_str = str(product_id)
        if product_id_str in request.session['cart']:
            del request.session['cart'][product_id_str]
            
            # Update cart count
            cart = request.session['cart']
            total_items = sum(item['quantity'] for item in cart.values())
            request.session['cart_count'] = total_items
            request.session.modified = True
    
    return redirect('marche_smart:cart')


def update_cart(request, product_id):
    """Update product quantity in cart"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            return remove_from_cart(request, product_id)
        
        if 'cart' in request.session:
            product_id_str = str(product_id)
            if product_id_str in request.session['cart']:
                request.session['cart'][product_id_str]['quantity'] = quantity
                
                # Update cart count
                cart = request.session['cart']
                total_items = sum(item['quantity'] for item in cart.values())
                request.session['cart_count'] = total_items
                request.session.modified = True
    
    return redirect('marche_smart:cart')
