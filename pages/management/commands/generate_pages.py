from django.core.management.base import BaseCommand
from faker import Faker
from pages.models import TermsAndConditions, PrivacyPolicy, FAQ, AboutPage
import random
from datetime import datetime

class Command(BaseCommand):
    help = 'Generates fake data for pages app (Terms, Privacy, FAQ, About)'

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(0)  # For consistent results
        
        self.stdout.write(self.style.SUCCESS('Generating fake pages data...'))
        
        # Generate Terms and Conditions
        terms = TermsAndConditions.objects.create(
            title="Terms of Service - Oktrip.club",
            content=self._generate_legal_content(fake),
            acceptance_required=random.choice([True, False]),
            version="1.0",
            meta_title="Terms of Service | Oktrip.club",
            meta_description="Read our terms and conditions for using Oktrip.club travel services"
        )
        self.stdout.write(self.style.SUCCESS(f'Created Terms: {terms.title}'))
        
        # Generate Privacy Policy
        privacy = PrivacyPolicy.objects.create(
            title="Privacy Policy - Oktrip.club",
            content=self._generate_privacy_content(fake),
            version="1.1",
            data_controller="Oktrip Travel Club",
            contact_email="privacy@oktrip.club",
            meta_title="Privacy Policy | Oktrip.club",
            meta_description="How we protect and use your data at Oktrip.club"
        )
        self.stdout.write(self.style.SUCCESS(f'Created Privacy Policy: {privacy.title}'))
        
        # Generate About Page
        about = AboutPage.objects.create(
            title="About Oktrip Travel Club",
            content=self._generate_about_content(fake),
            mission_statement=fake.paragraph(nb_sentences=3),
            values=self._generate_values(fake),
            history=self._generate_history(fake),
            meta_title="About Us | Oktrip.club",
            meta_description="Discover our story and mission to make travel better"
        )
        self.stdout.write(self.style.SUCCESS(f'Created About Page: {about.title}'))
        
        # Generate FAQs
        categories = ['Booking', 'Payments', 'Destinations', 'Account', 'General']
        faq_count = 15
        
        for i in range(faq_count):
            faq = FAQ.objects.create(
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(nb_sentences=5),
                category=random.choice(categories),
                order=i,
                meta_title=f"{fake.sentence(nb_words=4)} | Oktrip.club FAQ",
                meta_description=fake.sentence(nb_words=10)
            )
            self.stdout.write(self.style.SUCCESS(f'Created FAQ #{i+1}: {faq.title}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully generated all pages data!'))

    def _generate_legal_content(self, fake):
        sections = [
            "Introduction", "User Obligations", "Prohibited Activities",
            "Intellectual Property", "Termination", "Limitation of Liability"
        ]
        content = ""
        for section in sections:
            content += f"<h2>{section}</h2>\n"
            content += f"<p>{fake.paragraph(nb_sentences=8)}</p>\n"
            if random.random() > 0.5:
                content += f"<ul>\n"
                for _ in range(random.randint(3, 6)):
                    content += f"<li>{fake.sentence(nb_words=8)}</li>\n"
                content += f"</ul>\n"
        return content

    def _generate_privacy_content(self, fake):
        sections = [
            "Information We Collect", "How We Use Your Data",
            "Data Sharing", "Your Rights", "Cookies", "Security Measures"
        ]
        content = ""
        for section in sections:
            content += f"<h2>{section}</h2>\n"
            content += f"<p>{fake.paragraph(nb_sentences=6)}</p>\n"
            if section == "Information We Collect":
                content += "<h3>Personal Data</h3>\n<ul>\n"
                content += "<li>Name and contact details</li>\n"
                content += "<li>Payment information</li>\n"
                content += "<li>Travel preferences</li>\n"
                content += "</ul>\n"
        return content

    def _generate_about_content(self, fake):
        content = f"<p>{fake.paragraph(nb_sentences=5)}</p>\n"
        content += f"<p>{fake.paragraph(nb_sentences=4)}</p>\n"
        content += "<h2>Our Team</h2>\n"
        content += "<p>Meet the passionate travelers behind Oktrip.club:</p>\n"
        content += "<div class='row'>\n"
        for i in range(4):
            content += f"<div class='col-md-3'>\n"
            content += f"<h3>{fake.name()}</h3>\n"
            content += f"<p>{fake.job()} specializing in {fake.country()}</p>\n"
            content += "</div>\n"
        content += "</div>\n"
        return content

    def _generate_values(self, fake):
        values = [
            "Sustainable Travel", "Authentic Experiences",
            "Community Focus", "Transparency", "Adventure"
        ]
        content = "<ul>\n"
        for value in values:
            content += f"<li><strong>{value}:</strong> {fake.paragraph(nb_sentences=2)}</li>\n"
        content += "</ul>\n"
        return content

    def _generate_history(self, fake):
        years = [2018, 2019, 2020, 2021, 2022, 2023]
        content = "<div class='timeline'>\n"
        for year in years:
            content += f"<div class='timeline-item'>\n"
            content += f"<h3>{year}</h3>\n"
            content += f"<p>{fake.paragraph(nb_sentences=3)}</p>\n"
            content += "</div>\n"
        content += "</div>\n"
        return content