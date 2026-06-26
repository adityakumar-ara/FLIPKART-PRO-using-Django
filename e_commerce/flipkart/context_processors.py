from django.db.models import Q
from django.utils import timezone

from .models import Announcement


def site_announcement(request):
    now = timezone.now()
    ann = Announcement.objects.filter(
        is_active=True
    ).filter(
        Q(start_at__lte=now) | Q(start_at__isnull=True),
        Q(end_at__gte=now) | Q(end_at__isnull=True),
    ).order_by('-id').first()
    if not ann:
        return {}
    return {'site_announcement': ann}
