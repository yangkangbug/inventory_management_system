# 库存管理系统 (Inventory Management System)

一个基于 Flask 的现代化库存管理系统，支持产品管理、库存追踪、供应商管理等功能。

## 🚀 功能特性

### 核心功能
- **产品管理**: 完整的产品CRUD操作，支持分类和供应商关联
- **库存追踪**: 实时库存监控，支持入库/出库操作记录
- **低库存警告**: 自动检测并提醒库存不足的产品
- **分类管理**: 产品分类组织和管理
- **供应商管理**: 供应商信息维护和产品关联
- **库存报告**: 库存状态分析和历史记录查看

### 技术特性
- **响应式界面**: 基于 Bootstrap 5 的现代化 UI
- **数据库支持**: SQLite 数据库，易于部署和备份
- **RESTful API**: 提供 JSON API 接口
- **中文界面**: 完全中文化的用户界面

## 📋 系统要求

- Python 3.8+
- Flask 2.3.3
- SQLAlchemy 2.0+
- 现代浏览器 (Chrome, Firefox, Safari, Edge)

## 🛠️ 安装部署

### 1. 克隆项目
```bash
git clone https://github.com/yangkangbug/inventory_management_system.git
cd inventory_management_system
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行应用
```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

### 4. 加载示例数据 (可选)
```bash
python sample_data.py
```

## 📖 使用指南

### 首次使用
1. 启动应用后，访问 `http://localhost:5000`
2. 系统会自动创建数据库表
3. 建议先添加分类和供应商，再添加产品

### 主要操作流程

#### 产品管理
1. **添加产品**: 导航到 "产品管理" → "添加新产品"
2. **编辑产品**: 在产品列表中点击编辑按钮
3. **删除产品**: 在产品列表中点击删除按钮 (需确认)

#### 库存操作
1. **库存调整**: 在产品列表中点击库存调整按钮
2. **入库操作**: 选择 "入库" 类型，输入数量和备注
3. **出库操作**: 选择 "出库" 类型，输入数量和备注

#### 分类和供应商
1. **添加分类**: 导航到 "分类管理" → "添加新分类"
2. **添加供应商**: 导航到 "供应商管理" → "添加新供应商"

### 库存监控
- **低库存警告**: 当产品数量低于设定阈值时，系统会自动标记
- **库存报告**: 查看低库存产品和最近的库存变动记录

## 📊 API 接口

系统提供以下 JSON API 接口:

### 获取所有产品
```http
GET /api/products
```

### 获取低库存产品
```http
GET /api/low-stock
```

返回示例:
```json
[
  {
    "id": 1,
    "name": "iPhone 15",
    "quantity": 25,
    "price": 5999.0,
    "category": "电子产品",
    "supplier": "科技供应商有限公司"
  }
]
```

## 🧪 测试

运行测试套件:
```bash
python test_inventory.py
```

测试覆盖:
- 页面加载测试
- 数据库模型测试
- 产品属性计算测试
- 库存事务测试
- 表单提交测试

## 📁 项目结构

```
inventory_management_system/
├── app.py                 # 主应用文件
├── models.py             # 数据库模型 (已整合到 app.py)
├── sample_data.py        # 示例数据生成
├── test_inventory.py     # 测试文件
├── requirements.txt      # 依赖列表
├── templates/            # HTML 模板
│   ├── base.html        # 基础模板
│   ├── index.html       # 首页
│   ├── products.html    # 产品列表
│   ├── add_product.html # 添加产品
│   ├── edit_product.html# 编辑产品
│   ├── adjust_stock.html# 库存调整
│   ├── categories.html  # 分类管理
│   ├── add_category.html# 添加分类
│   ├── suppliers.html   # 供应商管理
│   ├── add_supplier.html# 添加供应商
│   └── reports.html     # 报告页面
├── static/              # 静态文件目录
│   ├── css/            # 样式文件
│   └── js/             # JavaScript 文件
└── inventory.db         # SQLite 数据库文件 (运行后生成)
```

## 🗃️ 数据库结构

### 产品表 (products)
- `id`: 主键
- `name`: 产品名称
- `description`: 产品描述
- `price`: 价格
- `quantity`: 库存数量
- `low_stock_threshold`: 低库存阈值
- `category_id`: 分类ID (外键)
- `supplier_id`: 供应商ID (外键)
- `created_at`: 创建时间
- `updated_at`: 更新时间

### 分类表 (categories)
- `id`: 主键
- `name`: 分类名称
- `description`: 分类描述
- `created_at`: 创建时间

### 供应商表 (suppliers)
- `id`: 主键
- `name`: 供应商名称
- `contact_person`: 联系人
- `phone`: 电话
- `email`: 邮箱
- `address`: 地址
- `created_at`: 创建时间

### 库存事务表 (stock_transactions)
- `id`: 主键
- `product_id`: 产品ID (外键)
- `transaction_type`: 事务类型 ('in'/'out')
- `quantity`: 数量
- `notes`: 备注
- `created_at`: 创建时间

## 🚀 部署说明

### 开发环境
```bash
python app.py
```
应用将以调试模式运行在 `http://localhost:5000`

### 生产环境
推荐使用 WSGI 服务器如 Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### 环境变量配置 (可选)
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export DATABASE_URL=sqlite:///production.db
```

## 🔧 自定义配置

在 `app.py` 中可以修改以下配置:
- `SECRET_KEY`: 应用密钥
- `SQLALCHEMY_DATABASE_URI`: 数据库连接字符串
- 服务器地址和端口

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙋‍♂️ 常见问题

### Q: 如何重置数据库？
A: 删除 `inventory.db` 文件，重新运行应用即可。

### Q: 如何修改低库存阈值？
A: 在编辑产品页面可以修改每个产品的低库存阈值。

### Q: 支持哪些数据库？
A: 默认使用 SQLite，但可以通过修改 `SQLALCHEMY_DATABASE_URI` 支持 PostgreSQL、MySQL 等。

### Q: 如何备份数据？
A: 直接复制 `inventory.db` 文件即可备份所有数据。

## 📞 支持

如有问题或建议，请通过以下方式联系:
- 提交 GitHub Issue
- 发送邮件至项目维护者

---

**库存管理系统** - 让库存管理变得简单高效! 🎯