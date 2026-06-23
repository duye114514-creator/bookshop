# 📚 书籍销售平台（BookShop System）

## 📌 项目简介

本项目是一个基于 Django 开发的书籍销售平台，实现用户注册登录、书籍浏览、搜索、购物车、订单管理以及评论等功能。

该项目为个人毕业设计，用于练习前后端开发与数据库设计能力。

---

## 🛠 技术栈

- 后端：Python / Django
- 数据库：SQLite
- 前端：HTML / CSS / JavaScript
- 工具：Git / GitHub / VS Code

---

## 🎯 功能模块

- 用户注册 / 登录
- 书籍分类展示
- 书籍搜索
- 购物车管理
- 订单管理
- 评论功能
- Django 后台管理

---

## 🚀 项目运行步骤

### 1. 创建虚拟环境（如未创建）

python -m venv venv

---

### 2. 激活虚拟环境（Windows PowerShell）

.\venv\Scripts\Activate.ps1

---

### 3. 安装依赖

pip install django  
pip install pillow

---

### 4. 数据库迁移

python manage.py makemigrations  
python manage.py migrate

---

### 5. 启动项目

python manage.py runserver

访问地址：

http://127.0.0.1:8000/

---

## ⚠️ 开发过程中遇到的问题记录

### 1. 虚拟环境无法激活（PowerShell 报错）

问题现象：
无法直接使用 venv\Scripts\activate

原因：
PowerShell 不支持该写法

解决方法：

.\venv\Scripts\Activate.ps1

---

### 2. Django 未安装

错误信息：
ModuleNotFoundError: No module named 'django'

解决方法：

pip install django

---

### 3. ImageField 报错（缺少 Pillow）

错误信息：
Cannot use ImageField because Pillow is not installed

解决方法：

pip install pillow

---

### 4. manage.py 找不到

错误信息：
can't open file 'manage.py'

原因：
没有进入 Django 项目目录

解决方法：

cd bookshop/bookstore

---



## 🎓 项目收获

- 熟悉 Django 后端开发流程
- 掌握数据库 ORM 使用
- 掌握前后端基础交互方式
- 熟悉虚拟环境与依赖管理
