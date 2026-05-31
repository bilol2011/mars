from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Certificate
from .services import build_certificate_pdf


@login_required
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id, user=request.user)
    response = HttpResponse(build_certificate_pdf(certificate), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_id}.pdf"'
    return response


def verify_certificate(request, certificate_id):
    certificate = get_object_or_404(
        Certificate.objects.select_related('user', 'course'),
        certificate_id=certificate_id,
    )
    return render(request, 'certificates/verify.html', {'certificate': certificate, 'is_valid': True})
