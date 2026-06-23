from django.contrib import admin
from .models import Book,Cart

# 把Book表加入后台

#把购物车加入后台
admin.site.register(Cart)

#后台多图上传
from django.contrib import admin
from .models import Book, BookImage

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1  # 默认显示1个上传框

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BookImageInline]