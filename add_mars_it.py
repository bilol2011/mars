import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilol_project.settings')
django.setup()

from apps.courses.models import EducationalCenter

# Create MARS IT School
mars_it, created = EducationalCenter.objects.get_or_create(
    slug='mars-it-school',
    defaults={
        'name': 'MARS IT School',
        'description': '''9 yoshdan 17 yoshgacha bo'lgan bolalar uchun kompyuter kurslari. 
Darslar 9 yoshdan 17 yoshgacha barcha bolalar uchun, ayniqsa kompyuter o'yinlaridan chalg'imaydigan 
va dasturlash olamiga qiziqishi katta bo'lganlar uchun.

Bizda o'quvchilar uchun Space onlayn platformasi mavjud. Shaxsiy kabinetda bolalar uy vazifalari, 
darslarini va to'plagan coin'lar sonini ko'rishlari mumkin.

Professional o'qituvchidan tashqari, yordamchi o'qituvchimiz ham bor. U har doim uy vazifalari, 
yaxshi tushunilmagan mavzular va o'tkazib yuborilgan darslarda yordam beradi.

Biz o'quvchilarni nazorat qilish uchun kursimizga 4 ta vositani kiritdik:
- Shaxsiy reja: Har oyda o'qituvchi sizga nima tugatilganligi, o'rganilishi kerak bo'lgan narsalarni aytib beradi 
  va bolangizni yanada rivojlantirish bo'yicha tavsiyalar beradi.
- Oylik hisobot: Siz har oyda markazimiz o'qituvchilaridan farzandingiz muvaffaqiyati haqida hisobot olasiz. 
  Shaxsiy kabinetni ham kuzatib borasiz.

4 yil ichida minglab o'quvchilarni tayyorladik, Toshkent bo'ylab filiallar ochdik va kuchli o'qituvchilar jamoasini yig'dik.''',
        'short_description': '9 yoshdan 17 yoshgacha bo\'lgan bolalar uchun kompyuter kurslari. Farzandingizga IT kasbini tanlashga yordam beradigan bepul proforiyentatsion testga yoziling.',
        'phone': '+998787777757',
        'email': 'info@marsit.uz',
        'address': '''Toshkent shahri bo'ylab 7 ta filial:
1. Tinchlik filiali: Beruniy ko'chasi 35A, Tinchlik metro bekati
2. Yunusobod filiali: Yunusobod tumani, Yangishahar 10
3. Chilonzor filiali: Chilonzor tumani, 8-kvartal, 2-uy
4. Mirzo-Ulugbek filiali: Mirzo-Ulugbek tumani, Buyuk Ipak yo'li, 152/1
5. Sergeli filiali: Sergeli tumani, Sug'diyona mahallasi
6. Minor filiali: Yunusobod tumani, Kiyev massivi, 3A
7. Oybek filiali: Mirobod tumani, Taras Shevchenko ko'chasi, 24''',
        'city': 'Toshkent',
        'website': 'https://marsit.uz',
        'telegram': 'https://t.me/marsituz',
        'instagram': 'https://instagram.com/marsit.uz',
        'facebook': 'https://facebook.com/marsit.uz',
        'rating': 4.8,
        'reviews_count': 150,
        'students_count': 2500,
        'courses_count': 15,
        'is_featured': True,
        'is_active': True,
    }
)

if created:
    print(f"MARS IT School muvaffaqiyatli qo'shildi!")
else:
    print(f"MARS IT School allaqachon mavjud. Yangilandi.")
    mars_it.description = '''9 yoshdan 17 yoshgacha bo'lgan bolalar uchun kompyuter kurslari. 
Darslar 9 yoshdan 17 yoshgacha barcha bolalar uchun, ayniqsa kompyuter o'yinlaridan chalg'imaydigan 
va dasturlash olamiga qiziqishi katta bo'lganlar uchun.

Bizda o'quvchilar uchun Space onlayn platformasi mavjud. Shaxsiy kabinetda bolalar uy vazifalari, 
darslarini va to'plagan coin'lar sonini ko'rishlari mumkin.

Professional o'qituvchidan tashqari, yordamchi o'qituvchimiz ham bor. U har doim uy vazifalari, 
yaxshi tushunilmagan mavzular va o'tkazib yuborilgan darslarda yordam beradi.

Biz o'quvchilarni nazorat qilish uchun kursimizga 4 ta vositani kiritdik:
- Shaxsiy reja: Har oyda o'qituvchi sizga nima tugatilganligi, o'rganilishi kerak bo'lgan narsalarni aytib beradi 
  va bolangizni yanada rivojlantirish bo'yicha tavsiyalar beradi.
- Oylik hisobot: Siz har oyda markazimiz o'qituvchilaridan farzandingiz muvaffaqiyati haqida hisobot olasiz. 
  Shaxsiy kabinetni ham kuzatib borasiz.

4 yil ichida minglab o'quvchilarni tayyorladik, Toshkent bo'ylab filiallar ochdik va kuchli o'qituvchilar jamoasini yig'dik.'''
    mars_it.short_description = '9 yoshdan 17 yoshgacha bo\'lgan bolalar uchun kompyuter kurslari. Farzandingizga IT kasbini tanlashga yordam beradigan bepul proforiyentatsion testga yoziling.'
    mars_it.phone = '+998787777757'
    mars_it.email = 'info@marsit.uz'
    mars_it.address = '''Toshkent shahri bo'ylab 7 ta filial:
1. Tinchlik filiali: Beruniy ko'chasi 35A, Tinchlik metro bekati
2. Yunusobod filiali: Yunusobod tumani, Yangishahar 10
3. Chilonzor filiali: Chilonzor tumani, 8-kvartal, 2-uy
4. Mirzo-Ulugbek filiali: Mirzo-Ulugbek tumani, Buyuk Ipak yo'li, 152/1
5. Sergeli filiali: Sergeli tumani, Sug'diyona mahallasi
6. Minor filiali: Yunusobod tumani, Kiyev massivi, 3A
7. Oybek filiali: Mirobod tumani, Taras Shevchenko ko'chasi, 24'''
    mars_it.website = 'https://marsit.uz'
    mars_it.telegram = 'https://t.me/marsituz'
    mars_it.instagram = 'https://instagram.com/marsit.uz'
    mars_it.facebook = 'https://facebook.com/marsit.uz'
    mars_it.rating = 4.8
    mars_it.reviews_count = 150
    mars_it.students_count = 2500
    mars_it.courses_count = 15
    mars_it.is_featured = True
    mars_it.save()
    print(f"MARS IT School ma'lumotlari yangilandi!")

print(f"\nMARS IT School ma'lumotlari:")
print(f"Nom: {mars_it.name}")
print(f"Telefon: {mars_it.phone}")
print(f"Email: {mars_it.email}")
print(f"Website: {mars_it.website}")
print(f"Telegram: {mars_it.telegram}")
print(f"Instagram: {mars_it.instagram}")
print(f"Facebook: {mars_it.facebook}")
print(f"Reyting: {mars_it.rating}")
print(f"O'quvchilar soni: {mars_it.students_count}")
print(f"Kurslar soni: {mars_it.courses_count}")
