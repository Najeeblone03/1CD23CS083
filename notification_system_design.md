# Stage 1 - Notification System Design

## Objective
Design a REST API for a notification system that allows users to receive notifications when they log in.

---

# REST API Endpoints

## 1. Get Notifications

**GET** `/api/notifications`

### Request Headers

```
Authorization: Bearer <token>
Content-Type: application/json
```

### Response

```json
{
  "success": true,
  "notifications": [
    {
      "id": 1,
      "title": "Placement Drive",
      "message": "TCS hiring starts tomorrow.",
      "type": "Placement",
      "isRead": false,
      "createdAt": "2026-06-29T10:30:00Z"
    }
  ]
}
```

---

## 2. Mark Notification as Read

**PUT** `/api/notifications/{id}/read`

### Request Headers

```
Authorization: Bearer <token>
Content-Type: application/json
```

### Response

```json
{
  "success": true,
  "message": "Notification marked as read."
}
```

---

## 3. Delete Notification

**DELETE** `/api/notifications/{id}`

### Request Headers

```
Authorization: Bearer <token>
```

### Response

```json
{
  "success": true,
  "message": "Notification deleted."
}
```

---

## 4. Send Notification (Admin)

**POST** `/api/notifications`

### Request

```json
{
  "title": "Exam Schedule",
  "message": "Semester exams begin next week.",
  "type": "Exam"
}
```

### Response

```json
{
  "success": true,
  "message": "Notification sent successfully."
}
```

---

# Real-Time Notification Design

The system uses WebSockets for real-time communication.

Flow:

1. User logs in.
2. Client establishes a WebSocket connection.
3. Server pushes new notifications instantly.
4. User receives notifications without refreshing the page.
5. Notifications are stored in the database.

---

# Advantages

- Fast delivery
- Real-time updates
- Scalable
- Easy to maintain
- REST APIs for CRUD operations
- WebSocket for live notifications