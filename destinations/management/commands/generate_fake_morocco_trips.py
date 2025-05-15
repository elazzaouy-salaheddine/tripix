# management/commands/generate_fake_morocco_trips.py
from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal
from django.utils.text import slugify
import uuid

from destinations.models import (
    Tag, Destination, Itinerary, 
    CostIncludeExclude, FAQ, RelatedTrip, 
    TourMap, Enquiry
)

class Command(BaseCommand):
    help = 'Generates fake data for Morocco trip models'

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(0)  # For consistent results
        
        self.stdout.write(self.style.SUCCESS('Creating fake Morocco trip data...'))
        
        # Create tags
        tag_names = [
            'Adventure', 'Cultural', 'Desert', 'Atlas Mountains', 
            'Sahara', 'Coastal', 'Historical', 'Food Tour', 
            'Hiking', 'Luxury', 'Budget', 'Family'
        ]
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
            self.stdout.write(f'Created tag: {tag.name}')
        
        # Moroccan cities and attractions
        morocco_destinations = [
            'Marrakech', 'Fes', 'Chefchaouen', 'Merzouga', 
            'Sahara Desert', 'Atlas Mountains Trek', 
            'Essaouira Coastal Tour', 'Ait Ben Haddou', 
            'Todgha Gorge', 'Dades Valley', 'Casablanca', 
            'Rabat', 'Tangier', 'Ouzoud Waterfalls'
        ]
        
        tour_types = [
            "Private Tour", "Group Tour", "Custom Tour", 
            "Luxury Tour", "Budget Tour", "Adventure Tour"
        ]
        
        seasons = [
            "Spring (March-May)", "Summer (June-August)", 
            "Autumn (September-November)", "Winter (December-February)"
        ]
        
        # Create destinations
        for i, dest_name in enumerate(morocco_destinations):
            # Randomly select 3-5 tags
            selected_tags = random.sample(tags, min(len(tags), random.randint(3, 5)))
            
            # Generate pricing - base price between 500 and 5000
            base_price = Decimal(random.randint(500, 5000))
            old_price = base_price * Decimal('1.2')  # 20% more than current price
            
            destination = Destination.objects.create(
                name=dest_name,
                location=f"{dest_name}, Morocco",
                accommodation=random.choice([
                    "4-star Hotels", "Luxury Riads", "Desert Camps", 
                    "Mountain Refuges", "Guest Houses"
                ]),
                best_season=random.choice(seasons),
                duration_days=random.randint(3, 14),
                elevation=f"{random.randint(500, 4000)}m" if "Mountain" in dest_name else "0m",  # Default to "0m"
                tour_types=", ".join(random.sample(tour_types, min(len(tour_types), random.randint(1, 3)))),  # Fixed missing parenthesis
                old_price=old_price,
                price=base_price,
                overview=fake.paragraph(nb_sentences=10),
                published=random.choice([True, False])
            )
            
            # Add tags
            destination.tags.set(selected_tags)
            
            self.stdout.write(f'Created destination: {destination.name}')
            
            # Create itineraries (3-7 days)
            num_days = destination.duration_days or random.randint(3, 7)
            for day in range(1, num_days + 1):
                Itinerary.objects.create(
                    destination=destination,
                    day=day,
                    title=f"Day {day}: {fake.sentence()}",
                    description=fake.paragraph(nb_sentences=5)
                )
            
            # Create cost includes (5-8 items)
            included_items = [
                "Accommodation", "Professional guide", "Meals as per itinerary",
                "Transportation", "Entrance fees", "Camel trek", "Airport transfers",
                "Local taxes", "Bottled water", "Cultural performances"
            ]
            sample_size = min(len(included_items), random.randint(5, 8))
            for item in random.sample(included_items, sample_size):
                CostIncludeExclude.objects.create(
                    destination=destination,
                    is_included=True,
                    item=item
                )
            
            # Create cost excludes (3-5 items)
            excluded_items = [
                "International flights", "Travel insurance", "Visa fees",
                "Personal expenses", "Tips", "Optional activities", "Alcoholic beverages",
                "Sleeping bags", "Gratuities", "Laundry services"
            ]
            sample_size = min(len(excluded_items), random.randint(3, 5))
            for item in random.sample(excluded_items, sample_size):
                CostIncludeExclude.objects.create(
                    destination=destination,
                    is_included=False,
                    item=item
                )
            
            # Create FAQs (3-5 questions)
            faq_questions = [
                "What should I pack for this trip?",
                "Is this tour suitable for children?",
                "What is the fitness level required?",
                "Are there any vaccination requirements?",
                "What is the cancellation policy?",
                "Can I customize this tour?",
                "What type of food will be served?",
                "Is there Wi-Fi available during the tour?",
                "What currency should I bring?",
                "Are there any cultural customs I should be aware of?"
            ]
            sample_size = min(len(faq_questions), random.randint(3, 5))
            for question in random.sample(faq_questions, sample_size):
                FAQ.objects.create(
                    destination=destination,
                    question=question,
                    answer=fake.paragraph(nb_sentences=3)
                )
            
            # Create related trips (2-4 trips)
            related_destinations = [d for d in morocco_destinations if d != dest_name]
            sample_size = min(len(related_destinations), random.randint(2, 4))
            for related_name in random.sample(related_destinations, sample_size):
                RelatedTrip.objects.create(
                    destination=destination,
                    name=f"{related_name} Adventure",
                    image=f"https://example.com/images/{slugify(related_name)}.jpg",
                    description=fake.paragraph(nb_sentences=3)
                )
            
            # Create tour map
            TourMap.objects.create(
                destination=destination,
                map_link=f"https://www.google.com/maps/embed/v1/place?key=YOUR_API_KEY&q={dest_name},Morocco"  # Replace YOUR_API_KEY
            )
            
            # Create some enquiries (1-3 per destination)
            for _ in range(random.randint(1, 3)):
                Enquiry.objects.create(
                    destination=destination,
                    name=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    Country=fake.country(),  # Fixed field name
                    NoofAdults=random.randint(1, 4),  # Fixed field name
                    NoofChildren=random.randint(0, 2),  # Fixed field name
                    EnquirySubject=f"Question about {destination.name} tour",  # Fixed field name
                    message=fake.paragraph(nb_sentences=3)
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully created fake Morocco trip data!'))
