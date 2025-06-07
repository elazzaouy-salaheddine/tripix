from django.contrib import admin
from .models import Subscriber, SubscriberTag, SubscriberList
from .models import EmailTemplate, EmailCampaign
from .models import CampaignOpen, CampaignLinkClick, Unsubscribe

admin.site.register(Subscriber)
admin.site.register(SubscriberTag)
admin.site.register(SubscriberList)
admin.site.register(EmailTemplate)
admin.site.register(EmailCampaign)
admin.site.register(CampaignOpen)
admin.site.register(CampaignLinkClick)
admin.site.register(Unsubscribe)