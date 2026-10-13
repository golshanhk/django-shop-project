from . import views

from django.urls import path


app_name = "home"


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "product/",
        views.all_product,
        name="product"
    ),

    path(
        "category/slug:<slug>/",
        views.all_product,
        name="category"
    ),

    path(
        "detail/<int:id>/",
        views.product_detail,
        name="detail"
    ),

    path(
        "product/<int:id>/",
        views.product_likes,
        name="product_likes"
    ),

    path(
        "dislike/<int:id>/",
        views.product_dislike,
        name="product_dislike"
    ),

    path(
        "comment<int:id>/",
        views.product_comment,
        name="product_comment"
    ),

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        'reply/<int:id>/<int:comment_id>',
        views.Reply,
        name='Reply'
    ),

    path('delete_comment/<int:id>',
        views.delete_comment,
        name='delete_comment'

    ),

    path('search/',
        views.product_search,
        name='product_search'
        ),

    path(
    'cart/increase/<str:id>/',
    views.increase_cart,
    name='increase_cart'
    ),

    path(
        'cart/decrease/<str:id>/',
        views.decrease_cart,
        name='decrease_cart'
    ),

    path(
        'cart/remove/<str:id>/',
        views.remove_cart,
        name='remove_cart'
    ),    
]