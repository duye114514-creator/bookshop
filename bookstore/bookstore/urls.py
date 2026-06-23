from django.contrib import admin
from django.urls import path
from books import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # 首页和书籍详情
    path('', views.book_list, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),


    # 用户注册/登录/登出
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('buy/<int:book_id>/', views.buy_now, name='buy_now'),
    # 购物车
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_cart_ajax/', views.update_cart_ajax, name='update_cart_ajax'),
    path('batch_delete/', views.batch_delete, name='batch_delete'),

    # 我的书
    path('my_books/', views.my_books, name='my_books'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),

    # 个人中心
    path('profile/', views.profile, name='profile'),


    # 地址管理（整合个人中心）
    path('address/add/', views.address_add, name='address_add'),
    path('address/edit/<int:addr_id>/', views.address_edit, name='address_edit'),
    path('address/', views.address_list, name='address_list'),       # 地址列表
    path('address/delete/<int:addr_id>/', views.delete_address, name='delete_address'),

    #订单
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/direct/<int:order_id>/', views.checkout_direct, name='checkout_direct'),
    #支付
    path('pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    #收藏
    path('toggle_fav/<int:book_id>/', views.toggle_fav, name='toggle_fav'),

    #评论
    path('comment/<int:book_id>/', views.add_comment, name='add_comment'),
    #删评论
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    #论坛
    path('forum/add/', views.add_post, name='add_post'),
    path('forum/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/comment/<int:post_id>/', views.add_post_comment, name='add_post_comment'),
    path('forum/', views.forum, name='forum'),
    #删帖
    path('forum/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    #编辑帖子
    path('forum/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    #搜索
    path('search/', views.search, name='search'),
    #分类
    path('category/<str:category_name>/', views.category_view, name='category'),
    #退款
    path('refund/<int:order_id>/', views.refund_order, name='refund_order'),
    #退款成功
    path('refund_complete/<int:order_id>/', views.complete_refund, name='complete_refund'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
