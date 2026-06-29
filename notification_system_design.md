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



# Stage 2

## Database Choice

I recommend **PostgreSQL** because it is reliable, scalable, open-source, and supports indexing, transactions, and large datasets efficiently. It is suitable for storing millions of notifications while maintaining good query performance.

---

## Database Schema

### Users

| Column | Type |
|---------|------|
| id | BIGSERIAL PRIMARY KEY |
| name | VARCHAR(100) |
| email | VARCHAR(255) UNIQUE |

### Notifications

| Column | Type |
|---------|------|
| id | BIGSERIAL PRIMARY KEY |
| user_id | BIGINT REFERENCES users(id) |
| title | VARCHAR(255) |
| message | TEXT |
| type | VARCHAR(50) |
| is_read | BOOLEAN DEFAULT FALSE |
| created_at | TIMESTAMP |

---

## SQL Queries

### Insert Notification

```sql
INSERT INTO notifications(user_id, title, message, type)
VALUES (101, 'Placement Drive', 'TCS hiring starts tomorrow', 'Placement');
```

### Get User Notifications

```sql
SELECT *
FROM notifications
WHERE user_id = 101
ORDER BY created_at DESC;
```

### Mark Notification as Read

```sql
UPDATE notifications
SET is_read = TRUE
WHERE id = 15;
```

### Delete Notification

```sql
DELETE FROM notifications
WHERE id = 15;
```

---

## Scalability

As the number of users and notifications increases:

- Create indexes on `user_id`, `created_at`, and `is_read`.
- Use pagination (`LIMIT` and `OFFSET`) to avoid loading all notifications at once.
- Archive old notifications.
- Partition the notifications table by date if the dataset becomes very large.
- Add read replicas for handling heavy read traffic.

---

## REST API and Database Flow

- `POST /api/notifications` → Insert notification into the database.
- `GET /api/notifications` → Fetch notifications for a user.
- `PUT /api/notifications/{id}/read` → Update notification status.
- `DELETE /api/notifications/{id}` → Remove a notification from the database.