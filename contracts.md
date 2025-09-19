# API Contracts - Tantawan Restaurant

## Overview
This document defines the API contracts between the frontend and backend for the Tantawan restaurant website, covering the ordering system and newsletter functionality.

## Data Models

### MenuItem
```json
{
  "id": "string",
  "category": "string", // "Vorspeisen", "Hauptgerichte", "Desserts"
  "name": "string",
  "description": "string",
  "price": "number",
  "image": "string", // URL
  "available": "boolean",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### Order
```json
{
  "id": "string",
  "items": [
    {
      "menuItemId": "string",
      "name": "string",
      "price": "number",
      "quantity": "number"
    }
  ],
  "customer": {
    "name": "string",
    "phone": "string",
    "notes": "string"
  },
  "pickupTime": "datetime",
  "total": "number",
  "status": "string", // "pending", "confirmed", "preparing", "ready", "completed", "cancelled"
  "orderNumber": "string", // Auto-generated
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### Newsletter Subscription
```json
{
  "id": "string",
  "email": "string",
  "isActive": "boolean",
  "subscribedAt": "datetime",
  "unsubscribedAt": "datetime"
}
```

## API Endpoints

### Menu Items

#### GET /api/menu
Get all menu items
- **Response**: Array of MenuItem objects
- **Status Codes**: 200 (success), 500 (server error)

#### GET /api/menu/:category
Get menu items by category
- **Parameters**: category (string)
- **Response**: Array of MenuItem objects
- **Status Codes**: 200 (success), 404 (category not found), 500 (server error)

### Orders

#### POST /api/orders
Create a new order
- **Request Body**:
  ```json
  {
    "items": [
      {
        "menuItemId": "string",
        "quantity": "number"
      }
    ],
    "customer": {
      "name": "string",
      "phone": "string",
      "notes": "string"
    },
    "pickupTime": "datetime"
  }
  ```
- **Response**: Order object with generated ID and order number
- **Status Codes**: 201 (created), 400 (bad request), 500 (server error)

#### GET /api/orders/:id
Get order by ID
- **Parameters**: id (string)
- **Response**: Order object
- **Status Codes**: 200 (success), 404 (not found), 500 (server error)

#### PUT /api/orders/:id/status
Update order status (admin functionality)
- **Parameters**: id (string)
- **Request Body**: 
  ```json
  {
    "status": "string"
  }
  ```
- **Response**: Updated Order object
- **Status Codes**: 200 (updated), 400 (bad request), 404 (not found), 500 (server error)

### Newsletter

#### POST /api/newsletter/subscribe
Subscribe to newsletter
- **Request Body**:
  ```json
  {
    "email": "string"
  }
  ```
- **Response**: 
  ```json
  {
    "message": "Successfully subscribed",
    "subscription": {
      "id": "string",
      "email": "string",
      "subscribedAt": "datetime"
    }
  }
  ```
- **Status Codes**: 201 (created), 400 (bad request/already subscribed), 500 (server error)

#### DELETE /api/newsletter/subscribe/:email
Unsubscribe from newsletter
- **Parameters**: email (string)
- **Response**: 
  ```json
  {
    "message": "Successfully unsubscribed"
  }
  ```
- **Status Codes**: 200 (success), 404 (not found), 500 (server error)

## Frontend Integration Changes

### Mock Data Removal
- Remove `mockData.js` dependencies for menu items
- Replace with API calls to `/api/menu`
- Remove mock orders array

### Cart Component Updates
- Replace mock order submission with POST to `/api/orders`
- Add proper error handling for API failures
- Show order confirmation with order number

### Newsletter Component Updates
- Replace mock subscription with POST to `/api/newsletter/subscribe`
- Handle duplicate subscription errors gracefully
- Add unsubscribe functionality

### Menu Component Updates
- Fetch menu items from `/api/menu` on component mount
- Add loading states while fetching data
- Handle API errors gracefully

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "message": "string",
    "code": "string",
    "details": "object" // optional
  }
}
```

### Common Error Codes
- `INVALID_INPUT`: Bad request data
- `NOT_FOUND`: Resource not found
- `DUPLICATE_EMAIL`: Email already subscribed
- `ORDER_FAILED`: Order creation failed
- `SERVER_ERROR`: Internal server error

## Database Collections

### menu_items
- Stores all menu items with categories
- Indexed on: category, available

### orders
- Stores all customer orders
- Indexed on: status, createdAt, orderNumber

### newsletter_subscriptions
- Stores newsletter subscriptions
- Indexed on: email (unique), isActive

## Implementation Priority

1. **Menu API**: Basic menu fetching functionality
2. **Order API**: Core ordering system with customer data
3. **Newsletter API**: Email subscription management
4. **Frontend Integration**: Remove mocks, add API calls
5. **Error Handling**: Comprehensive error states
6. **Order Status**: Admin functionality (future enhancement)

## Notes

- All datetime fields use ISO 8601 format
- Order numbers are generated using format: `TW-{YYYYMMDD}-{XXXX}` (e.g., TW-20250919-0001)
- Phone numbers should be validated for Swiss format
- Email validation uses standard regex pattern
- All monetary values are in CHF with 2 decimal places