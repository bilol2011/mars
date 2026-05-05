from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Category, Lesson
from apps.accounts.models import Wallet

User = get_user_model()


class Command(BaseCommand):
    help = 'Add sample courses with lessons'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding sample courses...')
        
        # Get or create mentor user
        mentor, created = User.objects.get_or_create(
            email='mentor@bilol.uz',
            defaults={
                'username': 'mentor',
                'first_name': 'Akmal',
                'last_name': 'Karimov',
                'role': 'mentor',
                'is_staff': True,
            }
        )
        if created:
            mentor.set_password('password123')
            mentor.save()
            self.stdout.write(f'Created mentor: {mentor.email}')
        
        # Create categories
        categories_data = [
            {'name': 'Web Dasturlash', 'slug': 'web-dasturlash', 'description': 'HTML, CSS, JavaScript, React, Vue.js'},
            {'name': 'Python Dasturlash', 'slug': 'python-dasturlash', 'description': 'Python asoslari, Django, Flask, Data Science'},
            {'name': 'Mobile Dasturlash', 'slug': 'mobile-dasturlash', 'description': 'Flutter, React Native, Android, iOS'},
            {'name': 'Dizayn', 'slug': 'dizayn', 'description': 'UI/UX, Figma, Photoshop, Illustrator'},
            {'name': 'Marketing', 'slug': 'marketing', 'description': 'SMM, SEO, Google Ads, Facebook Ads'},
            {'name': 'Biznes', 'slug': 'biznes', 'description': 'Startup, Biznes rejalashtirish, Moliya'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Course data
        courses_data = [
            {
                'title': 'HTML va CSS asoslari',
                'slug': 'html-css-asoslari',
                'description': 'Web dasturlashning asoslarini o\'rganing. HTML5 va CSS3 bilan zamonaviy veb-saytlar yaratishni bilib oling.',
                'price': 150000,
                'discount_price': 99000,
                'category': 'web-dasturlash',
                'level': 'beginner',
                'duration': '10 soat',
                'language': 'O\'zbek',
                'is_featured': True,
                'lessons': [
                    {'title': 'HTML Kirish', 'description': 'HTML tili haqida umumiy ma\'lumot', 'duration': 45, 'order': 1, 'is_free': True},
                    {'title': 'HTML Elementlari', 'description': 'Asosiy HTML teglar va ularning foydalanilishi', 'duration': 60, 'order': 2, 'is_free': True},
                    {'title': 'CSS Kirish', 'description': 'CSS tili va selektorlar', 'duration': 50, 'order': 3, 'is_free': False},
                    {'title': 'CSS Box Model', 'description': 'Box model va layout', 'duration': 55, 'order': 4, 'is_free': False},
                    {'title': 'Flexbox', 'description': 'Flexbox layout tizimi', 'duration': 60, 'order': 5, 'is_free': False},
                    {'title': 'Grid Layout', 'description': 'CSS Grid layout', 'duration': 65, 'order': 6, 'is_free': False},
                    {'title': 'Responsive Dizayn', 'description': 'Moslashuvchan dizayn', 'duration': 70, 'order': 7, 'is_free': False},
                    {'title': 'CSS Animatsiyalar', 'description': 'CSS bilan animatsiyalar yaratish', 'duration': 55, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'JavaScript asoslari',
                'slug': 'javascript-asoslari',
                'description': 'JavaScript dasturlash tilini o\'rganing. Interaktiv veb-saytlar yaratishni bilib oling.',
                'price': 200000,
                'discount_price': 149000,
                'category': 'web-dasturlash',
                'level': 'beginner',
                'duration': '15 soat',
                'language': 'O\'zbek',
                'is_featured': True,
                'lessons': [
                    {'title': 'JavaScript Kirish', 'description': 'JS haqida umumiy ma\'lumot', 'duration': 45, 'order': 1, 'is_free': True},
                    {'title': 'O\'zgaruvchilar va Ma\'lumot Turlari', 'description': 'Variables and Data Types', 'duration': 50, 'order': 2, 'is_free': True},
                    {'title': 'Funksiyalar', 'description': 'Functions in JavaScript', 'duration': 60, 'order': 3, 'is_free': False},
                    {'title': 'Massivlar', 'description': 'Arrays and methods', 'duration': 55, 'order': 4, 'is_free': False},
                    {'title': 'Obyektlar', 'description': 'Objects in JavaScript', 'duration': 60, 'order': 5, 'is_free': False},
                    {'title': 'DOM Manipulyatsiya', 'description': 'Working with DOM', 'duration': 70, 'order': 6, 'is_free': False},
                    {'title': 'Eventlar', 'description': 'Event handling', 'duration': 55, 'order': 7, 'is_free': False},
                    {'title': 'Asynchronous JS', 'description': 'Promises and Async/Await', 'duration': 65, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'React.js to\'liq kurs',
                'slug': 'reactjs-toliq-kurs',
                'description': 'React.js frameworkini chuqur o\'rganing. Zamonaviy single-page applications yaratishni bilib oling.',
                'price': 350000,
                'discount_price': 249000,
                'category': 'web-dasturlash',
                'level': 'intermediate',
                'duration': '25 soat',
                'language': 'O\'zbek',
                'is_featured': True,
                'lessons': [
                    {'title': 'React Kirish', 'description': 'React nima va qanday ishlaydi', 'duration': 45, 'order': 1, 'is_free': True},
                    {'title': 'JSX', 'description': 'JSX sintaksisi', 'duration': 50, 'order': 2, 'is_free': True},
                    {'title': 'Components', 'description': 'React komponentlari', 'duration': 60, 'order': 3, 'is_free': False},
                    {'title': 'Props va State', 'description': 'Props and State management', 'duration': 65, 'order': 4, 'is_free': False},
                    {'title': 'Hooks', 'description': 'React Hooks: useState, useEffect', 'duration': 70, 'order': 5, 'is_free': False},
                    {'title': 'Routing', 'description': 'React Router', 'duration': 55, 'order': 6, 'is_free': False},
                    {'title': 'State Management', 'description': 'Redux Toolkit', 'duration': 75, 'order': 7, 'is_free': False},
                    {'title': 'API Integration', 'description': 'REST API bilan ishlash', 'duration': 60, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'Python asoslari',
                'slug': 'python-asoslari',
                'description': 'Python dasturlash tilining asoslarini o\'rganing. Dasturlash dunyosiga birinchi qadamingni tashlang.',
                'price': 180000,
                'discount_price': 129000,
                'category': 'python-dasturlash',
                'level': 'beginner',
                'duration': '12 soat',
                'language': 'O\'zbek',
                'is_featured': True,
                'lessons': [
                    {'title': 'Python Kirish', 'description': 'Python haqida umumiy ma\'lumot', 'duration': 40, 'order': 1, 'is_free': True},
                    {'title': 'O\'zgaruvchilar va Turlar', 'description': 'Variables and Data Types', 'duration': 45, 'order': 2, 'is_free': True},
                    {'title': 'Shart operatorlari', 'description': 'If-else statements', 'duration': 50, 'order': 3, 'is_free': False},
                    {'title': 'Sikllar', 'description': 'For va while loop', 'duration': 55, 'order': 4, 'is_free': False},
                    {'title': 'Funksiyalar', 'description': 'Functions in Python', 'duration': 60, 'order': 5, 'is_free': False},
                    {'title': 'List va Tuple', 'description': 'Lists and Tuples', 'duration': 50, 'order': 6, 'is_free': False},
                    {'title': 'Dictionary', 'description': 'Dictionaries in Python', 'duration': 45, 'order': 7, 'is_free': False},
                    {'title': 'Fayllar bilan ishlash', 'description': 'File handling', 'duration': 55, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'Django Framework',
                'slug': 'django-framework',
                'description': 'Django frameworki bilan web-applications yaratishni o\'rganing. Backend dasturlashning eng yaxshi usuli.',
                'price': 400000,
                'discount_price': 299000,
                'category': 'python-dasturlash',
                'level': 'intermediate',
                'duration': '30 soat',
                'language': 'O\'zbek',
                'is_featured': True,
                'lessons': [
                    {'title': 'Django Kirish', 'description': 'Django haqida umumiy ma\'lumot', 'duration': 45, 'order': 1, 'is_free': True},
                    {'title': 'MVC/MPT Pattern', 'description': 'Model-View-Template pattern', 'duration': 50, 'order': 2, 'is_free': True},
                    {'title': 'Models', 'description': 'Django Models va ORM', 'duration': 60, 'order': 3, 'is_free': False},
                    {'title': 'Views va URLs', 'description': 'Views va URL routing', 'duration': 65, 'order': 4, 'is_free': False},
                    {'title': 'Templates', 'description': 'Django Templates', 'duration': 55, 'order': 5, 'is_free': False},
                    {'title': 'Forms', 'description': 'Django Forms', 'duration': 60, 'order': 6, 'is_free': False},
                    {'title': 'Authentication', 'description': 'User authentication', 'duration': 70, 'order': 7, 'is_free': False},
                    {'title': 'REST API', 'description': 'Django REST Framework', 'duration': 75, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'Flutter Mobile Dasturlash',
                'slug': 'flutter-mobile-dasturlash',
                'description': 'Flutter frameworki bilan iOS va Android uchun ilovalar yaratishni o\'rganing.',
                'price': 450000,
                'discount_price': 349000,
                'category': 'mobile-dasturlash',
                'level': 'intermediate',
                'duration': '35 soat',
                'language': 'O\'zbek',
                'is_featured': False,
                'lessons': [
                    {'title': 'Flutter Kirish', 'description': 'Flutter haqida umumiy ma\'lumot', 'duration': 45, 'order': 1, 'is_free': True},
                    {'title': 'Dart Asoslari', 'description': 'Dart programming language', 'duration': 60, 'order': 2, 'is_free': True},
                    {'title': 'Widgets', 'description': 'Flutter widgets', 'duration': 65, 'order': 3, 'is_free': False},
                    {'title': 'Layouts', 'description': 'Flutter layouts', 'duration': 70, 'order': 4, 'is_free': False},
                    {'title': 'State Management', 'description': 'Provider va Riverpod', 'duration': 75, 'order': 5, 'is_free': False},
                    {'title': 'Navigation', 'description': 'Flutter navigation', 'duration': 60, 'order': 6, 'is_free': False},
                    {'title': 'API Integration', 'description': 'REST API bilan ishlash', 'duration': 65, 'order': 7, 'is_free': False},
                    {'title': 'Firebase', 'description': 'Firebase integration', 'duration': 70, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'UI/UX Dizayn',
                'slug': 'ui-ux-dizayn',
                'description': 'Foydalanuvchi interfeysi va tajribasini yaratishni o\'rganing. Zamonaviy dizayn prinsiplarini bilib oling.',
                'price': 250000,
                'discount_price': 199000,
                'category': 'dizayn',
                'level': 'beginner',
                'duration': '20 soat',
                'language': 'O\'zbek',
                'is_featured': False,
                'lessons': [
                    {'title': 'UI/UX Kirish', 'description': 'UI va UX nima', 'duration': 40, 'order': 1, 'is_free': True},
                    {'title': 'Dizayn Prinsiplari', 'description': 'Asosiy dizayn prinsiplari', 'duration': 50, 'order': 2, 'is_free': True},
                    {'title': 'Color Theory', 'description': 'Ranglar nazariyasi', 'duration': 45, 'order': 3, 'is_free': False},
                    {'title': 'Typography', 'description': 'Shriftlar va tipografiya', 'duration': 50, 'order': 4, 'is_free': False},
                    {'title': 'Figma Asoslari', 'description': 'Figma bilan ishlash', 'duration': 60, 'order': 5, 'is_free': False},
                    {'title': 'Wireframing', 'description': 'Wireframe yaratish', 'duration': 55, 'order': 6, 'is_free': False},
                    {'title': 'Prototyping', 'description': 'Prototip yaratish', 'duration': 65, 'order': 7, 'is_free': False},
                    {'title': 'User Research', 'description': 'Foydalanuvchi tadqiqotlari', 'duration': 60, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'SMM Marketing',
                'slug': 'smm-marketing',
                'description': 'Ijtimoiy tarmoqlarda marketing qilishni o\'rganing. Instagram, Facebook, Telegram va TikTok uchun strategiyalar.',
                'price': 200000,
                'discount_price': 149000,
                'category': 'marketing',
                'level': 'beginner',
                'duration': '15 soat',
                'language': 'O\'zbek',
                'is_featured': False,
                'lessons': [
                    {'title': 'SMM Kirish', 'description': 'SMM haqida umumiy ma\'lumot', 'duration': 40, 'order': 1, 'is_free': True},
                    {'title': 'Instagram Marketing', 'description': 'Instagram strategiyalari', 'duration': 50, 'order': 2, 'is_free': True},
                    {'title': 'Facebook Ads', 'description': 'Facebook reklama', 'duration': 55, 'order': 3, 'is_free': False},
                    {'title': 'Telegram Marketing', 'description': 'Telegram kanallar va guruhlar', 'duration': 50, 'order': 4, 'is_free': False},
                    {'title': 'TikTok Marketing', 'description': 'TikTok strategiyalari', 'duration': 45, 'order': 5, 'is_free': False},
                    {'title': 'Content Creation', 'description': 'Kontent yaratish', 'duration': 60, 'order': 6, 'is_free': False},
                    {'title': 'Analytics', 'description': 'SMM analitikasi', 'duration': 55, 'order': 7, 'is_free': False},
                    {'title': 'Case Studies', 'description': 'Muvaffaqiyatli misollar', 'duration': 50, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'Startup Asoslari',
                'slug': 'startup-asoslari',
                'description': 'Startup yaratish va rivojlantirishni o\'rganing. Biznes modeli, moliyalashtirish va jamoa qurish.',
                'price': 300000,
                'discount_price': 249000,
                'category': 'biznes',
                'level': 'intermediate',
                'duration': '18 soat',
                'language': 'O\'zbek',
                'is_featured': False,
                'lessons': [
                    {'title': 'Startup Kirish', 'description': 'Startup nima', 'duration': 45, 'order': 1, 'is_free': True},
                    {'title': 'Idea Validation', 'description': 'G\'oyani tasdiqlash', 'duration': 50, 'order': 2, 'is_free': True},
                    {'title': 'Business Model', 'description': 'Biznes modeli yaratish', 'duration': 60, 'order': 3, 'is_free': False},
                    {'title': 'MVP Development', 'description': 'MVP yaratish', 'duration': 65, 'order': 4, 'is_free': False},
                    {'title': 'Team Building', 'description': 'Jamoa qurish', 'duration': 55, 'order': 5, 'is_free': False},
                    {'title': 'Fundraising', 'description': 'Moliyalashtirish', 'duration': 70, 'order': 6, 'is_free': False},
                    {'title': 'Pitch Deck', 'description': 'Pitch deck yaratish', 'duration': 60, 'order': 7, 'is_free': False},
                    {'title': 'Growth Hacking', 'description': 'O\'sish strategiyalari', 'duration': 65, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'Vue.js to\'liq kurs',
                'slug': 'vuejs-toliq-kurs',
                'description': 'Vue.js frameworkini chuqur o\'rganing. Zamonaviy veb-applications yaratishni bilib oling.',
                'price': 320000,
                'discount_price': 229000,
                'category': 'web-dasturlash',
                'level': 'intermediate',
                'duration': '22 soat',
                'language': 'O\'zbek',
                'is_featured': False,
                'lessons': [
                    {'title': 'Vue.js Kirish', 'description': 'Vue.js haqida umumiy ma\'lumot', 'duration': 45, 'order': 1, 'is_free': True},
                    {'title': 'Vue Instance', 'description': 'Vue instance yaratish', 'duration': 50, 'order': 2, 'is_free': True},
                    {'title': 'Components', 'description': 'Vue komponentlari', 'duration': 60, 'order': 3, 'is_free': False},
                    {'title': 'Props va Events', 'description': 'Props va Events', 'duration': 55, 'order': 4, 'is_free': False},
                    {'title': 'Vue Router', 'description': 'Vue Router', 'duration': 60, 'order': 5, 'is_free': False},
                    {'title': 'Vuex', 'description': 'Vuex state management', 'duration': 65, 'order': 6, 'is_free': False},
                    {'title': 'Composition API', 'description': 'Composition API', 'duration': 70, 'order': 7, 'is_free': False},
                    {'title': 'Vue 3 Features', 'description': 'Vue 3 yangiliklari', 'duration': 55, 'order': 8, 'is_free': False},
                ]
            },
            {
                'title': 'Data Science Python',
                'slug': 'data-science-python',
                'description': 'Python bilan Data Science o\'rganing. NumPy, Pandas, Matplotlib va Machine Learning.',
                'price': 500000,
                'discount_price': 399000,
                'category': 'python-dasturlash',
                'level': 'advanced',
                'duration': '40 soat',
                'language': 'O\'zbek',
                'is_featured': True,
                'lessons': [
                    {'title': 'Data Science Kirish', 'description': 'Data Science haqida', 'duration': 45, 'order': 1, 'is_free': True},
                    {'title': 'NumPy', 'description': 'NumPy kutubxonasi', 'duration': 60, 'order': 2, 'is_free': True},
                    {'title': 'Pandas', 'description': 'Pandas bilan ishlash', 'duration': 70, 'order': 3, 'is_free': False},
                    {'title': 'Matplotlib', 'description': 'Ma\'lumotlarni vizualizatsiya qilish', 'duration': 65, 'order': 4, 'is_free': False},
                    {'title': 'Data Cleaning', 'description': 'Ma\'lumotlarni tozalash', 'duration': 60, 'order': 5, 'is_free': False},
                    {'title': 'Machine Learning Kirish', 'description': 'ML asoslari', 'duration': 70, 'order': 6, 'is_free': False},
                    {'title': 'Scikit-learn', 'description': 'Scikit-learn kutubxonasi', 'duration': 75, 'order': 7, 'is_free': False},
                    {'title': 'Deep Learning', 'description': 'Deep Learning asoslari', 'duration': 80, 'order': 8, 'is_free': False},
                ]
            },
        ]
        
        # Create courses
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                slug=course_data['slug'],
                defaults={
                    'title': course_data['title'],
                    'description': course_data['description'],
                    'price': course_data['price'],
                    'discount_price': course_data['discount_price'],
                    'category': categories[course_data['category']],
                    'mentor': mentor,
                    'level': course_data['level'],
                    'duration': course_data['duration'],
                    'language': course_data['language'],
                    'is_published': True,
                    'is_featured': course_data['is_featured'],
                    'rating': 4.5,
                    'students_count': 0,
                }
            )
            
            if created:
                self.stdout.write(f'Created course: {course.title}')
                
                # Create lessons
                for lesson_data in course_data['lessons']:
                    Lesson.objects.create(
                        course=course,
                        title=lesson_data['title'],
                        description=lesson_data['description'],
                        duration=lesson_data['duration'],
                        order=lesson_data['order'],
                        is_free=lesson_data['is_free']
                    )
                self.stdout.write(f'  - Added {len(course_data["lessons"])} lessons')
            else:
                self.stdout.write(f'Course already exists: {course.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample courses added successfully!'))
