# 💰 ExpenseTracker - Full Stack Web Application

A modern, full-featured expense tracking application built with Django, HTML, CSS, JavaScript, and SQLite. Track your income and expenses in real-time, set budgets, receive alerts, and generate detailed reports with beautiful visualizations.

## 🌟 Features

### Core Features
- **💵 Income & Expense Tracking**: Log transactions with categories, amounts, dates, and descriptions
- **📊 Real-time Budget Management**: Set budgets by category (monthly/yearly) with customizable alerts
- **🔔 Smart Alerts**: Get notifications when approaching or exceeding budget limits
- **📈 Beautiful Reports**: View spending patterns with interactive pie charts and charts
- **📥 PDF Download**: Export your financial reports as PDF documents
- **🏷️ Custom Categories**: Create and manage expense/income categories with emojis and colors
- **💡 Money-Saving Quotes**: Daily motivational quotes to inspire financial discipline

### Security & User Management
- **🔐 Secure Authentication**: Unique username and password-based login
- **👤 User Profiles**: Personalized profiles with profile pictures and bio
- **🔑 Password Management**: Change password functionality with security validation
- **📝 Transaction History**: Complete history with filtering and pagination

### Modern UI/UX
- **✨ Smooth Animations**: Engaging page transitions and interactions
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **🎨 Modern Aesthetics**: Beautiful gradient backgrounds, cards, and color schemes
- **⚡ Fast Performance**: Optimized loading and smooth interactions
- **📊 Visual Analytics**: Pie charts, progress bars, and data visualizations

### Advanced Features
- **🎯 Category-wise Budget Tracking**: Set different budgets for each category
- **💳 Payment Methods**: Track different payment methods (Cash, Card, Digital, etc.)
- **📸 Receipt Upload**: Attach receipt images to your expenses
- **🔍 Advanced Filtering**: Filter transactions by date, category, type, and amount
- **📊 Expense Distribution**: View expense breakdown by category
- **💰 Balance Calculation**: Automatic income-expense balance tracking

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or Extract the Project**
```bash
cd django
```

2. **Activate Virtual Environment**
```bash
# On Windows
env\Scripts\activate

# On macOS/Linux
source env/bin/activate
```

3. **Install Dependencies**
```bash
pip install Django Pillow reportlab
```

4. **Database Setup**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Populate default quotes
python manage.py populate_quotes
```

5. **Create Superuser (Admin)**
```bash
python manage.py createsuperuser
# Or use default: username: admin, password: admin123
```

6. **Run Development Server**
```bash
python manage.py runserver
```

7. **Access the Application**
- Landing Page: http://localhost:8000
- Dashboard: http://localhost:8000 (after login)
- Admin Panel: http://localhost:8000/admin

## 📖 Usage Guide

### 1. Registration & Login
- Visit the landing page
- Click "Get Started" or "Sign Up"
- Create account with unique username, email, and password
- Login with your credentials

### 2. Dashboard
- View income/expense summary
- See expense breakdown by category
- Access quick action buttons
- View recent transactions
- Read money-saving quotes

### 3. Adding Transactions
- **Income**: Click "Add Income" → Select category → Enter amount → Add date & description
- **Expense**: Click "Add Expense" → Select category → Enter amount → Choose payment method → Optional receipt image

### 4. Budget Management
- Navigate to "Budgets" section
- Click "Set New Budget"
- Select category and amount
- Set frequency (Monthly/Yearly)
- Adjust alert threshold (default 80%)
- Budget alerts appear when thresholds are exceeded

### 5. Viewing Reports
- Go to "Reports" section
- Choose time range (This Month, Quarter, Year, Last 30 Days)
- View interactive pie charts
- See expense/income distribution
- Download detailed PDF report

### 6. Transaction Management
- View all transactions with filters
- Edit or delete transactions
- Filter by type, category, date range
- Pagination support for large datasets

### 7. Alerts & Notifications
- Budget alerts appear when limits are approached/exceeded
- Mark alerts as read
- View alert history
- Different colored icons for warning/critical status

### 8. Profile Management
- Upload profile picture
- Add phone number and bio
- Change password with current password verification
- Manage notification settings

## 📁 Project Structure

```
django/
├── expensetracker/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # User authentication app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── tracker/                 # Main tracker app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── utils.py
│   └── management/
│       └── commands/
│           └── populate_quotes.py
├── templates/               # HTML templates
│   ├── base.html
│   ├── landing.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── transactions.html
│   ├── budgets.html
│   ├── reports.html
│   ├── alerts.html
│   ├── profile.html
│   └── category_management.html
├── static/                  # Static files
│   ├── css/
│   │   └── style.css       # Main stylesheet with animations
│   ├── js/
│   │   └── script.js       # JavaScript functionality
│   └── images/
├── media/                   # User uploads
│   ├── profile_pics/
│   └── receipts/
└── db.sqlite3              # SQLite database
```

## 🗄️ Database Models

### UserProfile
- Links to Django User
- Phone number, profile picture, bio
- Creation and update timestamps

### Category
- Name, type (income/expense)
- Emoji, color code
- User-specific categories

### Income
- User, category, amount
- Description, date
- Automatic timestamp tracking

### Expense
- User, category, amount
- Description, payment method
- Optional receipt image
- Date and timestamp

### Budget
- User, category, amount
- Frequency (monthly/yearly)
- Alert threshold (default 80%)
- Unique constraint per user/category/month/year

### BudgetAlert
- User, budget reference
- Status (warning/critical)
- Spent amount, message
- Read/unread status

### MoneySavingQuote
- Quote text, author
- Emoji for visual appeal
- Random ordering for variety

## 🎨 UI/UX Highlights

### Colors & Branding
- Primary: #667eea (Purple Blue)
- Success: #27ae60 (Green)
- Danger: #e74c3c (Red)
- Warning: #f39c12 (Orange)
- Info: #3498db (Blue)

### Animations
- Slide up/down transitions
- Fade in effects
- Smooth transforms
- Progress bar animations
- Hover effects

### Responsive Breakpoints
- Desktop: Full width features
- Tablet: Grid adjustments (768px and below)
- Mobile: Stacked layout, touch-friendly buttons (480px and below)

## 🔒 Security Features

- Password hashing with Django's built-in system
- CSRF protection on all forms
- SQL injection prevention with ORM
- XSS protection with template auto-escaping
- Secure session management
- User authentication required for sensitive operations
- Unique username validation
- Password strength requirements (8+ characters)

## 📊 Advanced Features Explained

### Real-time Budget Tracking
- Automatically calculates spent amount vs. budget
- Shows percentage of budget used
- Color-coded status (green/yellow/red)
- Manual alert threshold customization

### Smart Alert System
- Triggered when hitting 80% (configurable)
- Critical alert at 100% budget exceeded
- Alert history with timestamps
- Mark read/unread functionality

### PDF Report Generation
- Uses ReportLab library
- Includes summary and detailed tables
- Styled report with colors
- Customizable date ranges
- Multiple download options

### Category Management
- Create custom income/expense categories
- Assign emojis for quick identification
- Pick colors for visual distinction
- Delete unused categories
- User-specific categories

## 🎯 Unique Features

1. **Interactive Pie Charts**: Beautiful Chart.js powered visualizations
2. **Real-time Balance**: Automatic calculation of income vs. expense
3. **Dynamic Quotes**: Rotating money-saving quotes for daily motivation
4. **Payment Methods**: Track expenses by payment type
5. **Receipt Upload**: Store evidence of expenses
6. **Advanced Filtering**: Filter by date, category, amount, and type
7. **Pagination**: Handle large datasets efficiently
8. **Responsive Charts**: Works on all device sizes
9. **Smooth Transitions**: Professional animations throughout
10. **Category Emojis**: Fun, visual category identification

## 🛠️ Customization

### Adding New Categories
- Login and go to "Categories" section
- Add category with name, type, emoji, and color
- Use in transactions immediately

### Modifying Budget Thresholds
- Edit budget and change alert percentage
- Receive alerts based on new threshold

### Changing Colors
- Edit `static/css/style.css`
- Modify CSS variables in `:root`
- Customize button, card, and text colors

## 📝 API Endpoints

### Authentication
- `GET/POST /accounts/register/` - User registration
- `GET/POST /accounts/login/` - User login
- `GET /accounts/logout/` - User logout
- `GET /accounts/profile/` - View/Edit profile
- `POST /accounts/change-password/` - Change password

### Transactions
- `GET/POST /add-income/` - Add income
- `GET/POST /add-expense/` - Add expense
- `GET /transactions/` - View all transactions
- `GET/POST /edit-income/<id>/` - Edit income
- `GET /delete-income/<id>/` - Delete income
- `GET/POST /edit-expense/<id>/` - Edit expense
- `GET /delete-expense/<id>/` - Delete expense

### Analytics
- `GET /budgets/` - View/create budgets
- `GET /reports/` - View reports
- `GET /download-pdf/` - Download PDF report
- `GET /alerts/` - View budget alerts

### Management
- `GET /categories/` - Manage categories
- `GET /` - Dashboard
- `GET /landing/` - Landing page

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Issues
```bash
# Fresh database
rm db.sqlite3
python manage.py migrate
python manage.py populate_quotes
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Module Not Found Errors
```bash
pip install -r requirements.txt
```

## 📊 Performance Optimization

- SQLite database for lightweight deployment
- Pagination for transaction lists
- Lazy loading of images
- CSS and JS minification ready
- Database indexing on frequently queried fields
- Caching-friendly template structure

## 🤝 Contributing

To contribute improvements:
1. Make changes to the code
2. Test thoroughly
3. Update documentation
4. Submit for review

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check Django documentation

## 🎉 Special Features

- **16 Money-Saving Quotes**: Preloaded motivational content
- **Staggered Animations**: Professional, performance-optimized animations
- **Touch-Friendly UI**: Minimum 44px touch targets on mobile
- **Dark Mode Ready**: CSS structure supports easy theme switching
- **Accessibility**: Semantic HTML and proper ARIA labels
- **Performance**: Optimized database queries and minimal reflows

## 🌐 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📈 Future Enhancements

- Two-factor authentication
- Email notifications
- Data export (CSV, Excel)
- Recurring transactions
- Investment tracking
- Tax categorization
- Multi-currency support
- API for mobile apps
- Dark mode toggle
- Advanced filtering UI

---

**ExpenseTracker** - Take control of your finances, one transaction at a time! 💰✨
