from django.core.management.base import BaseCommand
from faker import Faker
import random
from pages.models import TravelGuide, AboutPage

class Command(BaseCommand):
    help = "Generate 3 fake travel guides"

    def handle(self, *args, **kwargs):
        fake = Faker()
        about = AboutPage.objects.first()

        if not about:
            self.stdout.write(self.style.ERROR('No AboutPage found. Create one first.'))
            return

        roles = ['Senior Guide', 'Cultural Expert', 'Adventure Specialist']
        specialties = ['Sahara Desert', 'High Atlas', 'Nomadic Culture', 'Draa Valley']
        langs = ['English, French', 'Arabic, Spanish', 'Tamazight, French', 'English, Arabic']

        for _ in range(3):
            guide = TravelGuide.objects.create(
                about_page=about,
                name=fake.name(),
                title=random.choice(roles),
                photo=None,  # Add a path or skip if no media
                bio=fake.paragraph(nb_sentences=4),
                expertise=random.choice(specialties),
                languages=random.choice(langs),
                facebook=fake.url(),
                instagram=fake.url(),
       
                is_featured=random.choice([True, False]),
                order=random.randint(1, 10)
            )
            self.stdout.write(self.style.SUCCESS(f"Created guide: {guide.name}"))
