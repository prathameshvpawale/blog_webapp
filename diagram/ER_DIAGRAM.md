# ER Diagram - Django Blog Project

## Entity-Relationship Diagram (Text-Based)

```
┌─────────────────────────────────┐
│          User (Django)          │
├─────────────────────────────────┤
│ id (PK)                         │
│ username (unique)               │
│ email                           │
│ password (hashed)               │
│ first_name                      │
│ last_name                       │
│ is_staff                        │
│ is_active                       │
│ date_joined                     │
└─────────────────────────────────┘
        ▲           ▲
        │           │
        │1          │1
        │           │
   (1:N)│      (1:1)│
        │           │
        │           │
┌───────┴─────────────────────┐   ┌──────────────────────────┐
│       Post (blog app)        │   │   Profile (users app)    │
├──────────────────────────────┤   ├──────────────────────────┤
│ id (PK)                      │   │ id (PK)                  │
│ title (max 100 chars)        │   │ user_id (FK, unique)     │
│ content (FroalaField)        │   │ image (profile pic)      │
│ image (ImageField, optional) │   │                          │
│ date_posted (datetime)       │   │ Relationships:           │
│ author_id (FK to User)       │   │ - OneToOne ↔ User        │
│                              │   │                          │
│ Relationships:               │   └──────────────────────────┘
│ - ForeignKey → User (author) │
└──────────────────────────────┘
```

## Detailed Schema

### 1. **User** (Django Auth - django.contrib.auth)
**Type:** Django Built-in Model  
**Primary Key:** id (auto-increment)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-incrementing primary key |
| username | CharField | Unique, max 150 | User login name |
| email | EmailField | Blank | User email address |
| password | CharField | - | Hashed password |
| first_name | CharField | Blank, max 30 | User's first name |
| last_name | CharField | Blank, max 30 | User's last name |
| is_staff | BooleanField | Default False | Admin access flag |
| is_active | BooleanField | Default True | Account active status |
| date_joined | DateTimeField | - | Account creation time |

---

### 2. **Post** (blog app)
**Type:** Custom Model  
**Primary Key:** id (auto-increment)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-incrementing primary key |
| title | CharField | max 100 | Blog post title |
| content | FroalaField | - | Rich text editor content |
| image | ImageField | Null, Blank | Post featured image (optional) |
| date_posted | DateTimeField | Default now | Post creation timestamp |
| author_id | ForeignKey | FK to User | Post author (Many:One) |

**Relationships:**
- `author` → **User** (ForeignKey, Many-to-One)
  - Cascade delete: If User deleted, all their Posts are deleted
  - Reverse relation: `user.post_set.all()` to get all posts by user

---

### 3. **Profile** (users app)
**Type:** Custom Model  
**Primary Key:** id (auto-increment)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | PK | Auto-incrementing primary key |
| user_id | OneToOneField | FK to User, unique | One profile per user |
| image | ImageField | Default "profile.jpg" | User profile picture |

**Relationships:**
- `user` → **User** (OneToOneField, One-to-One)
  - Cascade delete: If User deleted, Profile is deleted
  - Reverse relation: `user.profile` to access user's profile

---

## Relationships Summary

| Relationship | Type | From | To | Cardinality | Cascade |
|--------------|------|------|-----|-------------|---------|
| author | ForeignKey | Post | User | N:1 | CASCADE |
| user | OneToOneField | Profile | User | 1:1 | CASCADE |

---

## Query Examples

### Get all posts by a user:
```python
user = User.objects.get(username='pratham')
posts = user.post_set.all()  # or Post.objects.filter(author=user)
```

### Get user's profile:
```python
user = User.objects.get(username='pratham')
profile = user.profile
```

### Get post author and profile:
```python
post = Post.objects.get(pk=1)
author = post.author  # User object
profile = post.author.profile  # Profile object
```

### Create new post:
```python
from django.utils import timezone
post = Post.objects.create(
    title='My First Post',
    content='Content here',
    author=request.user,
    date_posted=timezone.now()
)
```

---

## Database Tables Generated

When you run `python manage.py migrate`, Django creates:

1. `auth_user` — User accounts
2. `blog_post` — Blog posts
3. `users_profile` — User profiles

**Foreign Keys:**
- `blog_post.author_id` → `auth_user.id`
- `users_profile.user_id` → `auth_user.id` (UNIQUE)
