#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存管理系统基本测试
"""

import unittest
import tempfile
import os
from app import app, db, Product, Category, Supplier, StockTransaction

class InventorySystemTestCase(unittest.TestCase):
    
    def setUp(self):
        """设置测试环境"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """清理测试环境"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_home_page(self):
        """测试首页加载"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('库存概览'.encode('utf-8'), response.data)
    
    def test_products_page(self):
        """测试产品页面"""
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn('产品管理'.encode('utf-8'), response.data)
    
    def test_add_category(self):
        """测试添加分类"""
        with app.app_context():
            category = Category(name="测试分类", description="这是一个测试分类")
            db.session.add(category)
            db.session.commit()
            
            saved_category = Category.query.filter_by(name="测试分类").first()
            self.assertIsNotNone(saved_category)
            self.assertEqual(saved_category.description, "这是一个测试分类")
    
    def test_add_supplier(self):
        """测试添加供应商"""
        with app.app_context():
            supplier = Supplier(
                name="测试供应商",
                contact_person="张三",
                phone="138-0000-0000",
                email="test@example.com"
            )
            db.session.add(supplier)
            db.session.commit()
            
            saved_supplier = Supplier.query.filter_by(name="测试供应商").first()
            self.assertIsNotNone(saved_supplier)
            self.assertEqual(saved_supplier.contact_person, "张三")
    
    def test_add_product(self):
        """测试添加产品"""
        with app.app_context():
            product = Product(
                name="测试产品",
                description="这是一个测试产品",
                price=100.0,
                quantity=50,
                low_stock_threshold=10
            )
            db.session.add(product)
            db.session.commit()
            
            saved_product = Product.query.filter_by(name="测试产品").first()
            self.assertIsNotNone(saved_product)
            self.assertEqual(saved_product.price, 100.0)
            self.assertEqual(saved_product.quantity, 50)
    
    def test_product_properties(self):
        """测试产品属性计算"""
        with app.app_context():
            product = Product(
                name="测试产品",
                price=50.0,
                quantity=20,
                low_stock_threshold=25
            )
            
            # 测试总价值计算
            self.assertEqual(product.total_value, 1000.0)
            
            # 测试低库存检查
            self.assertTrue(product.is_low_stock)
            
            # 修改数量，再次测试
            product.quantity = 30
            self.assertFalse(product.is_low_stock)
    
    def test_stock_transaction(self):
        """测试库存事务"""
        with app.app_context():
            # 创建产品
            product = Product(
                name="库存测试产品",
                price=10.0,
                quantity=100
            )
            db.session.add(product)
            db.session.commit()
            
            # 创建入库事务
            transaction_in = StockTransaction(
                product_id=product.id,
                transaction_type='in',
                quantity=50,
                notes='入库测试'
            )
            db.session.add(transaction_in)
            
            # 创建出库事务
            transaction_out = StockTransaction(
                product_id=product.id,
                transaction_type='out',
                quantity=20,
                notes='出库测试'
            )
            db.session.add(transaction_out)
            db.session.commit()
            
            # 验证事务记录
            transactions = StockTransaction.query.filter_by(product_id=product.id).all()
            self.assertEqual(len(transactions), 2)
            
            in_transaction = next(t for t in transactions if t.transaction_type == 'in')
            out_transaction = next(t for t in transactions if t.transaction_type == 'out')
            
            self.assertEqual(in_transaction.quantity, 50)
            self.assertEqual(out_transaction.quantity, 20)
    
    def test_add_product_form(self):
        """测试添加产品表单提交"""
        response = self.app.post('/products/add', data={
            'name': '表单测试产品',
            'description': '通过表单添加的产品',
            'price': '99.99',
            'quantity': '10',
            'low_stock_threshold': '5'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('产品添加成功'.encode('utf-8'), response.data)
        
        # 验证产品已保存到数据库
        with app.app_context():
            product = Product.query.filter_by(name='表单测试产品').first()
            self.assertIsNotNone(product)
            self.assertEqual(float(product.price), 99.99)

def run_tests():
    """运行所有测试"""
    unittest.main()

if __name__ == '__main__':
    run_tests()