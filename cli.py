#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存管理系统命令行工具
提供快速操作接口
"""

import argparse
import sys
from app import app, db, Product, Category, Supplier, StockTransaction

def list_products():
    """列出所有产品"""
    with app.app_context():
        products = Product.query.all()
        if not products:
            print("📦 暂无产品")
            return
        
        print("📦 产品列表:")
        print("-" * 80)
        print(f"{'ID':<5} {'名称':<20} {'数量':<8} {'价格':<10} {'状态':<8} {'分类':<15}")
        print("-" * 80)
        
        for product in products:
            status = "⚠️ 低库存" if product.is_low_stock else "✅ 正常"
            category = product.category.name if product.category else "未分类"
            print(f"{product.id:<5} {product.name:<20} {product.quantity:<8} ¥{product.price:<9.2f} {status:<8} {category:<15}")

def list_low_stock():
    """列出低库存产品"""
    with app.app_context():
        products = Product.query.all()
        low_stock_products = [p for p in products if p.is_low_stock]
        
        if not low_stock_products:
            print("✅ 没有低库存产品")
            return
        
        print("⚠️ 低库存产品警告:")
        print("-" * 60)
        print(f"{'产品名称':<20} {'当前库存':<10} {'阈值':<8} {'建议采购':<10}")
        print("-" * 60)
        
        for product in low_stock_products:
            recommend = max(product.low_stock_threshold * 2 - product.quantity, 0)
            print(f"{product.name:<20} {product.quantity:<10} {product.low_stock_threshold:<8} {recommend:<10}")

def add_product(name, price, quantity, description="", category_name="", supplier_name=""):
    """添加新产品"""
    with app.app_context():
        # 查找分类
        category = None
        if category_name:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                print(f"❌ 分类 '{category_name}' 不存在")
                return False
        
        # 查找供应商
        supplier = None
        if supplier_name:
            supplier = Supplier.query.filter_by(name=supplier_name).first()
            if not supplier:
                print(f"❌ 供应商 '{supplier_name}' 不存在")
                return False
        
        # 创建产品
        product = Product(
            name=name,
            description=description,
            price=float(price),
            quantity=int(quantity),
            category_id=category.id if category else None,
            supplier_id=supplier.id if supplier else None
        )
        
        db.session.add(product)
        db.session.commit()
        
        print(f"✅ 产品 '{name}' 添加成功 (ID: {product.id})")
        return True

def adjust_stock(product_id, operation, quantity, notes=""):
    """调整库存"""
    with app.app_context():
        product = Product.query.get(product_id)
        if not product:
            print(f"❌ 产品 ID {product_id} 不存在")
            return False
        
        quantity = int(quantity)
        
        if operation == 'in':
            product.quantity += quantity
            print(f"📦 入库: {product.name} +{quantity}, 新库存: {product.quantity}")
        elif operation == 'out':
            if product.quantity < quantity:
                print(f"❌ 库存不足! 当前库存: {product.quantity}, 请求出库: {quantity}")
                return False
            product.quantity -= quantity
            print(f"📤 出库: {product.name} -{quantity}, 新库存: {product.quantity}")
        else:
            print("❌ 操作类型错误，请使用 'in' 或 'out'")
            return False
        
        # 记录事务
        transaction = StockTransaction(
            product_id=product_id,
            transaction_type=operation,
            quantity=quantity,
            notes=notes
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        # 检查是否变为低库存
        if product.is_low_stock:
            print(f"⚠️ 警告: {product.name} 库存已低于阈值 {product.low_stock_threshold}")
        
        return True

def show_summary():
    """显示库存概要"""
    with app.app_context():
        products = Product.query.all()
        categories = Category.query.all()
        suppliers = Supplier.query.all()
        
        total_products = len(products)
        total_value = sum(p.total_value for p in products)
        low_stock_count = len([p for p in products if p.is_low_stock])
        
        print("📊 库存管理系统概要")
        print("=" * 40)
        print(f"总产品数量: {total_products}")
        print(f"总库存价值: ¥{total_value:.2f}")
        print(f"低库存产品: {low_stock_count}")
        print(f"产品分类数: {len(categories)}")
        print(f"供应商数量: {len(suppliers)}")
        print("=" * 40)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='库存管理系统命令行工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 列出产品
    subparsers.add_parser('list', help='列出所有产品')
    
    # 低库存产品
    subparsers.add_parser('low-stock', help='显示低库存产品')
    
    # 概要信息
    subparsers.add_parser('summary', help='显示库存概要')
    
    # 添加产品
    add_parser = subparsers.add_parser('add', help='添加新产品')
    add_parser.add_argument('name', help='产品名称')
    add_parser.add_argument('price', type=float, help='产品价格')
    add_parser.add_argument('quantity', type=int, help='初始数量')
    add_parser.add_argument('--description', default='', help='产品描述')
    add_parser.add_argument('--category', default='', help='分类名称')
    add_parser.add_argument('--supplier', default='', help='供应商名称')
    
    # 调整库存
    stock_parser = subparsers.add_parser('stock', help='调整库存')
    stock_parser.add_argument('product_id', type=int, help='产品ID')
    stock_parser.add_argument('operation', choices=['in', 'out'], help='操作类型: in(入库) 或 out(出库)')
    stock_parser.add_argument('quantity', type=int, help='数量')
    stock_parser.add_argument('--notes', default='', help='备注')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'list':
            list_products()
        elif args.command == 'low-stock':
            list_low_stock()
        elif args.command == 'summary':
            show_summary()
        elif args.command == 'add':
            add_product(args.name, args.price, args.quantity, 
                       args.description, args.category, args.supplier)
        elif args.command == 'stock':
            adjust_stock(args.product_id, args.operation, args.quantity, args.notes)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()