# Pomodoro Mobile App Project Plan

**Stack:**
- Frontend: React Native (JavaScript, CSS-in-JS)
- Backend: Flask (Python)
- Database: SQLite (local storage; can migrate to MySQL/cloud later)
- Authentication: JWT or session-based
- Deployment: Local for development; cloud server (Heroku, AWS, DigitalOcean, or PythonAnywhere) for future updates

---

## Step-by-Step Project Plan

### 1. Initial Setup
- Install Node.js, npm, and React Native CLI
- Install Python and Flask
- Set up SQLite (comes built-in with Python)
- Set up Git for version control

### 2. Design Database Schema

Below is a suggested schema for the Pomodoro app using SQLite:

#### Users Table
| Column        | Type     | Constraints                |
|--------------|----------|----------------------------|
| id           | Integer  | Primary Key, Auto-increment|
| username     | String   | Unique, Not Null           |
| email        | String   | Unique, Not Null           |
| password_hash| String   | Not Null                   |
| created_at   | DateTime | Default: current timestamp |

#### Activities Table
| Column        | Type     | Constraints                |
|--------------|----------|----------------------------|
| id           | Integer  | Primary Key, Auto-increment|
| user_id      | Integer  | Foreign Key (Users.id)     |
| name         | String   | Not Null                   |
| color        | String   | (optional, for UI)         |
| created_at   | DateTime | Default: current timestamp |

#### PomodoroSessions Table
| Column        | Type     | Constraints                |
|--------------|----------|----------------------------|
| id           | Integer  | Primary Key, Auto-increment|
| user_id      | Integer  | Foreign Key (Users.id)     |
| activity_id  | Integer  | Foreign Key (Activities.id)|
| start_time   | DateTime | Not Null                   |
| end_time     | DateTime | Not Null                   |
| duration     | Integer  | (seconds or minutes)       |

#### Streaks Table (Optional)
| Column        | Type     | Constraints                |
|--------------|----------|----------------------------|
| id           | Integer  | Primary Key, Auto-increment|
| user_id      | Integer  | Foreign Key (Users.id)     |
| activity_id  | Integer  | Foreign Key (Activities.id)|
| date         | Date     | Not Null                   |
| streak_count | Integer  | Not Null                   |

**Notes:**
- You can calculate streaks and analytics on the fly from PomodoroSessions, but a Streaks table can make it easier to track daily progress.
- All foreign keys should be set up with ON DELETE CASCADE for data integrity.
- Add indexes on user_id and activity_id for faster queries.
- You can expand the schema with more fields (e.g., notes, tags) as needed.

### 3. Build Flask Backend
- Set up Flask project structure
- Connect Flask to SQLite database
- Implement user authentication (register, login, JWT/session)
- Create REST API endpoints:
  - User registration/login
  - CRUD for activities
  - Start/end Pomodoro session
  - Fetch analytics/streaks
- Test endpoints with Postman/Insomnia

### 4. Build React Native Frontend
- Initialize React Native project
- Set up navigation (e.g., React Navigation)
- Create screens:
  - Login/Register
  - Activity selection/creation
  - Pomodoro timer
  - Analytics/streaks
- Connect frontend to backend API (using fetch/axios)
- Handle authentication tokens
- Display and update user data

### 5. Implement Data Sync & Backup (Future Enhancement)
- For now, all data is stored locally via SQLite on the backend
- When ready to add cloud sync, migrate backend to use MySQL or another cloud database
- On sign-in, fetch user data from backend
- On sign-out, clear local data
- Handle offline mode (optional: cache data locally and sync when online)

### 6. Testing
- Test all features on Android emulator/device
- Test API security and error handling
- Test data sync across multiple devices (when cloud sync is added)

### 7. Deployment
- Deploy Flask backend locally for development
- For future updates, deploy backend to cloud server
- Set up environment variables and secure credentials
- Update React Native app to use production backend URL when cloud deployed
- Build and package APK for Android

### 8. Future Enhancements (Optional)
- Add notifications/reminders
- Add social/sharing features
- Add iOS support (if desired)
- Improve UI/UX
- Migrate to cloud database for cross-device sync

---

**Tips:**
- Commit code regularly and use branches for features.
- Document API endpoints and app features.
- Use environment variables for sensitive data.
- Refer to official documentation for each technology as needed.
- When ready, migrating from SQLite to MySQL is straightforward with Flask ORM libraries like SQLAlchemy. 