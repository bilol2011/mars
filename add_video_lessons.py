import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilol_project.settings')
django.setup()

from django.db.models import Q
from apps.courses.models import Lesson

# Sample YouTube video URLs for different topics
video_urls = {
    'python': [
        'https://www.youtube.com/watch?v=kqtD5dpn9C8',
        'https://www.youtube.com/watch?v=xiq9Fj5WLH0',
        'https://www.youtube.com/watch?v=ix6rT1AeK4Q',
        'https://www.youtube.com/watch?v=1F2gjTQ5jg0',
        'https://www.youtube.com/watch?v=Q_IR8jJ8fZQ',
        'https://www.youtube.com/watch?v=Gz1-2k3k4k5',
        'https://www.youtube.com/watch?v=6l7j1k8l9m0',
        'https://www.youtube.com/watch?v=n0o1p2q3r4s',
    ],
    'javascript': [
        'https://www.youtube.com/watch?v=hZ1lD7J0gK0',
        'https://www.youtube.com/watch?v=PkZNo7MFNFg',
        'https://www.youtube.com/watch?v=hdI2bqOjy3c',
        'https://www.youtube.com/watch?v=Bv_5Zv5cF8Q',
        'https://www.youtube.com/watch?v=2Ievh8Z6QkU',
        'https://www.youtube.com/watch?v=Zf5v1eW4k5Y',
        'https://www.youtube.com/watch?v=6X6x6x6x6x6',
        'https://www.youtube.com/watch?v=7y7y7y7y7y7',
    ],
    'html': [
        'https://www.youtube.com/watch?v=qz0aGYrrlhU',
        'https://www.youtube.com/watch?v=kUMe1FH4CHE',
        'https://www.youtube.com/watch?v=1Rs2ND1ryYc',
        'https://www.youtube.com/watch?v=yfoY53QXEnI',
        'https://www.youtube.com/watch?v=pQNpv1j2V4Q',
        'https://www.youtube.com/watch?v=jV8B24rSN5o',
        'https://www.youtube.com/watch?v=Ru1WpB1vW8M',
        'https://www.youtube.com/watch?v=Hc3O3lxJQk8',
    ],
    'css': [
        'https://www.youtube.com/watch?v=1Rs2ND1ryYc',
        'https://www.youtube.com/watch?v=yfoY53QXEnI',
        'https://www.youtube.com/watch?v=pQNpv1j2V4Q',
        'https://www.youtube.com/watch?v=jV8B24rSN5o',
        'https://www.youtube.com/watch?v=Ru1WpB1vW8M',
        'https://www.youtube.com/watch?v=Hc3O3lxJQk8',
        'https://www.youtube.com/watch?v=1Rs2ND1ryYc',
        'https://www.youtube.com/watch?v=yfoY53QXEnI',
    ],
    'react': [
        'https://www.youtube.com/watch?v=w7ejDZ8SWv8',
        'https://www.youtube.com/watch?v=SqcY0GlETPk',
        'https://www.youtube.com/watch?v=Ke90Tje7VS0',
        'https://www.youtube.com/watch?v=Rh3tobs8pBw',
        'https://www.youtube.com/watch?v=CvPaNeKU8fI',
        'https://www.youtube.com/watch?v=sBws8QXvhcw',
        'https://www.youtube.com/watch?v=nXOVWvxPch0',
        'https://www.youtube.com/watch?v=1wZo7MHJTRw',
    ],
    'vue': [
        'https://www.youtube.com/watch?v=FXpIoQ_rT_c',
        'https://www.youtube.com/watch?v=nhBVL41-_Cw',
        'https://www.youtube.com/watch?v=4deVCNJy3d0',
        'https://www.youtube.com/watch?v=qZXt1Aom3Cs',
        'https://www.youtube.com/watch?v=7o0zM9bP6lM',
        'https://www.youtube.com/watch?v=9Jc2i8a6lIw',
        'https://www.youtube.com/watch?v=0N3P0NNEz4M',
        'https://www.youtube.com/watch?v=8pDqJVmN1lI',
    ],
    'django': [
        'https://www.youtube.com/watch?v=F5mRW0jo224',
        'https://www.youtube.com/watch?v=Uml6XSmRfKW',
        'https://www.youtube.com/watch?v=PtX3hS3pXx8',
        'https://www.youtube.com/watch?v=qgjrr8T2DqY',
        'https://www.youtube.com/watch?v=JeznW_7DlB0',
        'https://www.youtube.com/watch?v=Urxw-K2S5jk',
        'https://www.youtube.com/watch?v=J0Bw8y3YbQ8',
        'https://www.youtube.com/watch?v=0M1uN8sJ3C0',
    ],
    'flutter': [
        'https://www.youtube.com/watch?v=VPvVD8t0U9E',
        'https://www.youtube.com/watch?v=1RwQ3zC-8oU',
        'https://www.youtube.com/watch?v=wU7kan9fC1M',
        'https://www.youtube.com/watch?v=MVx5Qw1LqkI',
        'https://www.youtube.com/watch?v=3fJ1t8y6W4Y',
        'https://www.youtube.com/watch?v=5t1f8g2k3l4',
        'https://www.youtube.com/watch?v=6m7n8o9p0q1',
        'https://www.youtube.com/watch?v=8r9s0t1u2v3',
    ],
    'uiux': [
        'https://www.youtube.com/watch?v=03b3OThXz1M',
        'https://www.youtube.com/watch?v=9N0V3m7m6m5',
        'https://www.youtube.com/watch?v=4l5n6o7p8q9',
        'https://www.youtube.com/watch?v=0r1s2t3u4v5',
        'https://www.youtube.com/watch?v=6w7x8y9z0a1',
        'https://www.youtube.com/watch?v=2b3c4d5e6f7',
        'https://www.youtube.com/watch?v=8g9h0i1j2k3',
        'https://www.youtube.com/watch?v=4l5m6n7o8p9',
    ],
    'smm': [
        'https://www.youtube.com/watch?v=K4qDfBXI8h0',
        'https://www.youtube.com/watch?v=7n8o9p0q1r2',
        'https://www.youtube.com/watch?v=3s4t5u6v7w8',
        'https://www.youtube.com/watch?v=9x0y1z2a3b4',
        'https://www.youtube.com/watch?v=5c6d7e8f9g0',
        'https://www.youtube.com/watch?v=1h2i3j4k5l6',
        'https://www.youtube.com/watch?v=7m8n9o0p1q2',
        'https://www.youtube.com/watch?v=3r4s5t6u7v8',
    ],
    'startup': [
        'https://www.youtube.com/watch?v=8t9u0v1w2x3',
        'https://www.youtube.com/watch?v=4y5z6a7b8c9',
        'https://www.youtube.com/watch?v=0d1e2f3g4h5',
        'https://www.youtube.com/watch?v=6i7j8k9l0m1',
        'https://www.youtube.com/watch?v=2n3o4p5q6r7',
        'https://www.youtube.com/watch?v=8s9t0u1v2w3',
        'https://www.youtube.com/watch?v=4x5y6z7a8b9',
        'https://www.youtube.com/watch?v=0c1d2e3f4g5',
    ],
    'data': [
        'https://www.youtube.com/watch?v=ru3qu1YfYs8',
        'https://www.youtube.com/watch?v=4YZ9sS2y8oY',
        'https://www.youtube.com/watch?v=xxadD1XE0aY',
        'https://www.youtube.com/watch?v=QIU4vXj4xLQ',
        'https://www.youtube.com/watch?v=TxD1HdC6J0k',
        'https://www.youtube.com/watch?v=7e8f9g0h1i2',
        'https://www.youtube.com/watch?v=3j4k5l6m7n8',
        'https://www.youtube.com/watch?v=9o0p1q2r3s4',
    ],
}

lessons = Lesson.objects.filter(video_url__isnull=True) | Lesson.objects.filter(video_url='')
print(f'Found {lessons.count()} lessons without video')

updated_count = 0
for lesson in lessons:
    title_lower = lesson.title.lower()
    
    # Determine topic based on lesson title
    if 'python' in title_lower or 'django' in title_lower:
        topic = 'python' if 'python' in title_lower else 'django'
    elif 'javascript' in title_lower or 'js' in title_lower:
        topic = 'javascript'
    elif 'html' in title_lower or 'css' in title_lower:
        topic = 'html' if 'html' in title_lower else 'css'
    elif 'react' in title_lower:
        topic = 'react'
    elif 'vue' in title_lower:
        topic = 'vue'
    elif 'flutter' in title_lower:
        topic = 'flutter'
    elif 'ui' in title_lower or 'ux' in title_lower or 'figma' in title_lower or 'design' in title_lower:
        topic = 'uiux'
    elif 'smm' in title_lower or 'marketing' in title_lower or 'instagram' in title_lower or 'facebook' in title_lower:
        topic = 'smm'
    elif 'startup' in title_lower or 'business' in title_lower or 'fundraising' in title_lower:
        topic = 'startup'
    elif 'data' in title_lower or 'machine' in title_lower or 'numpy' in title_lower or 'pandas' in title_lower:
        topic = 'data'
    else:
        topic = 'python'  # default
    
    # Get video URL for this topic
    if topic in video_urls:
        # Use lesson order to pick different videos
        videos = video_urls[topic]
        video_index = (lesson.order - 1) % len(videos)
        lesson.video_url = videos[video_index]
        lesson.save()
        updated_count += 1
        print(f'Updated: {lesson.title} -> {lesson.video_url}')

print(f'\nTotal updated: {updated_count}')
