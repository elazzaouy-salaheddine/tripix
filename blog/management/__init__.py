# blog/management/commands/generate_blog_data.py

import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post, Category, Tag, Comment
from django.contrib.auth import get_user_model
from faker import Faker
#TODO FAKER NOT WORK AND CHEK VIEWS URL AND TEMPLATES OF THE BLOG
fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = 'Generates fake blog data including posts, categories, tags, and comments'

    def add_arguments(self, parser):
        parser.add_argument('--posts', type=int, default=10, help='Number of posts to create')
        parser.add_argument('--categories', type=int, default=5, help='Number of categories to create')
        parser.add_argument('--tags', type=int, default=10, help='Number of tags to create')
        parser.add_argument('--comments', type=int, default=3, help='Max number of comments per post')

    def handle(self, *args, **kwargs):
        num_posts = kwargs['posts']
        num_categories = kwargs['categories']
        num_tags = kwargs['tags']
        max_comments = kwargs['comments']

        # Get or create sample users
        try:
            user = User.objects.first()
        except Exception:
            self.stdout.write(self.style.ERROR("No user found. Please create at least one user first."))
            return

        # Generate categories
        category_names = ["Adventure", "Culture", "Food", "Nature", "Tips", "Destinations", "Hiking", "Luxury", "Budget", "Family"]
        categories = []
        for name in category_names[:num_categories]:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            categories.append(category)

        # Generate tags
        tag_names = [
            "Travel Tips", "Solo Travel", "Photography", "Backpacking",
            "Local Culture", "Eco-Tourism", "Foodie", "Beach Life",
            "Mountain Views", "City Exploration"
        ]
        tags = []
        for name in tag_names[:num_tags]:
            tag, created = Tag.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            tags.append(tag)

        # Generate posts
        posts = []
        for _ in range(num_posts):
            title = fake.sentence(nb_words=6).rstrip('.')
            post = Post.objects.create(
                title=title,
                slug=slugify(title) + '-' + str(random.randint(1000, 9999)),
                author=user,
                content='\n\n'.join(fake.paragraphs(nb=5)),
                excerpt=fake.sentence(nb_words=15),
                category=random.choice(categories),
                published=True
            )
            post.tags.add(*random.sample(tags, k=random.randint(2, 5)))
            posts.append(post)

        # Generate comments
        for post in posts:
            for _ in range(random.randint(0, max_comments)):
                Comment.objects.create(
                    post=post,
                    name=fake.name(),
                    email=fake.email(),
                    content=fake.sentence(nb_words=15),
                    approved=True
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_posts} posts, '
                                            f'{len(categories)} categories, '
                                            f'{len(tags)} tags, and {Comment.objects.count()} comments'))