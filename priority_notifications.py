from datetime import datetime

notifications = [
    {
        "ID": 1,
        "Type": "Placement",
        "Message": "Google hiring drive",
        "Timestamp": "2026-06-28T10:30:00",
        "isRead": False
    },
    {
        "ID": 2,
        "Type": "Event",
        "Message": "Hackathon tomorrow",
        "Timestamp": "2026-06-29T09:00:00",
        "isRead": False
    },
    {
        "ID": 3,
        "Type": "Result",
        "Message": "Semester result declared",
        "Timestamp": "2026-06-29T08:30:00",
        "isRead": False
    },
    {
        "ID": 4,
        "Type": "Placement",
        "Message": "Microsoft internship",
        "Timestamp": "2026-06-29T11:15:00",
        "isRead": False
    },
    {
        "ID": 5,
        "Type": "Event",
        "Message": "Workshop on AI",
        "Timestamp": "2026-06-27T15:20:00",
        "isRead": True
    },
    {
        "ID": 6,
        "Type": "Placement",
        "Message": "Amazon recruitment",
        "Timestamp": "2026-06-29T10:45:00",
        "isRead": False
    }
]

priority = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

unread = [n for n in notifications if not n["isRead"]]

sorted_notifications = sorted(
    unread,
    key=lambda x: (
        priority[x["Type"]],
        datetime.fromisoformat(x["Timestamp"])
    ),
    reverse=True
)

print("=" * 60)
print("TOP PRIORITY NOTIFICATIONS")
print("=" * 60)

for i, n in enumerate(sorted_notifications, start=1):
    print(f"{i}. {n['Type']}")
    print(f"   ID: {n['ID']}")
    print(f"   Message: {n['Message']}")
    print(f"   Time: {n['Timestamp']}")
    print("-" * 60)