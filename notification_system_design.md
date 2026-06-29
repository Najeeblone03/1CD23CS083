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
# Stage 3

## Query Analysis

Current Query:

```sql
SELECT *
FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt ASC;
```

### Is this query accurate?

Yes. It fetches all unread notifications for a student ordered by creation time.

### Why is it slow?

- Database contains millions of notifications.
- `SELECT *` retrieves unnecessary columns.
- Missing indexes on `studentID`, `isRead`, and `createdAt`.
- Sorting a large dataset is expensive.

### Better Solution

Create a composite index:

```sql
CREATE INDEX idx_notifications
ON notifications(studentID, isRead, createdAt);
```

Fetch only required columns:

```sql
SELECT id, title, message, createdAt
FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt ASC;
```

### Should we index every column?

No.

Adding indexes to every column:
- Increases storage.
- Slows INSERT and UPDATE operations.
- Makes database maintenance harder.

Indexes should only be created on frequently searched or sorted columns.

### Query to find placement notifications in the last 7 days

```sql
SELECT DISTINCT studentID
FROM notifications
WHERE notificationType = 'Placement'
AND createdAt >= CURRENT_DATE - INTERVAL '7 days';
```
# Stage 4

## Performance Improvements

To improve notification performance:

1. Use database indexes.
2. Fetch notifications using pagination (LIMIT and OFFSET).
3. Cache frequently accessed notifications using Redis.
4. Load notifications only when required (lazy loading).
5. Archive old notifications into another table.
6. Use read replicas for heavy read traffic.

## Trade-offs

| Solution | Advantage | Disadvantage |
|----------|-----------|--------------|
| Indexing | Faster search | More storage |
| Pagination | Faster API | Multiple requests |
| Redis Cache | Very fast | Extra infrastructure |
| Read Replicas | Better scalability | Higher cost |
| Archiving | Smaller active database | More complex queries |

### Recommended Approach

Use:
- Proper indexes
- Pagination
- Redis caching
- Database replication

These techniques provide good performance even with millions of notifications.