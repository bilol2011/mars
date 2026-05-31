# BILOL - Online Course Marketplace + Fintech Platform

A complete, production-ready education + fintech marketplace platform built with Django. BILOL includes an online course marketplace, wallet system, payment processing, LMS (Learning Management System), AI recommendations, gamification, and comprehensive admin analytics.

## Features

### Core Systems

#### 1. Course Marketplace
- Course listing with search and filters
- Course detail pages with syllabus and mentor info
- Categories and level-based filtering
- Instructor/mentor system
- Reviews & ratings system
- Wishlist functionality

#### 2. Wallet + Payment System
- User wallet with balance management
- Fake top-up system for testing
- Transaction history
- Purchase logic with balance validation
- Payment status tracking
- Click/Payme ready integration

#### 3. LMS Learning System
- Course progress tracking (0% → 100%)
- Lesson system with video support
- Mark lessons as completed
- Progress bar visualization
- Continue learning button
- Lesson completion with points awarding

#### 4. AI Recommendation System
- Smart course recommendations based on:
  - User history
  - Category interest
  - Trending courses
  - Popularity
- "Recommended for you" section
- Personalized learning paths

#### 5. Gamification System
- User levels: Bronze / Silver / Gold / Platinum / Diamond
- Points system:
  - +10 points per lesson
  - +50 per course completion
- Badges:
  - First Course
  - Fast Learner
  - Course Expert
  - Streak Champion
  - Level achievements
- XP and streak tracking

#### 6. Admin + Analytics Dashboard
- Total users and active users
- Total revenue and sales
- Top courses ranking
- Daily sales chart
- Wallet balances summary
- Course-specific analytics
- Payment history tracking

### Additional Features
- **User Authentication**: Registration, login, logout, profile management
- **Payment System**: Support for Click/Payme integration with installment plans (3, 6, 12, 18 months)
- **User Dashboard**: Track enrolled courses, progress, certificates, and payment history
- **Reviews System**: Star ratings and comments for courses
- **Notifications**: In-app notifications for users
- **Certificates**: Generate certificates upon course completion

### Design
- Modern, premium UI with Tailwind CSS
- Responsive mobile design
- White and blue theme with soft shadows
- Smooth hover effects and transitions
- Professional card-based layouts

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: Django Templates + Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django built-in auth system
- **Admin Panel**: Django Admin
- **Payment Integration**: Click/Payme ready

## Project Structure

```
bilol_project/
├── manage.py
├── bilol_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── accounts/          # User authentication and profiles
│   ├── courses/           # Course management
│   ├── payments/          # Payment processing
│   ├── dashboard/         # User dashboard
│   └── reviews/           # Reviews system
├── templates/
│   ├── base.html          # Base template with Tailwind CSS
│   ├── home.html          # Home page
│   ├── accounts/          # Account templates
│   ├── courses/           # Course templates
│   ├── payments/          # Payment templates
│   ├── dashboard/         # Dashboard templates
│   └── reviews/           # Review templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
└── requirements.txt       # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd bilol_project
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser for admin panel**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Frontend: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Database Models

### Accounts
- **User**: Custom user model with email authentication, roles (student, mentor, admin)
- **Wallet**: User wallet for balance management
- **Transaction**: Transaction history for wallet operations
- **UserLevel**: Gamification user level (Bronze/Silver/Gold/Platinum/Diamond)
- **Badge**: Achievement badges
- **UserBadge**: User earned badges

### Courses
- **Category**: Course categories
- **Course**: Course information with pricing, duration, level
- **Lesson**: Individual lessons within courses
- **Enrollment**: User course enrollments with progress tracking
- **LessonProgress**: LMS lesson progress tracking

### Payments
- **PaymentPlan**: Installment payment plans (3, 6, 12, 18 months)
- **Payment**: Payment records with status tracking
- **InstallmentPayment**: Individual installment payments

### Dashboard
- **Wishlist**: User saved courses
- **Certificate**: Course completion certificates
- **Notification**: User notifications
- **CourseRecommendation**: AI-based course recommendations
- **DailyAnalytics**: Daily analytics for admin dashboard
- **CourseAnalytics**: Per-course analytics

### Reviews
- **Review**: Course reviews with ratings
- **MentorReview**: Mentor-specific reviews

## Management Commands

The project includes custom management commands for seeding data:

### Seed Sample Courses
```bash
python manage.py add_sample_courses
```
This command creates:
- Sample mentor user
- Course categories
- 10 sample courses with lessons

### Seed Badges
```bash
python manage.py seed_badges
```
This command creates gamification badges:
- First Course, Fast Learner, Course Expert
- Streak Champion
- Level achievements (Bronze through Diamond)
- Category-specific badges

### Seed Analytics
```bash
python manage.py seed_analytics
```
This command creates:
- Daily analytics for the last 30 days
- Course-specific analytics data

## Admin Panel Features

The Django Admin panel provides full control over:
- User management (students, mentors, admins)
- Course management (add, edit, delete courses)
- Category management
- Payment tracking and management
- Review moderation
- Notification management

## Payment Integration

The project is ready for Click and Payme payment integration. To enable:
1. Update the payment views with actual API integration
2. Configure payment credentials in settings.py
3. Set up webhooks for payment status updates

## Deployment

### Production Checklist
1. Set `DEBUG = False` in settings.py
2. Configure allowed hosts
3. Use PostgreSQL instead of SQLite
4. Set up static files serving
5. Configure media files storage (e.g., AWS S3)
6. Set up SSL/HTTPS
7. Configure email backend for notifications
8. Set up environment variables for sensitive data

### Recommended Hosting
- Heroku
- DigitalOcean
- AWS
- Railway

## Customization

### Adding New Features
1. Create new apps following the existing structure
2. Add models, views, and templates
3. Update URLs in main urls.py
4. Register models in admin.py

### Styling
- Tailwind CSS is loaded via CDN for simplicity
- Custom styles can be added in the base template
- All templates use a consistent design system

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is proprietary software. All rights reserved.

## Support

For support and questions:
- Email: info@bilol.uz
- Phone: +998 90 123 45 67
- Address: Tashkent, Uzbekistan

## Roadmap

### Completed Features ✅
- Course marketplace with search and filters
- Wallet system with balance management
- Payment processing with installment plans
- LMS with lesson progress tracking
- AI recommendation system
- Gamification system (levels, points, badges)
- Admin analytics dashboard
- Certificate generation
- Reviews and ratings system

### Future Enhancements
- Mobile app (React Native)
- Advanced analytics for mentors
- Live streaming for courses
- Discussion forums
- Mobile payment integration
- Multi-language support
- Advanced search with filters
#   m a r s  
 #   b i l o l _ c u r s  
 #   b i l o l _ c u r s  
 #   b i l o l _ c u r s  
 #   b i l o l _ c u r s  
 #   b i l o l _ c u r s  
 # bilol_curs
# online
