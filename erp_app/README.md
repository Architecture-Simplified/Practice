# ZOHO-like ERP Application

A comprehensive Enterprise Resource Planning (ERP) application built with Python, featuring modules for CRM, Inventory Management, Accounting, HR, and Sales - similar to ZOHO.

## Features

### 🏢 Core Modules
- **CRM (Customer Relationship Management)**: Lead management, contact management, deal tracking
- **Inventory Management**: Product catalog, stock tracking, warehouse management
- **Accounting**: Invoicing, expense tracking, financial reporting
- **Human Resources**: Employee management, attendance tracking, payroll
- **Sales**: Order management, quotations, sales analytics

### 🛠️ Technical Features
- Modern REST API with FastAPI
- SQLAlchemy ORM with PostgreSQL/SQLite support
- JWT-based authentication
- Role-based access control
- Real-time dashboard
- Responsive web interface
- File upload and management
- Email notifications
- Export to PDF/Excel
- Multi-tenant architecture

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+ (for frontend build tools)
- PostgreSQL (optional, SQLite works too)

### Installation

1. **Clone and setup backend**:
   ```bash
   cd erp_app
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

2. **Setup database**:
   ```bash
   python backend/app/core/init_db.py
   ```

3. **Run the application**:
   ```bash
   python backend/main.py
   ```

4. **Access the application**:
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Admin Panel: http://localhost:8000/admin

### Default Login
- Email: admin@erp.com
- Password: admin123

## Architecture

```
erp_app/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── core/           # Core functionality
│   │   ├── modules/        # Business modules
│   │   │   ├── crm/        # Customer management
│   │   │   ├── inventory/  # Stock management
│   │   │   ├── accounting/ # Financial management
│   │   │   ├── hr/         # Human resources
│   │   │   └── sales/      # Sales management
│   │   └── api/            # API endpoints
│   └── main.py             # Application entry point
├── frontend/               # Web Interface
│   ├── static/            # CSS, JS, Images
│   └── templates/         # HTML templates
├── database/              # Database files
├── config/                # Configuration
└── tests/                 # Test suite
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Refresh token

### CRM Module
- `GET /api/crm/leads` - List leads
- `POST /api/crm/leads` - Create lead
- `GET /api/crm/contacts` - List contacts
- `POST /api/crm/contacts` - Create contact

### Inventory Module
- `GET /api/inventory/products` - List products
- `POST /api/inventory/products` - Create product
- `GET /api/inventory/stock` - Check stock levels

### Accounting Module
- `GET /api/accounting/invoices` - List invoices
- `POST /api/accounting/invoices` - Create invoice
- `GET /api/accounting/expenses` - List expenses

### HR Module
- `GET /api/hr/employees` - List employees
- `POST /api/hr/employees` - Create employee
- `GET /api/hr/attendance` - Attendance records

### Sales Module
- `GET /api/sales/orders` - List orders
- `POST /api/sales/orders` - Create order
- `GET /api/sales/quotes` - List quotations

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black backend/
```

### Database Migrations
```bash
alembic upgrade head
```

## Deployment

### Docker
```bash
docker-compose up -d
```

### Production Setup
1. Set environment variables
2. Configure PostgreSQL
3. Setup SSL certificates
4. Configure reverse proxy (Nginx)

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Email: support@erp-app.com
