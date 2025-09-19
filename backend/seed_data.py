"""
Seed data script for Tantawan Restaurant
Populates the database with initial menu items
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from models import MenuItem, Category

# Menu items data
MENU_ITEMS = [
    # Vorspeisen
    {
        "category": Category.VORSPEISEN,
        "name": "Frühlingsrollen (4 Stück)",
        "description": "Knusprige Frühlingsrollen mit Gemüsefüllung, serviert mit süß-sauer Sauce",
        "price": 8.50,
        "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop&crop=center"
    },
    {
        "category": Category.VORSPEISEN,
        "name": "Gyoza (6 Stück)",
        "description": "Japanische Teigtaschen mit Schweinefleisch und Gemüse",
        "price": 9.80,
        "image": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=400&h=300&fit=crop&crop=center"
    },
    {
        "category": Category.VORSPEISEN,
        "name": "Tom Kha Gai Suppe",
        "description": "Thai Kokosnusssuppe mit Huhn, Galangal und Zitronengras",
        "price": 7.90,
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=300&fit=crop&crop=center"
    },
    
    # Hauptgerichte
    {
        "category": Category.HAUPTGERICHTE,
        "name": "Pad Thai mit Huhn",
        "description": "Klassische Thai-Nudeln mit Huhn, Ei, Bohnensprossen und Erdnüssen",
        "price": 16.50,
        "image": "https://images.unsplash.com/photo-1559847844-d2e2c6880675?w=400&h=300&fit=crop&crop=center"
    },
    {
        "category": Category.HAUPTGERICHTE,
        "name": "Sweet & Sour Schweinefleisch",
        "description": "Knuspriges Schweinefleisch mit Ananas, Paprika in süß-saurer Sauce",
        "price": 17.80,
        "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=center"
    },
    {
        "category": Category.HAUPTGERICHTE,
        "name": "Beef Teriyaki",
        "description": "Zartes Rindfleisch in Teriyaki-Sauce mit Sesam und Frühlingszwiebeln",
        "price": 19.90,
        "image": "https://images.unsplash.com/photo-1534939561126-855b8675edd7?w=400&h=300&fit=crop&crop=center"
    },
    {
        "category": Category.HAUPTGERICHTE,
        "name": "Vegetarisches Curry",
        "description": "Gemischtes Gemüse in cremiger Kokosmilch-Curry-Sauce",
        "price": 15.50,
        "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400&h=300&fit=crop&crop=center"
    },
    {
        "category": Category.HAUPTGERICHTE,
        "name": "Gebratene Nudeln mit Ente",
        "description": "Breite Reisnudeln mit knuspriger Ente und chinesischem Brokkoli",
        "price": 21.50,
        "image": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=400&h=300&fit=crop&crop=center"
    },
    {
        "category": Category.HAUPTGERICHTE,
        "name": "Kung Pao Huhn",
        "description": "Scharfes Huhn mit Erdnüssen, Chili und Szechuan-Pfefferkörner",
        "price": 18.20,
        "image": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop&crop=center"
    },
    
    # Desserts
    {
        "category": Category.DESSERTS,
        "name": "Mango Sticky Rice",
        "description": "Traditioneller Thai-Dessert mit süßem Klebreis und frischer Mango",
        "price": 6.50,
        "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center"
    },
    {
        "category": Category.DESSERTS,
        "name": "Sesam-Eiscreme",
        "description": "Hausgemachte Eiscreme mit schwarzem Sesam",
        "price": 5.50,
        "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=300&fit=crop&crop=center"
    }
]


async def seed_menu_items():
    """Seed the database with menu items"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(os.environ["MONGO_URL"])
        db = client[os.environ["DB_NAME"]]
        
        # Clear existing menu items
        await db.menu_items.delete_many({})
        print("🗑️  Cleared existing menu items")
        
        # Insert new menu items
        menu_items = []
        for item_data in MENU_ITEMS:
            menu_item = MenuItem(**item_data)
            menu_items.append(menu_item.dict())
        
        result = await db.menu_items.insert_many(menu_items)
        print(f"✅ Inserted {len(result.inserted_ids)} menu items")
        
        # Create indexes
        await db.menu_items.create_index("category")
        await db.menu_items.create_index("available")
        print("✅ Created menu items indexes")
        
        # Close connection
        client.close()
        print("✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    from pathlib import Path
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent
    load_dotenv(ROOT_DIR / '.env')
    
    # Run seeding
    asyncio.run(seed_menu_items())