#from django.shortcuts import render, get_object_or_404
from .models import Book, Cart, Order, OrderItem, Post, PostComment
from django.contrib.auth import logout
from .forms import BookForm
from .models import Order, Favorite, Message
from .forms import AddressForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Cart, Order, OrderItem, Address
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect



# 首页书籍列表
def book_list(request):
    category = request.GET.get('category')

    if category:
        books = Book.objects.filter(category=category)
    else:
        books = Book.objects.all()

    return render(request, "book_list.html", {
        "books": books,
        "current_category": category
    })






# 用户注册 显示注册页面 提交后创建用户
def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

# 登出
def logout_view(request):
    logout(request)
    return redirect('/login/')

#找到当前用户的所有购物车商品传给网页显示
from .models import Cart

def cart(request):

    carts = Cart.objects.filter(user=request.user)

    return render(request, "cart.html", {"carts": carts})


# ================== 购物车功能 ==================

# 查看购物车
@login_required
def cart_view(request):
    """
    显示购物车页面，包括每一项的小计和总价
    """
    carts = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in carts)  # 自动计算总价
    return render(request, "cart.html", {"carts": carts, "total": total})


# 添加商品到购物车
@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # 如果该用户已有该商品，数量+1，否则创建新条目
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('/cart/')


# 删除购物车项
@login_required
def remove_from_cart(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id, user=request.user)
    item.delete()
    return redirect('/cart/')


# 更新购物车数量（通过表单 POST）
@login_required
def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('qty_'):
                cart_id = int(key.split('_')[1])
                cart_item = Cart.objects.get(id=cart_id, user=request.user)
                cart_item.quantity = int(value)
                cart_item.save()
    return redirect('/cart/')



from .models import Cart


#购物车批量修改
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Cart

@csrf_exempt
def batch_delete(request):
    if request.method=="POST":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Cart.objects.filter(id__in=ids).delete()
        return JsonResponse({"success": True})

@csrf_exempt
def update_cart_ajax(request):
    if request.method=="POST":
        for key, value in request.POST.items():
            if key.startswith('qty_'):
                cid = key.split('_')[1]
                try:
                    cart_item = Cart.objects.get(id=cid, user=request.user)
                    cart_item.quantity = int(value)
                    cart_item.save()
                except:
                    pass
        return JsonResponse({"success": True})



# 我的书籍（普通用户管理自己发布的书）
@login_required
def my_books(request):
    books = Book.objects.filter(owner=request.user)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()

            print("书籍添加成功")

            return redirect('my_books')

        else:
            print(form.errors)   # 👈 关键调试

    else:
        form = BookForm()

    return render(request, "my_books.html", {
        "books": books,
        "form": form
    })

#删除书籍
@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, owner=request.user)
    book.delete()
    return redirect('my_books')

#编辑书籍
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, owner=request.user)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('my_books')
    else:
        form = BookForm(instance=book)

    return render(request, "edit_book.html", {"form": form})


#个人中心
@login_required
def profile(request):
    user = request.user
    selected_subtab = request.GET.get('subtab', 'all')

    # 获取所有订单并自动更新状态
    orders = Order.objects.filter(user=user).order_by('-created_at')
    for order in orders:
        order.update_status()

    # 根据二级导航筛选
    if selected_subtab == 'unpaid':
        orders = orders.filter(is_paid=False)
    elif selected_subtab == 'paid':
        orders = orders.filter(is_paid=True)
    elif selected_subtab == 'shipped':
        orders = orders.filter(is_shipped=True, is_received=False)
    elif selected_subtab == 'not_shipped':
        orders = orders.filter(is_shipped=False, is_paid=True)
    elif selected_subtab == 'received':
        orders = orders.filter(is_received=True)
    elif selected_subtab == 'refund':
       orders = orders.filter(is_refund=True)
    elif selected_subtab == 'cancelled':
        orders = orders.filter(status='refund')


    # 查询用户地址
    addresses = Address.objects.filter(user=request.user)


    context = {
        'orders': orders,
        'selected_subtab': selected_subtab,
        'favorites': Favorite.objects.filter(user=user),
        'messages': Message.objects.filter(user=user),
        'addresses': addresses,
    }
    return render(request, 'profile.html', context)


# 地址列表
@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'address_list.html', {'addresses': addresses})

# ------------------ 新增地址 ------------------
@login_required
def address_add(request):
    if request.method == "POST":
        Address.objects.create(
            user=request.user,
            receiver_name=request.POST['recipient'],
            phone=request.POST['phone'],
            province=request.POST.get('province', ''),
            city=request.POST.get('city', ''),
            district=request.POST.get('district', ''),
            detail=request.POST['detail'],
            postal_code=request.POST.get('postal_code', ''),
            is_default=False
        )
    return redirect('/profile/#address')




# ------------------ 删除地址 ------------------
@login_required
def delete_address(request, addr_id):
    Address.objects.filter(id=addr_id, user=request.user).delete()
    return redirect('/profile/#address')


# ------------------ 编辑地址 ------------------
@login_required
def address_edit(request, addr_id):
    address = get_object_or_404(Address, id=addr_id, user=request.user)
    if request.method == "POST":
        address.receiver_name = request.POST['recipient']
        address.phone = request.POST['phone']
        address.province = request.POST.get('province', '')
        address.city = request.POST.get('city', '')
        address.district = request.POST.get('district', '')
        address.detail = request.POST['detail']
        address.postal_code = request.POST.get('postal_code', '')
        address.save()
        return redirect('/profile/#address')
    return render(request, 'address_edit.html', {'address': address})


#我的订单

#支付
#购物车
@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        return redirect('cart')

    addresses = Address.objects.filter(user=request.user)
    total_price = sum(i.book.price * i.quantity for i in cart_items)

    if request.method == "POST":

        address_id = request.POST.get("address")
        address = get_object_or_404(Address, id=address_id, user=request.user)

        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            address=address
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )

        cart_items.delete()

        return redirect('order_detail', order_id=order.id)

    return render(request, "checkout.html", {
        "items": cart_items,
        "total_price": total_price,
        "addresses": addresses
    })


#订单详情
@login_required
def order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    order.update_status()

    return render(request, "order_detail.html", {
        "order": order,
        "items": order.items.all()
    })


@login_required
def pay_order(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    # 防止重复支付
    if order.is_paid:
        return redirect('order_detail', order_id=order.id)

    # 防止退款单支付
    if order.status == 'refund':
        return redirect('order_detail', order_id=order.id)

    order.is_paid = True
    order.save()

    order.update_status()

    return redirect('order_detail', order_id=order.id)
#详情页视图
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    images = book.images.all()  # 多图

    is_fav = False
    if request.user.is_authenticated:
        is_fav = Favorite.objects.filter(user=request.user, book=book).exists()

        #评论
        comments = book.comments.all().order_by('-created_at')

    return render(request, 'book_detail.html', {
        'book': book,
        'images': images,
        'is_fav': is_fav,
        'comments': comments
    })


#收藏
from django.http import JsonResponse
from .models import Favorite

@login_required
def toggle_fav(request, book_id):
    book = Book.objects.get(id=book_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if not created:
        fav.delete()
        return JsonResponse({'status': 'removed'}) #取消收藏
    else:
        return JsonResponse({'status': 'added'})  # 收藏成功


#评论
from .models import Comment
from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, book_id):
    if request.method == "POST":
        content = request.POST.get("content")
        book = Book.objects.get(id=book_id)

        Comment.objects.create(
            user=request.user,
            book=book,
            content=content
        )

    return redirect('book_detail', book_id=book_id)


#删除评论
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    book_id = comment.book.id
    comment.delete()

    return redirect('book_detail', book_id=book_id)

#论坛
def book_list(request):
    books = Book.objects.all()
    posts = Post.objects.all().order_by('-id')

    return render(request, "book_list.html", {
        "books": books,
        "posts": posts
    })


def forum_page(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum.html', {'posts': posts})

#发帖
@login_required
def forum(request):

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        print("POST进来了")  # 🔥调试用

        Post.objects.create(
            title=title,
            content=content,
            user=request.user
        )

        print("创建成功")

        return redirect('forum')

    posts = Post.objects.all().order_by('-id')

    return render(request, 'forum.html', {
        'posts': posts
    })
#删帖
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('forum')

#编辑帖子
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'edit_post.html', {'post': post})

@login_required
def add_post(request):
    if request.method == "POST":
        Post.objects.create(
            user=request.user,
            title=request.POST['title'],
            content=request.POST['content']
        )
        return redirect('forum')

    return render(request, 'add_post.html')


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})


@login_required
def add_post_comment(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        PostComment.objects.create(
            user=request.user,
            post=post,
            content=request.POST['content']
        )

    return redirect('post_detail', post_id=post_id)

#搜索页面
def search(request):
    query = request.GET.get('q')

    results = []
    if query:
        results = Book.objects.filter(title__icontains=query)

    return render(request, 'search.html', {
        'query': query,
        'results': results
    })

#分类
def category_view(request, category_name):
    books = Book.objects.filter(category=category_name)

    #把 choices 转成字典
    CATEGORY_DICT = dict(Book.CATEGORY_CHOICES)

    # 根据英文拿中文
    category_display = CATEGORY_DICT.get(category_name)

    return render(request, 'category.html', {
        'books': books,
        'category': category_display
    })

#立即购买
@login_required
def buy_now(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    order = Order.objects.create(
        user=request.user,
        total_price=book.price,
        is_paid=False
    )

    OrderItem.objects.create(
        order=order,
        book=book,
        quantity=1,
        price=book.price
    )

    # 👉 直接进入“确认订单页面”
    return redirect('checkout_direct', order_id=order.id)

@login_required
def checkout_direct(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        address_id = request.POST.get("address")
        address = get_object_or_404(Address, id=address_id, user=request.user)

        order.address = address
        order.save()

        return redirect('order_detail', order_id=order.id)

    return render(request, "checkout.html", {
        "order": order,
        "items": order.items.all(),
        "total_price": order.total_price,
        "addresses": addresses
    })

#退款
@login_required
def refund_order(request, order_id):
    print("进入退款函数")
    order = Order.objects.get(id=order_id, user=request.user)
    print("当前状态：", order.status)
    # 👉强制改，不加任何条件
    order.status = 'refund'
    order.is_paid = False
    order.save()
    return redirect('order_detail', order_id=order.id)
#退款成功
@login_required
def complete_refund(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if order.status == 'refund':
        order.status = 'refunded'
        order.save()

        # 👉 恢复库存
        for item in order.items.all():
            item.book.stock += item.quantity
            item.book.save()

    return redirect('order_detail', order_id=order.id)