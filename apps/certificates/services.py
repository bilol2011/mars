from django.db import transaction

from .models import Certificate


@transaction.atomic
def issue_certificate(user, course):
    certificate, _ = Certificate.objects.get_or_create(user=user, course=course)
    return certificate


def build_certificate_pdf(certificate):
    lines = [
        '%PDF-1.4',
        '1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj',
        '2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj',
        '3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 842 595] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >> endobj',
        '4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj',
        '5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> endobj',
    ]
    user_name = certificate.user.get_full_name() or certificate.user.email
    issued_date = certificate.issued_at.strftime('%Y-%m-%d')
    content = (
        'BT /F2 34 Tf 250 500 Td (BILOL Certificate) Tj ET\n'
        'BT /F1 16 Tf 245 455 Td (This certifies that) Tj ET\n'
        f'BT /F2 26 Tf 220 415 Td ({_pdf_escape(user_name)}) Tj ET\n'
        'BT /F1 16 Tf 210 375 Td (successfully completed the course) Tj ET\n'
        f'BT /F2 24 Tf 180 335 Td ({_pdf_escape(certificate.course.title)}) Tj ET\n'
        f'BT /F1 13 Tf 120 270 Td (Completion date: {issued_date}) Tj ET\n'
        f'BT /F1 13 Tf 120 245 Td (Certificate ID: {certificate.certificate_id}) Tj ET\n'
        '0 0 0 RG 620 180 120 120 re S\n'
        'BT /F1 11 Tf 642 235 Td (QR placeholder) Tj ET\n'
    )
    stream = f'6 0 obj << /Length {len(content.encode("latin-1", "ignore"))} >> stream\n{content}endstream endobj'
    lines.append(stream)
    body = '\n'.join(lines) + '\n'
    offsets = []
    cursor = 0
    for part in body.splitlines(True):
        if part.endswith(' obj << /Type /Catalog /Pages 2 0 R >> endobj\n') or part[:1].isdigit() and ' 0 obj' in part:
            offsets.append(cursor)
        cursor += len(part.encode('latin-1', 'ignore'))
    xref_start = len(body.encode('latin-1', 'ignore'))
    xref = ['xref', '0 7', '0000000000 65535 f ']
    for offset in offsets[:6]:
        xref.append(f'{offset:010d} 00000 n ')
    trailer = f'trailer << /Size 7 /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF'
    return (body + '\n'.join(xref) + '\n' + trailer).encode('latin-1', 'ignore')


def _pdf_escape(value):
    return str(value).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
