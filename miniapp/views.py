#views.py
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import Addforms
from .models import bag,Cart,registerr
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as logout
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Cart, PurchaseHistory
# Create your views here.
def main(request):
    return render(request,"product.html")

def detailsadd(request):
    form = Addforms()
    if request.method == "POST":
        form = Addforms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request,"form.html",{'form': form})

def productdetails(request):
    return render(request,'productmain.html')

def vieww(request):
    query = request.GET.get("search", "")  
    if query:
        cr = bag.objects.filter(name=query)  
    else:
        cr = bag.objects.all()  

    return render(request, "productmain.html", {'cr': cr, 'query': query})


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)  
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})


@login_required(login_url='/login/')
def update_cart(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        action = request.POST.get("action")
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)  # Ensure user owns the cart item

        if action == "increment":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrement":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()  # Remove item if quantity is zero
        elif action == "remove":
            cart_item.delete()  # Directly remove item from cart

    return redirect("cart")



@login_required(login_url='/login/')  
def add_to_cart(request, product_id):
    product = get_object_or_404(bag, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart successfully!")
    return redirect('cart')
    

def register(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        age = request.POST.get("age")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if registerr.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        registerr.objects.create(name=name, age=age, phone=phone, email=email, username=username, password=password)

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, "register.html")



def userlog(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Correct usage
            messages.success(request, "Login successful!")
            return redirect("viewproduct")  # Redirect to your homepage
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")  # Redirect back to login page

    return render(request, "login.html")


def logoutuser(request):
    logout(request)
    return redirect("main")
def loginn(request):
    return render(request,'login.html')
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("cart")

    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        # Process checkout
        for item in cart_items:
            PurchaseHistory.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.total_price(),
            )
            item.delete()  # Remove from cart after purchase

        messages.success(request, "Order placed successfully!")
        return redirect("purchase_history")

    return render(request, "checkout.html", {"cart_items": cart_items, "total_price": total_price})





@login_required
def purchase_history(request):
    history_items = PurchaseHistory.objects.filter(user=request.user)
    return render(request, "purchase_history.html", {"history_items": history_items})


@login_required
def download_purchase_history(request):
    history_items = PurchaseHistory.objects.filter(user=request.user)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 800, f"Purchase History for {request.user.username}")

    y = 780
    for item in history_items:
        pdf.drawString(100, y, f"{item.product.name} - Quantity: {item.quantity} - Total: ${item.total_price}")
        y -= 20

    pdf.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="purchase_history.pdf")

def contact(request):
    return render(request,'contact.html')