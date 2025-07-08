#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存管理系统 (Inventory Management System)
主应用程序入口
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'inventory-management-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 定义数据库模型
class Category(db.Model):
    """商品分类模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    products = db.relationship('Product', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Supplier(db.Model):
    """供应商模型"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    products = db.relationship('Product', backref='supplier', lazy=True)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'

class Product(db.Model):
    """产品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False, default=0.0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    
    # 关系
    transactions = db.relationship('StockTransaction', backref='product', lazy=True)
    
    @property
    def total_value(self):
        """计算总价值"""
        return self.quantity * self.price
    
    @property
    def is_low_stock(self):
        """检查是否低库存"""
        return self.quantity <= self.low_stock_threshold
    
    def __repr__(self):
        return f'<Product {self.name}>'

class StockTransaction(db.Model):
    """库存事务模型 - 记录所有库存变动"""
    __tablename__ = 'stock_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'in' 或 'out'
    quantity = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<StockTransaction {self.transaction_type} {self.quantity}>'

# 创建数据库表
with app.app_context():
    db.create_all()

# 主页路由
@app.route('/')
def index():
    """首页 - 显示库存概览"""
    products = Product.query.all()
    total_products = len(products)
    low_stock_products = [p for p in products if p.quantity <= p.low_stock_threshold]
    total_value = sum(p.quantity * p.price for p in products)
    
    return render_template('index.html', 
                         total_products=total_products,
                         low_stock_count=len(low_stock_products),
                         total_value=total_value,
                         recent_products=products[:5])

# 产品管理路由
@app.route('/products')
def products():
    """产品列表页面"""
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """添加新产品"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        low_stock_threshold = int(request.form.get('low_stock_threshold', 10))
        category_id = request.form.get('category_id')
        supplier_id = request.form.get('supplier_id')
        
        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            low_stock_threshold=low_stock_threshold,
            category_id=category_id if category_id else None,
            supplier_id=supplier_id if supplier_id else None
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('产品添加成功！', 'success')
        return redirect(url_for('products'))
    
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    return render_template('add_product.html', categories=categories, suppliers=suppliers)

@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    """编辑产品"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form.get('description', '')
        product.price = float(request.form['price'])
        product.quantity = int(request.form['quantity'])
        product.low_stock_threshold = int(request.form.get('low_stock_threshold', 10))
        product.category_id = request.form.get('category_id') if request.form.get('category_id') else None
        product.supplier_id = request.form.get('supplier_id') if request.form.get('supplier_id') else None
        
        db.session.commit()
        flash('产品更新成功！', 'success')
        return redirect(url_for('products'))
    
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    return render_template('edit_product.html', product=product, categories=categories, suppliers=suppliers)

@app.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """删除产品"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('产品删除成功！', 'success')
    return redirect(url_for('products'))

# 库存调整路由
@app.route('/stock/adjust/<int:product_id>', methods=['GET', 'POST'])
def adjust_stock(product_id):
    """调整库存"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        transaction_type = request.form['transaction_type']  # 'in' 或 'out'
        quantity = int(request.form['quantity'])
        notes = request.form.get('notes', '')
        
        if transaction_type == 'in':
            product.quantity += quantity
        else:
            if product.quantity >= quantity:
                product.quantity -= quantity
            else:
                flash('库存不足！', 'error')
                return redirect(url_for('adjust_stock', product_id=product_id))
        
        # 记录库存事务
        transaction = StockTransaction(
            product_id=product_id,
            transaction_type=transaction_type,
            quantity=quantity,
            notes=notes
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash('库存调整成功！', 'success')
        return redirect(url_for('products'))
    
    return render_template('adjust_stock.html', product=product)

# 分类管理路由
@app.route('/categories')
def categories():
    """分类列表"""
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """添加分类"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash('分类添加成功！', 'success')
        return redirect(url_for('categories'))
    
    return render_template('add_category.html')

# 供应商管理路由
@app.route('/suppliers')
def suppliers():
    """供应商列表"""
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    """添加供应商"""
    if request.method == 'POST':
        name = request.form['name']
        contact_person = request.form.get('contact_person', '')
        phone = request.form.get('phone', '')
        email = request.form.get('email', '')
        address = request.form.get('address', '')
        
        supplier = Supplier(
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address
        )
        
        db.session.add(supplier)
        db.session.commit()
        
        flash('供应商添加成功！', 'success')
        return redirect(url_for('suppliers'))
    
    return render_template('add_supplier.html')

# 报告路由
@app.route('/reports')
def reports():
    """报告页面"""
    products = Product.query.all()
    low_stock_products = [p for p in products if p.quantity <= p.low_stock_threshold]
    transactions = StockTransaction.query.order_by(StockTransaction.created_at.desc()).limit(10).all()
    
    return render_template('reports.html', 
                         low_stock_products=low_stock_products,
                         recent_transactions=transactions)

# API路由 (用于AJAX请求)
@app.route('/api/products')
def api_products():
    """获取所有产品的API"""
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'quantity': p.quantity,
        'price': p.price,
        'category': p.category.name if p.category else None,
        'supplier': p.supplier.name if p.supplier else None
    } for p in products])

@app.route('/api/low-stock')
def api_low_stock():
    """获取低库存产品的API"""
    products = Product.query.all()
    low_stock = [p for p in products if p.quantity <= p.low_stock_threshold]
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'quantity': p.quantity,
        'threshold': p.low_stock_threshold
    } for p in low_stock])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)