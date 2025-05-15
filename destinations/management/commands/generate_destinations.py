# core/management/commands/generate_destinations.py

import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from destinations.models import Destination, Tag, Itinerary, CostIncludeExclude, FAQ, RelatedTrip, TourMap
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake destination data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=5, help='Number of destinations to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        # Sample tags to assign randomly
        tag_names = [
            "Hiking", "Adventure", "Cultural", "Eco-Tourism",
            "Beach", "Luxury", "Family Friendly", "Budget Travel"
        ]
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        for _ in range(count):
            # Generate fake destination
            name = fake.catch_phrase().title()
            location = fake.city()
            duration_days = random.randint(3, 14)
            price = round(random.uniform(500, 5000), 2)

            destination = Destination.objects.create(
                name=name,
                image="https://via.placeholder.com/800x400.png?text= " + name.replace(" ", "+"),
                overview=fake.paragraph(nb_sentences=5),
                location=location,
                accommodation=random.choice(["3 Stars", "4 Stars", "5 Stars"]),
                best_season=", ".join([fake.month_name() for _ in range(3)]),
                duration_days=duration_days,
                elevation=fake.random_element(elements=("1000m", "2000m", "3000m", "4000m")),
                tour_types=fake.random_element(elements=("Group Tour", "Solo Travel", "Private")),
                price=price
            )

            # Assign random tags
            destination.tags.add(*random.sample(tags, k=random.randint(2, 4)))

            # Add itinerary
            for day in range(1, duration_days + 1):
                Itinerary.objects.create(
                    destination=destination,
                    day=day,
                    title=fake.sentence(nb_words=4).rstrip('.'),
                    description=fake.paragraph(nb_sentences=3)
                )

            # Add cost includes/excludes
            includes = [
                "Accommodation", "Meals", "Transport", "Guide", "Entry Fees"
            ]
            excludes = [
                "Flights", "Insurance", "Tips", "Personal Expenses"
            ]

            for item in random.sample(includes, k=random.randint(2, len(includes))):
                CostIncludeExclude.objects.create(
                    destination=destination,
                    is_included=True,
                    item=item
                )

            for item in random.sample(excludes, k=random.randint(1, len(excludes))):
                CostIncludeExclude.objects.create(
                    destination=destination,
                    is_included=False,
                    item=item
                )

            # Add FAQs
            faq_questions = [
                "What is the difficulty level?",
                "Do I need travel insurance?",
                "Can I customize the trip?",
                "Are flights included?",
                "What is the cancellation policy?"
            ]
            for question in random.sample(faq_questions, k=3):
                FAQ.objects.create(
                    destination=destination,
                    question=question,
                    answer=fake.paragraph(nb_sentences=2)
                )

            # Add related trips
            for _ in range(2):
                RelatedTrip.objects.create(
                    destination=destination,
                    name=fake.catch_phrase().title(),
                    image="https://via.placeholder.com/300x200.png?text=Related+Trip ",
                    description=fake.sentence(nb_words=8)
                )

            # Add tour map (fake Google Maps link)
            TourMap.objects.create(
                destination=destination,
                map_link=f"https://maps.google.com/?q= {location}"
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} fake destinations'))