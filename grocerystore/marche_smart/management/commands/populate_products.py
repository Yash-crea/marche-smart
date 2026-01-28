from django.core.management.base import BaseCommand
from marche_smart.models import Category, Product


class Command(BaseCommand):
    help = 'Populate the database with sample categories and products'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Vegetables', 'description': 'Fresh vegetables'},
            {'name': 'Fruits', 'description': 'Fresh fruits'},
            {'name': 'Dairy', 'description': 'Milk, cheese, and dairy products'},
            {'name': 'Meat & Fish', 'description': 'Fresh meat and fish'},
            {'name': 'Bread & Bakery', 'description': 'Bread and bakery items'},
            {'name': 'Beverages', 'description': 'Drinks and beverages'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create sample products
        products_data = [
            # Vegetables
            {'name': 'Tomatoes', 'category': 'Vegetables', 'price': 3.99, 'description': 'Fresh red tomatoes'},
            {'name': 'Carrots', 'category': 'Vegetables', 'price': 2.49, 'description': 'Organic carrots'},
            {'name': 'Lettuce', 'category': 'Vegetables', 'price': 2.99, 'description': 'Fresh green lettuce'},
            {'name': 'Broccoli', 'category': 'Vegetables', 'price': 3.49, 'description': 'Fresh broccoli florets'},
            {'name': 'Onions', 'category': 'Vegetables', 'price': 1.99, 'description': 'Yellow onions'},
            
            # Fruits
            {'name': 'Apples', 'category': 'Fruits', 'price': 4.99, 'description': 'Red delicious apples'},
            {'name': 'Bananas', 'category': 'Fruits', 'price': 2.49, 'description': 'Fresh yellow bananas'},
            {'name': 'Oranges', 'category': 'Fruits', 'price': 3.99, 'description': 'Fresh oranges'},
            {'name': 'Strawberries', 'category': 'Fruits', 'price': 5.99, 'description': 'Fresh strawberries'},
            {'name': 'Grapes', 'category': 'Fruits', 'price': 4.49, 'description': 'Green seedless grapes'},
            
            # Dairy
            {'name': 'Milk', 'category': 'Dairy', 'price': 3.49, 'description': '1L whole milk'},
            {'name': 'Cheese', 'category': 'Dairy', 'price': 6.99, 'description': 'Cheddar cheese block'},
            {'name': 'Yogurt', 'category': 'Dairy', 'price': 3.99, 'description': 'Greek yogurt'},
            {'name': 'Butter', 'category': 'Dairy', 'price': 5.49, 'description': 'Unsalted butter'},
            
            # Meat & Fish
            {'name': 'Chicken Breast', 'category': 'Meat & Fish', 'price': 9.99, 'description': 'Boneless chicken breast'},
            {'name': 'Ground Beef', 'category': 'Meat & Fish', 'price': 8.99, 'description': 'Lean ground beef'},
            {'name': 'Salmon', 'category': 'Meat & Fish', 'price': 14.99, 'description': 'Fresh salmon fillet'},
            
            # Bread & Bakery
            {'name': 'Whole Wheat Bread', 'category': 'Bread & Bakery', 'price': 3.49, 'description': 'Fresh whole wheat bread'},
            {'name': 'Bagels', 'category': 'Bread & Bakery', 'price': 4.99, 'description': 'Fresh bagels pack'},
            
            # Beverages
            {'name': 'Orange Juice', 'category': 'Beverages', 'price': 4.99, 'description': 'Fresh orange juice 1L'},
            {'name': 'Coffee', 'category': 'Beverages', 'price': 8.99, 'description': 'Ground coffee 1lb'},
            {'name': 'Tea', 'category': 'Beverages', 'price': 3.49, 'description': 'Assorted tea pack'},
        ]

        for prod_data in products_data:
            category = categories[prod_data['category']]
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'price': prod_data['price'],
                    'description': prod_data['description'],
                    'in_stock': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))
