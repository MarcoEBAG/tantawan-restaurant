from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List
from datetime import datetime
from ..models import Order, OrderCreate, OrderStatusUpdate, OrderStatus
from ..database import get_database, generate_order_number
from ..services.email_service import email_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order)
async def create_order(
    order_data: OrderCreate, 
    background_tasks: BackgroundTasks,
    db=Depends(get_database)
):
    """Create a new order with automatic notifications"""
    try:
        # Calculate total
        total = sum(item.price * item.quantity for item in order_data.items)
        
        # Generate order number
        order_number = await generate_order_number()
        
        # Create order object
        order = Order(
            items=order_data.items,
            customer=order_data.customer,
            pickup_time=order_data.pickup_time,
            total=total,
            order_number=order_number
        )
        
        # Insert into database
        result = await db.orders.insert_one(order.dict())
        
        if result.inserted_id:
            # Add background tasks for notifications
            background_tasks.add_task(email_service.send_order_notification, order)
            background_tasks.add_task(email_service.send_order_to_printer, order)
            
            return order
        else:
            raise HTTPException(status_code=500, detail="Failed to create order")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str, db=Depends(get_database)):
    """Get order by ID"""
    try:
        order = await db.orders.find_one({"id": order_id})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Convert MongoDB _id to id if needed
        order["id"] = str(order.pop("_id", order.get("id")))
        return Order(**order)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch order: {str(e)}")


@router.get("/number/{order_number}", response_model=Order)
async def get_order_by_number(order_number: str, db=Depends(get_database)):
    """Get order by order number"""
    try:
        order = await db.orders.find_one({"order_number": order_number})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Convert MongoDB _id to id if needed
        order["id"] = str(order.pop("_id", order.get("id")))
        return Order(**order)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch order: {str(e)}")


@router.put("/{order_id}/status", response_model=Order)
async def update_order_status(order_id: str, status_update: OrderStatusUpdate, db=Depends(get_database)):
    """Update order status"""
    try:
        # Find the order first
        order = await db.orders.find_one({"id": order_id})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Update status and timestamp
        update_data = {
            "status": status_update.status.value,
            "updated_at": datetime.utcnow()
        }
        
        result = await db.orders.update_one(
            {"id": order_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to update order status")
        
        # Return updated order
        updated_order = await db.orders.find_one({"id": order_id})
        updated_order["id"] = str(updated_order.pop("_id", updated_order.get("id")))
        return Order(**updated_order)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update order status: {str(e)}")


@router.get("/", response_model=List[Order])
async def get_orders(
    status: OrderStatus = None, 
    limit: int = 50,
    skip: int = 0,
    db=Depends(get_database)
):
    """Get orders with optional filtering"""
    try:
        query = {}
        if status:
            query["status"] = status.value
        
        cursor = db.orders.find(query).sort("created_at", -1).skip(skip).limit(limit)
        orders = []
        async for order in cursor:
            # Convert MongoDB _id to id
            order["id"] = str(order.pop("_id", order.get("id")))
            orders.append(Order(**order))
        
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {str(e)}")


@router.get("/customer/{phone}", response_model=List[Order])
async def get_customer_orders(phone: str, db=Depends(get_database)):
    """Get orders by customer phone number"""
    try:
        cursor = db.orders.find({"customer.phone": phone}).sort("created_at", -1)
        orders = []
        async for order in cursor:
            # Convert MongoDB _id to id
            order["id"] = str(order.pop("_id", order.get("id")))
            orders.append(Order(**order))
        
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch customer orders: {str(e)}")