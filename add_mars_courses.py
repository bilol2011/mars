import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilol_project.settings')
django.setup()

from apps.courses.models import Course, Lesson, Category, EducationalCenter
from apps.accounts.models import User
from decimal import Decimal

# Get MARS IT School
mars_it = EducationalCenter.objects.get(slug='mars-it-school')

# Get or create categories
category, _ = Category.objects.get_or_create(
    slug='dasturlash',
    defaults={
        'name': 'Dasturlash',
        'description': 'Dasturlash va IT kurslari',
        'icon': 'fas fa-code'
    }
)

# Get mentor user
mentor = User.objects.filter(role='mentor').first()
if not mentor:
    print("Mentor topilmadi! Mentor yaratmoqda...")
    mentor = User.objects.create_user(
        email='marsit@bilol.uz',
        username='marsit',
        password='marsit123',
        first_name='MARS IT',
        last_name='School',
        role='mentor'
    )
    print(f"Mentor yaratildi: {mentor.email}")

# Courses data
courses_data = [
    {
        'title': 'Front-End Dasturlash Asoslari',
        'slug': 'mars-frontend-asoslari',
        'description': '''Front-End dasturlash asoslarini o'rganing. HTML, CSS va JavaScript orqali 
zamonaviy veb-saytlar yaratishni o'rganasiz. Bu kurs 9-17 yoshdagi bolalar uchun mo'ljallangan 
va amaliy mashg'ulotlarga asoslangan.''',
        'short_description': 'HTML, CSS va JavaScript orqali veb-saytlar yaratishni o\'rganing',
        'price': Decimal('1500000'),
        'discount_price': Decimal('1200000'),
        'duration': '3 oy',
        'total_hours': 48,
        'level': 'beginner',
        'language': 'O\'zbek',
        'category': category,
        'mentor': mentor,
        'lessons': [
            ('HTML Kirish', 'HTML tuzilishi va asosiy teglar', 45),
            ('CSS Asoslari', 'CSS orqali stil berish', 60),
            ('CSS Flexbox', 'Flexbox layout tizimi', 60),
            ('CSS Grid', 'Grid layout tizimi', 60),
            ('JavaScript Kirish', 'JavaScript asoslari', 60),
            ('O\'zgaruvchilar va Turlar', 'JavaScript o\'zgaruvchilar', 45),
            ('Funksiyalar', 'JavaScript funksiyalar', 60),
            ('DOM Manipulyatsiya', 'DOM bilan ishlash', 60),
        ]
    },
    {
        'title': 'Back-End Dasturlash',
        'slug': 'mars-backend',
        'description': '''Back-End dasturlashni o'rganing. Python orqali server tomon dasturlash, 
ma'lumotlar bazasi bilan ishlash va API yaratishni o'rganasiz.''',
        'short_description': 'Python orqali server tomon dasturlashni o\'rganing',
        'price': Decimal('1800000'),
        'discount_price': Decimal('1500000'),
        'duration': '4 oy',
        'total_hours': 64,
        'level': 'intermediate',
        'language': 'O\'zbek',
        'category': category,
        'mentor': mentor,
        'lessons': [
            ('Python Kirish', 'Python dasturlash tili asoslari', 60),
            ('O\'zgaruvchilar va Turlar', 'Python ma\'lumot turlari', 45),
            ('Funksiyalar', 'Python funksiyalar', 60),
            ('Obyektga yo\'naltirilgan dasturlash', 'OOP asoslari', 90),
            ('Django Framework', 'Django orqali veb-app yaratish', 90),
            ('Ma\'lumotlar Bazasi', 'SQL va PostgreSQL', 60),
            ('API Yaratish', 'REST API yaratish', 60),
            ('Loyiha', 'Final loyiha', 120),
        ]
    },
    {
        'title': 'Bolalar uchun Dasturlash (9-12 yosh)',
        'slug': 'mars-kids-programming',
        'description': '''9-12 yoshdagi bolalar uchun dasturlash asoslari. Scratch va blokli dasturlash 
orqali mantiqiy fikrlashni o'rganish. O'yinlar va animatsiyalar yaratish.''',
        'short_description': '9-12 yoshdagi bolalar uchun dasturlash asoslari',
        'price': Decimal('1000000'),
        'discount_price': Decimal('800000'),
        'duration': '2 oy',
        'total_hours': 32,
        'level': 'beginner',
        'language': 'O\'zbek',
        'category': category,
        'mentor': mentor,
        'lessons': [
            ('Scratch Kirish', 'Scratch dasturlash muhiti', 45),
            ('Harakatlar', 'Sprite harakatlari', 45),
            ('O\'zgaruvchilar', 'Scratch o\'zgaruvchilar', 45),
            ('Shartlar', 'If-else shartlari', 45),
            ('Sikllar', 'Looplar', 45),
            ('O\'yin Yaratish', 'Simple o\'yin', 60),
            ('Animatsiya', 'Animatsiya yaratish', 60),
            ('Final Loyiha', 'O\'z loyihasi', 60),
        ]
    },
    {
        'title': 'O\'smirlar uchun Dasturlash (13-17 yosh)',
        'slug': 'mars-teens-programming',
        'description': '''13-17 yoshdagi o'smirlar uchun Python dasturlash. Haqiqiy loyihalar yaratish, 
ma'lumotlar tahlili va o'yin dasturlash asoslari.''',
        'short_description': '13-17 yoshdagi o\'smirlar uchun Python dasturlash',
        'price': Decimal('1500000'),
        'discount_price': Decimal('1200000'),
        'duration': '3 oy',
        'total_hours': 48,
        'level': 'beginner',
        'language': 'O\'zbek',
        'category': category,
        'mentor': mentor,
        'lessons': [
            ('Python Kirish', 'Python asoslari', 60),
            ('O\'zgaruvchilar', 'Python o\'zgaruvchilar', 45),
            ('Funksiyalar', 'Python funksiyalar', 60),
            ('List va Tuple', 'Python ma\'lumot tuzilmalari', 60),
            ('Looplar', 'For va while looplar', 45),
            ('O\'yin Dasturlash', 'Pygame asoslari', 90),
            ('Ma\'lumotlar Tahlili', 'Pandas asoslari', 60),
            ('Loyiha', 'Final loyiha', 90),
        ]
    },
    {
        'title': 'Sun\'iy Intellekt (AI) Asoslari',
        'slug': 'mars-ai-basics',
        'description': '''Sun'iy intellekt asoslarini o'rganing. Machine learning, neural networks va 
amaliy AI loyihalar yaratish.''',
        'short_description': 'AI va Machine Learning asoslari',
        'price': Decimal('2000000'),
        'discount_price': Decimal('1700000'),
        'duration': '4 oy',
        'total_hours': 64,
        'level': 'intermediate',
        'language': 'O\'zbek',
        'category': category,
        'mentor': mentor,
        'lessons': [
            ('AI Kirish', 'Sun\'iy intellekt tarixi va turlari', 60),
            ('Python for AI', 'AI uchun Python kutubxonalari', 60),
            ('Ma\'lumotlar Tahlili', 'NumPy va Pandas', 90),
            ('Machine Learning Kirish', 'ML asoslari', 90),
            ('Scikit-learn', 'Scikit-learn kutubxonasi', 90),
            ('Neural Networks', 'Neural networks asoslari', 90),
            ('Deep Learning', 'Deep learning asoslari', 90),
            ('Loyiha', 'AI loyiha', 120),
        ]
    },
]

# Create courses
for course_data in courses_data:
    lessons_data = course_data.pop('lessons')
    
    course, created = Course.objects.get_or_create(
        slug=course_data['slug'],
        defaults=course_data
    )
    
    if created:
        print(f"Kurs qo'shildi: {course.title}")
        
        # Add lessons
        for i, (title, description, duration) in enumerate(lessons_data, 1):
            Lesson.objects.create(
                course=course,
                title=title,
                description=description,
                duration=duration,
                order=i,
                video_url=f'https://www.youtube.com/watch?v=example{i}'
            )
        print(f"  - {len(lessons_data)} ta dars qo'shildi")
    else:
        print(f"Kurs allaqachon mavjud: {course.title}")

print(f"\nMARS IT School uchun jami {len(courses_data)} ta kurs qo'shildi!")
