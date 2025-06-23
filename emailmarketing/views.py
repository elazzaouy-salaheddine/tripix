from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Subscriber

@require_POST
def subscribe_view(request):
    email = request.POST.get("email", "").strip()

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'status': 'danger', 'message': 'Invalid email address.'})

    # Try to create or get existing subscriber
    subscriber, created = Subscriber.objects.get_or_create(email=email)

    if not created:
        if subscriber.subscribed:
            return JsonResponse({'status': 'info', 'message': 'You are already subscribed.'})
        else:
            subscriber.subscribed = True
            subscriber.save()
            return JsonResponse({'status': 'success', 'message': 'Subscription re-enabled.'})
    else:
        return JsonResponse({'status': 'success', 'message': 'Subscribed successfully!'})
