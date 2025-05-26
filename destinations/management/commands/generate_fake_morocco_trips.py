# your_app/management/commands/fake_data.py

import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from faker import Faker
from destinations.models import (
    Destination, Itinerary, CostIncludeExclude,
    FAQ, RelatedTrip, TourMap, GalleryImage, TopDestination, Tag
)

User = get_user_model()
fake = Faker()


def safe_text(length=20):
    """Generate text safely within max_length"""
    return fake.sentence(nb_words=6)[:length] if len(fake.sentence()) > length else fake.sentence()


class Command(BaseCommand):
    help = 'Generates fake destinations and related data for all existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found in the database.'))
            return

        tags = list(Tag.objects.all())
        if not tags:
            self.stdout.write(self.style.WARNING('No tags found. Creating sample tags...'))
            tags = [Tag.objects.create(name=fake.word().capitalize()) for _ in range(5)]

        for user in users:
            self.stdout.write(f"Creating data for user: {user.username}")

            # Generate 3–5 destinations per user
            for _ in range(fake.random_int(min=3, max=5)):
                destination = Destination(
                    name=safe_text(100),
                    location=safe_text(100) if fake.boolean() else "",
                    accommodation=fake.random_element(elements=("Hotel", "Camping", "Lodge")),
                    best_season=safe_text(100) if fake.boolean() else "",
                    duration_days=fake.random_int(min=3, max=15),
                    elevation=safe_text(100) if fake.boolean() else "",
                    tour_types=safe_text(100) if fake.boolean() else "",
                    old_price=Decimal(fake.random.uniform(500, 1000)).quantize(Decimal('0.00')),
                    price=Decimal(fake.random.uniform(300, 800)).quantize(Decimal('0.00')),
                    overview=fake.paragraphs(nb=5),
                    created_by=user,
                    published=True
                )
                destination.save()

                # Add random tags
                destination.tags.add(*fake.random_elements(elements=tags, length=fake.random_int(min=1, max=3)))

                # Add itinerary
                for day in range(1, fake.random_int(min=3, max=7) + 1):
                    Itinerary.objects.create(
                        destination=destination,
                        day=day,
                        title=safe_text(100),
                        description=fake.paragraph()
                    )

                # Add cost includes/excludes
                for _ in range(3):
                    CostIncludeExclude.objects.create(
                        destination=destination,
                        is_included=True,
                        item=safe_text(100)
                    )
                for _ in range(3):
                    CostIncludeExclude.objects.create(
                        destination=destination,
                        is_included=False,
                        item=safe_text(100)
                    )

                # Add FAQs
                for _ in range(3):
                    FAQ.objects.create(
                        destination=destination,
                        question=safe_text(100),
                        answer=fake.paragraph()
                    )

                # Add Related Trips
                for _ in range(2):
                    RelatedTrip.objects.create(
                        destination=destination,
                        name=safe_text(100),
                        image="https://via.placeholder.com/600x400 ",
                        description=safe_text(100)
                    )

                # Add Tour Map


                # Add Gallery Images
                for _ in range(3):
                    GalleryImage.objects.create(
                        destination=destination,
                        image="https://via.placeholder.com/800x600 "
                    )

                # Add Top Destination
                if fake.boolean(chance_of_getting_true=30):
                    TopDestination.objects.create(
                        destination=destination,
                        label=safe_text(20),
                        order=fake.random_int(min=1, max=100)
                    )

                self.stdout.write(self.style.SUCCESS(f"Created destination: {destination.name}"))

        self.stdout.write(self.style.SUCCESS("Successfully generated fake data for all users."))