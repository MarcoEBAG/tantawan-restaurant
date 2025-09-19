from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from ..models import NewsletterSubscription, NewsletterSubscribe, NewsletterResponse
from ..database import get_database

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("/subscribe", response_model=NewsletterResponse)
async def subscribe_newsletter(subscription_data: NewsletterSubscribe, db=Depends(get_database)):
    """Subscribe to newsletter"""
    try:
        # Check if email already exists
        existing = await db.newsletter_subscriptions.find_one({"email": subscription_data.email})
        
        if existing:
            if existing.get("is_active", False):
                raise HTTPException(
                    status_code=400, 
                    detail="Email is already subscribed to newsletter"
                )
            else:
                # Reactivate subscription
                await db.newsletter_subscriptions.update_one(
                    {"email": subscription_data.email},
                    {
                        "$set": {
                            "is_active": True,
                            "subscribed_at": datetime.utcnow(),
                            "unsubscribed_at": None
                        }
                    }
                )
                
                return NewsletterResponse(
                    message="Successfully resubscribed to newsletter",
                    subscription={
                        "id": existing.get("id"),
                        "email": subscription_data.email,
                        "subscribed_at": datetime.utcnow().isoformat()
                    }
                )
        else:
            # Create new subscription
            subscription = NewsletterSubscription(email=subscription_data.email)
            result = await db.newsletter_subscriptions.insert_one(subscription.dict())
            
            if result.inserted_id:
                return NewsletterResponse(
                    message="Successfully subscribed to newsletter",
                    subscription={
                        "id": subscription.id,
                        "email": subscription.email,
                        "subscribed_at": subscription.subscribed_at.isoformat()
                    }
                )
            else:
                raise HTTPException(status_code=500, detail="Failed to subscribe to newsletter")
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to subscribe: {str(e)}")


@router.delete("/subscribe/{email}", response_model=NewsletterResponse)
async def unsubscribe_newsletter(email: str, db=Depends(get_database)):
    """Unsubscribe from newsletter"""
    try:
        # Find the subscription
        subscription = await db.newsletter_subscriptions.find_one({"email": email})
        
        if not subscription:
            raise HTTPException(status_code=404, detail="Email not found in newsletter subscriptions")
        
        if not subscription.get("is_active", False):
            raise HTTPException(status_code=400, detail="Email is already unsubscribed")
        
        # Update subscription to inactive
        result = await db.newsletter_subscriptions.update_one(
            {"email": email},
            {
                "$set": {
                    "is_active": False,
                    "unsubscribed_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            return NewsletterResponse(message="Successfully unsubscribed from newsletter")
        else:
            raise HTTPException(status_code=500, detail="Failed to unsubscribe")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unsubscribe: {str(e)}")


@router.get("/subscriptions/count")
async def get_subscription_count(db=Depends(get_database)):
    """Get total number of active subscriptions"""
    try:
        count = await db.newsletter_subscriptions.count_documents({"is_active": True})
        return {"active_subscriptions": count}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subscription count: {str(e)}")


@router.get("/subscriptions")
async def get_all_subscriptions(
    active_only: bool = True,
    limit: int = 100,
    skip: int = 0,
    db=Depends(get_database)
):
    """Get all newsletter subscriptions (admin functionality)"""
    try:
        query = {"is_active": True} if active_only else {}
        
        cursor = db.newsletter_subscriptions.find(query).sort("subscribed_at", -1).skip(skip).limit(limit)
        subscriptions = []
        async for sub in cursor:
            # Convert MongoDB _id to id
            sub["id"] = str(sub.pop("_id", sub.get("id")))
            subscriptions.append(NewsletterSubscription(**sub))
        
        return subscriptions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch subscriptions: {str(e)}")