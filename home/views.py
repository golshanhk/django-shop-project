
from django.db.models import Q
from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
def home(request):
    category = Category.objects.filter(sub_category__isnull=True)
    return render(request, "home/home.html", {'category': category})
def all_product(request, slug=None,id=None):

    products = Product.objects.all()
    categories = Category.objects.filter(sub_cat=False)


    if slug :
        data = get_object_or_404(Category, slug=slug)

        if data.sub.exists():

            children = data.sub.all()

            products = Product.objects.filter(
                category__in=children
            ) | products.filter(
                category=data
            )

        else:
            products = products.filter(category=data)
        

    return render(
        request,
        "home/product.html",
        {
            'products': products,
            'category': categories,
       
            
        })
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    comment_form =CommentForm()
    comments = Comment.objects.filter(product_id=id,is_reply=False).order_by("-id")
    similar = product.tags.similar_objects()[:4]
    variant = Variant.objects.filter(product_variant_id=id)
    variants = variant.first()
    reply_form = ReplyForm()

    if request.method == 'POST':
        var_id = request.POST.get('select')

        if var_id:
            variants = get_object_or_404(
                Variant,
                id=var_id
            )
    return render(
        request,
        'home/detail.html',
        {
            'product': product,
            'variant': variant,
            'variants': variants,
            'similar': similar,
            'comment_form' : comment_form,
            'comments' : comments,
            'reply_form': reply_form,
        }
    )
@login_required
def product_likes(request, id):
    product = get_object_or_404(Product, id=id)

    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        messages.success(request, 'Your like removed')
    else:
        product.dislike.remove(request.user) 
        product.like.add(request.user)
        messages.success(request, 'Thanks for your reaction')

    return redirect('home:detail', product.id)
@login_required
def product_dislike(request, id):
    product = get_object_or_404(Product, id=id)

    if product.dislike.filter(id=request.user.id).exists():
        product.dislike.remove(request.user)
        messages.success(request, 'Your dislike removed')
    else:
        product.like.remove(request.user)  
        product.dislike.add(request.user)
        messages.success(request, 'Thanks for your reaction')

    return redirect('home:detail', product.id)

@login_required
def product_comment(request , id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(
                comment = data['comment'],
                rate=data['rate'],
                user_id=request.user.id,
                product_id =id )
    return redirect(url) 

@login_required
def Reply(request, id,comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST" :
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(

                comment = data['comment'],
                product_id =id,
                user_id=request.user.id,
                reply_id = comment_id,
                is_reply = True

            )
            
            messages.success(
                request,
                "thanks for sharing your opinion "
            )

            return redirect(url)
     
def add_to_cart(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    cart_data = request.session.get(
        "cart",
        {}
    )

    product_id = str(product.id)

    if product_id in cart_data:

        cart_data[product_id] += 1

    else:

        cart_data[product_id] = 1

    request.session["cart"] = cart_data

    messages.success(
        request,
        "Product added to cart"
    )

    return redirect(
        "home:detail",
        product.id
    )


def cart(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    products = []

    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = (
            product.total_price *
            quantity
        )

        total += subtotal

        products.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "home/cart.html",
        {
            "products": products,
            "total": total,
        }
    )
@login_required
def delete_comment(request, id):

    comment = get_object_or_404(
        Comment,
        id=id
    )


    if comment.user != request.user:
        messages.error(
            request,
            "You cannot delete this comment"
        )

        return redirect(
            request.META.get('HTTP_REFERER')
        )


    comment.delete()


    messages.success(
        request,
        "Deleted successfully"
    )


    return redirect(
        request.META.get('HTTP_REFERER')
    )

def product_search(request):

    query = request.GET.get('search', '').strip()

    products = Product.objects.all()


    if query:

        products = products.filter(
            Q(name__icontains=query) |
            Q(information__icontains=query)
        )


    return render(
        request,
        'home/product.html',
        {
            'products': products,
            'query': query,
        }
    )

def increase_cart(request, id):

    cart_data = request.session.get(
        "cart",
        {}
    )

    if id in cart_data:
        cart_data[id] += 1

    request.session["cart"] = cart_data

    return redirect("home:cart") 

def decrease_cart(request, id):

    cart_data = request.session.get(
        "cart",
        {}
    )

    if id in cart_data:

        if cart_data[id] > 1:
            cart_data[id] -= 1

        else:
            del cart_data[id]


    request.session["cart"] = cart_data

    return redirect("home:cart")

def remove_cart(request, id):

    cart_data = request.session.get(
        "cart",
        {}
    )


    if id in cart_data:
        del cart_data[id]


    request.session["cart"] = cart_data


    messages.success(
        request,
        "Product removed from cart"
    )


    return redirect("home:cart")