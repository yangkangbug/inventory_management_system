#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例数据生成脚本
为库存管理系统添加一些示例数据
"""

from app import app, db, Category, Supplier, Product, StockTransaction

def create_sample_data():
    """创建示例数据"""
    with app.app_context():
        # 清空现有数据 (仅用于演示)
        db.session.query(StockTransaction).delete()
        db.session.query(Product).delete()
        db.session.query(Category).delete()
        db.session.query(Supplier).delete()
        
        # 创建分类
        categories = [
            Category(name="电子产品", description="电脑、手机、电子配件等"),
            Category(name="办公用品", description="文具、办公设备等"),
            Category(name="食品饮料", description="零食、饮料、食品等"),
            Category(name="日用百货", description="生活用品、清洁用品等")
        ]
        
        for category in categories:
            db.session.add(category)
        
        # 创建供应商
        suppliers = [
            Supplier(
                name="科技供应商有限公司",
                contact_person="张先生",
                phone="138-0000-1234",
                email="zhang@tech-supplier.com",
                address="深圳市南山区科技园"
            ),
            Supplier(
                name="办公设备专营店",
                contact_person="李女士",
                phone="139-0000-5678",
                email="li@office-supply.com",
                address="广州市天河区商业中心"
            ),
            Supplier(
                name="食品批发商城",
                contact_person="王经理",
                phone="137-0000-9012",
                email="wang@food-wholesale.com",
                address="上海市浦东新区食品城"
            )
        ]
        
        for supplier in suppliers:
            db.session.add(supplier)
        
        db.session.commit()
        
        # 获取创建的分类和供应商ID
        electronic_cat = Category.query.filter_by(name="电子产品").first()
        office_cat = Category.query.filter_by(name="办公用品").first()
        food_cat = Category.query.filter_by(name="食品饮料").first()
        daily_cat = Category.query.filter_by(name="日用百货").first()
        
        tech_supplier = Supplier.query.filter_by(name="科技供应商有限公司").first()
        office_supplier = Supplier.query.filter_by(name="办公设备专营店").first()
        food_supplier = Supplier.query.filter_by(name="食品批发商城").first()
        
        # 创建产品
        products = [
            # 电子产品
            Product(
                name="iPhone 15",
                description="苹果最新款智能手机",
                price=5999.00,
                quantity=25,
                low_stock_threshold=5,
                category_id=electronic_cat.id,
                supplier_id=tech_supplier.id
            ),
            Product(
                name="MacBook Air M3",
                description="苹果笔记本电脑",
                price=8999.00,
                quantity=8,
                low_stock_threshold=3,
                category_id=electronic_cat.id,
                supplier_id=tech_supplier.id
            ),
            Product(
                name="无线充电器",
                description="支持多设备无线充电",
                price=199.00,
                quantity=50,
                low_stock_threshold=15,
                category_id=electronic_cat.id,
                supplier_id=tech_supplier.id
            ),
            
            # 办公用品
            Product(
                name="办公椅",
                description="人体工学办公椅",
                price=899.00,
                quantity=15,
                low_stock_threshold=5,
                category_id=office_cat.id,
                supplier_id=office_supplier.id
            ),
            Product(
                name="激光打印机",
                description="黑白激光打印机",
                price=1299.00,
                quantity=6,
                low_stock_threshold=3,
                category_id=office_cat.id,
                supplier_id=office_supplier.id
            ),
            Product(
                name="A4复印纸",
                description="80g A4白色复印纸 500张/包",
                price=25.00,
                quantity=100,
                low_stock_threshold=20,
                category_id=office_cat.id,
                supplier_id=office_supplier.id
            ),
            
            # 食品饮料
            Product(
                name="矿泉水",
                description="550ml瓶装矿泉水",
                price=2.50,
                quantity=200,
                low_stock_threshold=50,
                category_id=food_cat.id,
                supplier_id=food_supplier.id
            ),
            Product(
                name="咖啡豆",
                description="意式浓缩咖啡豆 1kg装",
                price=158.00,
                quantity=3,  # 低库存示例
                low_stock_threshold=5,
                category_id=food_cat.id,
                supplier_id=food_supplier.id
            ),
            
            # 日用百货
            Product(
                name="洗手液",
                description="免洗手消毒液 500ml",
                price=28.00,
                quantity=2,  # 低库存示例
                low_stock_threshold=10,
                category_id=daily_cat.id
            ),
            Product(
                name="垃圾袋",
                description="加厚垃圾袋 45L 100只装",
                price=35.00,
                quantity=80,
                low_stock_threshold=20,
                category_id=daily_cat.id
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        
        # 创建一些库存事务记录
        from datetime import datetime, timedelta
        
        # 获取产品用于创建事务
        iphone = Product.query.filter_by(name="iPhone 15").first()
        macbook = Product.query.filter_by(name="MacBook Air M3").first()
        water = Product.query.filter_by(name="矿泉水").first()
        
        transactions = [
            StockTransaction(
                product_id=iphone.id,
                transaction_type='in',
                quantity=30,
                notes='初始库存入库',
                created_at=datetime.utcnow() - timedelta(days=7)
            ),
            StockTransaction(
                product_id=iphone.id,
                transaction_type='out',
                quantity=5,
                notes='销售出库',
                created_at=datetime.utcnow() - timedelta(days=3)
            ),
            StockTransaction(
                product_id=macbook.id,
                transaction_type='in',
                quantity=10,
                notes='新采购入库',
                created_at=datetime.utcnow() - timedelta(days=5)
            ),
            StockTransaction(
                product_id=macbook.id,
                transaction_type='out',
                quantity=2,
                notes='客户订单出库',
                created_at=datetime.utcnow() - timedelta(days=1)
            ),
            StockTransaction(
                product_id=water.id,
                transaction_type='in',
                quantity=250,
                notes='大批量采购',
                created_at=datetime.utcnow() - timedelta(days=10)
            ),
            StockTransaction(
                product_id=water.id,
                transaction_type='out',
                quantity=50,
                notes='员工福利发放',
                created_at=datetime.utcnow() - timedelta(days=2)
            )
        ]
        
        for transaction in transactions:
            db.session.add(transaction)
        
        db.session.commit()
        
        print("✅ 示例数据创建成功！")
        print(f"📦 创建了 {len(categories)} 个分类")
        print(f"🏢 创建了 {len(suppliers)} 个供应商")
        print(f"📱 创建了 {len(products)} 个产品")
        print(f"📊 创建了 {len(transactions)} 条库存事务记录")
        print("\n🔍 低库存产品预警:")
        
        low_stock_products = [p for p in Product.query.all() if p.is_low_stock]
        for product in low_stock_products:
            print(f"   ⚠️  {product.name}: {product.quantity} (阈值: {product.low_stock_threshold})")

if __name__ == "__main__":
    create_sample_data()