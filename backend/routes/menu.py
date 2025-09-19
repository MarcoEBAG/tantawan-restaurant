from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import MenuItem, MenuItemCreate, Category
from database import get_database

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/", response_model=List[MenuItem])
async def get_all_menu_items(db=Depends(get_database)):
    """Get all menu items"""
    try:
        cursor = db.menu_items.find({"available": True})
        menu_items = []
        async for item in cursor:
            # Convert MongoDB _id to id
            item["id"] = str(item.pop("_id", item.get("id")))
            menu_items.append(MenuItem(**item))
        
        return menu_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch menu items: {str(e)}")


@router.get("/{category}", response_model=List[MenuItem])
async def get_menu_items_by_category(category: Category, db=Depends(get_database)):
    """Get menu items by category"""
    try:
        cursor = db.menu_items.find({"category": category.value, "available": True})
        menu_items = []
        async for item in cursor:
            # Convert MongoDB _id to id
            item["id"] = str(item.pop("_id", item.get("id")))
            menu_items.append(MenuItem(**item))
        
        if not menu_items:
            raise HTTPException(status_code=404, detail=f"No menu items found for category: {category.value}")
        
        return menu_items
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch menu items: {str(e)}")


@router.post("/", response_model=MenuItem)
async def create_menu_item(item: MenuItemCreate, db=Depends(get_database)):
    """Create a new menu item (admin functionality)"""
    try:
        menu_item = MenuItem(**item.dict())
        result = await db.menu_items.insert_one(menu_item.dict())
        
        if result.inserted_id:
            menu_item.id = str(result.inserted_id)
            return menu_item
        else:
            raise HTTPException(status_code=500, detail="Failed to create menu item")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create menu item: {str(e)}")


@router.get("/item/{item_id}", response_model=MenuItem)
async def get_menu_item(item_id: str, db=Depends(get_database)):
    """Get a specific menu item by ID"""
    try:
        item = await db.menu_items.find_one({"id": item_id})
        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        
        # Convert MongoDB _id to id
        item["id"] = str(item.pop("_id", item.get("id")))
        return MenuItem(**item)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch menu item: {str(e)}")