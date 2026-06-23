from django.utils import timezone

from .models import Announcement


def site_announcement(request):
    now = timezone.now()
    ann = Announcement.objects.filter(is_active=True).order_by('-id').first()
    if not ann:
        return {}
    if ann.start_at and ann.start_at > now:
        return {}
    if ann.end_at and ann.end_at < now:
        return {}
    return {'site_announcement': ann}
