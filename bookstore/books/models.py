from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

# 书籍数据表
class Book(models.Model):

    #分类
    CATEGORY_CHOICES = [
        ('literature', '文学艺术'),
        ('technology', '科技'),
        ('education', '教材'),
        ('life', '生活'),
        ('economics', '经济管理'),
        ('history', '历史文化'),
        ('psychology', '心理学'),
        ('other', '其他'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'  # 👈 建议默认改成这个
    )

    # 书名
    title = models.CharField(max_length=200)

    # 作者
    author = models.CharField(max_length=100)

    # 价格
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # 书籍描述
    description = models.TextField()

    # 封面图片
    image = models.ImageField(upload_to='books/', null=True, blank=True)

    # 库存
    stock = models.IntegerField(default=1)

    # 发布时间
    created_at = models.DateTimeField(auto_now_add=True)

    # 上传人
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

    # 后台显示名字
    def __str__(self):
        return self.title




# 购物车数据表
class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # 书
    quantity = models.IntegerField(default=1)  # 数量

    def __str__(self):
        return self.user.username

    @property
    def total_price(self):
        """自动计算购物车这一项的小计"""
        return self.book.price * self.quantity


# 新增订单表
# 新增订单表
class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', '未支付'),
        ('paid', '已支付'),
        ('not_shipped', '未发货'),
        ('shipped', '已发货'),
        ('received', '已收货'),
        ('refund', '退款中'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]

    # 用户
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # 收货地址
    address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # 总金额
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # 状态
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # 支付状态
    is_paid = models.BooleanField(default=False)
    # 发货状态
    is_shipped = models.BooleanField(default=False)
    # 收货状态
    is_received = models.BooleanField(default=False)
    # 退款状态
    is_refund = models.BooleanField(default=False)
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True)
    # 自动更新订单状态
    def update_status(self):

        # 超过30分钟未支付自动取消
        if not self.is_paid and timezone.now() - self.created_at > timedelta(minutes=30):
            self.status = 'cancelled'
            self.save()
            return

        if self.is_refund:
            self.status = 'refund'

        elif self.is_paid:

            if self.is_shipped:

                if self.is_received:
                    self.status = 'received'
                else:
                    self.status = 'shipped'

            else:
                self.status = 'not_shipped'

        else:
            self.status = 'pending'

        self.save()


# 订单项表
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

#收藏
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # 防止重复收藏

#消息
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


#地图
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    detail = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.receiver_name} - {self.province}{self.city}{self.district}{self.detail}"


# 商品图片（一个商品多张图）
class BookImage(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='books/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 自动设置封面
        if not self.book.image:
            self.book.image = self.image
            self.book.save()

#评论
class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

#论坛
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PostComment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)