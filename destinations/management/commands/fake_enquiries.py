# your_app/management/commands/fake_enquiries.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from destinations.models import Destination, Enquiry


class Command(BaseCommand):
    help = 'Creates fake enquiry data for all existing destinations'

    def handle(self, *args, **kwargs):
        fake = Faker()
        destinations = Destination.objects.all()

        if not destinations.exists():
            self.stdout.write(self.style.ERROR("No destinations found. Please add destinations first."))
            return

        for destination in destinations:
            num_enquiries = fake.random_int(min=3, max=5)
            self.stdout.write(f"Creating {num_enquiries} enquiries for destination: {destination.name}")

            for _ in range(num_enquiries):
                Enquiry.objects.create(
                    destination=destination,
                    name=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number()[:20],  # Limit to 20 chars
                    Country=fake.country(),           # CharField(max_length=100)
                    NoofAdults=fake.random_int(min=1, max=10),
                    NoofChildren=fake.random_element(elements=(None, fake.random_int(min=0, max=5))),
                    EnquirySubject=fake.sentence(nb_words=6)[:255],  # Respect max_length=255
                    message=fake.paragraph(nb_sentences=5),
                )

            self.stdout.write(self.style.SUCCESS(f"Created {num_enquiries} enquiries for '{destination.name}'"))

        self.stdout.write(self.style.SUCCESS("Successfully created fake enquiries for all destinations."))