from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
from models import Order, OrderStatus, OrderStatusUpdate
from database import get_database

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/orders", response_model=List[Order])
async def get_all_orders(
    status: Optional[OrderStatus] = None,
    date_from: Optional[str] = Query(None, description="Date from (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Date to (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    db=Depends(get_database)
):
    """Get all orders with filtering options for admin dashboard"""
    try:
        query = {}
        
        # Filter by status
        if status:
            query["status"] = status.value
        
        # Filter by date range
        if date_from or date_to:
            date_filter = {}
            if date_from:
                date_filter["$gte"] = datetime.fromisoformat(date_from)
            if date_to:
                # Add one day to include the entire end date
                end_date = datetime.fromisoformat(date_to) + timedelta(days=1)
                date_filter["$lt"] = end_date
            query["created_at"] = date_filter
        
        cursor = db.orders.find(query).sort("created_at", -1).skip(skip).limit(limit)
        orders = []
        async for order in cursor:
            # Convert MongoDB _id to id
            order["id"] = str(order.pop("_id", order.get("id")))
            orders.append(Order(**order))
        
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {str(e)}")


@router.get("/orders/pending", response_model=List[Order])
async def get_pending_orders(db=Depends(get_database)):
    """Get all pending orders for kitchen display"""
    try:
        cursor = db.orders.find({
            "status": {"$in": ["pending", "confirmed", "preparing"]}
        }).sort("created_at", 1)  # Oldest first for kitchen
        
        orders = []
        async for order in cursor:
            order["id"] = str(order.pop("_id", order.get("id")))
            orders.append(Order(**order))
        
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pending orders: {str(e)}")


@router.get("/orders/today", response_model=List[Order])
async def get_todays_orders(db=Depends(get_database)):
    """Get today's orders"""
    try:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        cursor = db.orders.find({
            "created_at": {
                "$gte": today_start,
                "$lt": today_end
            }
        }).sort("created_at", -1)
        
        orders = []
        async for order in cursor:
            order["id"] = str(order.pop("_id", order.get("id")))
            orders.append(Order(**order))
        
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch today's orders: {str(e)}")


@router.put("/orders/{order_id}/status", response_model=Order)
async def update_order_status_admin(
    order_id: str, 
    status_update: OrderStatusUpdate, 
    db=Depends(get_database)
):
    """Update order status - enhanced for admin use"""
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


@router.get("/orders/stats")
async def get_order_stats(db=Depends(get_database)):
    """Get order statistics for dashboard"""
    try:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # Get today's stats
        today_orders = await db.orders.count_documents({
            "created_at": {"$gte": today_start, "$lt": today_end}
        })
        
        # Get revenue today
        pipeline = [
            {"$match": {"created_at": {"$gte": today_start, "$lt": today_end}}},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total"}}}
        ]
        revenue_result = await db.orders.aggregate(pipeline).to_list(1)
        today_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
        
        # Get status counts
        status_pipeline = [
            {"$match": {"created_at": {"$gte": today_start, "$lt": today_end}}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        status_results = await db.orders.aggregate(status_pipeline).to_list(10)
        status_counts = {result["_id"]: result["count"] for result in status_results}
        
        # Get pending orders count
        pending_count = await db.orders.count_documents({
            "status": {"$in": ["pending", "confirmed", "preparing"]}
        })
        
        return {
            "today": {
                "orders": today_orders,
                "revenue": round(today_revenue, 2)
            },
            "status_counts": status_counts,
            "pending_orders": pending_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch order stats: {str(e)}")


@router.delete("/orders/{order_id}")
async def delete_order(order_id: str, db=Depends(get_database)):
    """Delete an order (admin only - use with caution)"""
    try:
        result = await db.orders.delete_one({"id": order_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {"message": f"Order {order_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete order: {str(e)}")


@router.get("/orders/search")
async def search_orders(
    q: str = Query(..., description="Search query (order number, customer name, or phone)"),
    limit: int = Query(20, ge=1, le=100),
    db=Depends(get_database)
):
    """Search orders by order number, customer name, or phone"""
    try:
        # Create search query
        search_query = {
            "$or": [
                {"order_number": {"$regex": q, "$options": "i"}},
                {"customer.name": {"$regex": q, "$options": "i"}},
                {"customer.phone": {"$regex": q, "$options": "i"}}
            ]
        }
        
        cursor = db.orders.find(search_query).sort("created_at", -1).limit(limit)
        orders = []
        async for order in cursor:
            order["id"] = str(order.pop("_id", order.get("id")))
            orders.append(Order(**order))
        
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search orders: {str(e)}")