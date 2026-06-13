# PostgreSQL Migration Guide

## 🎉 Successfully Migrated to PostgreSQL!

The application has been upgraded from **JSON file storage** to **PostgreSQL database**.

---

## 📊 What Changed?

### Before (v1.0):
```
backend/config/
├── agent_config.json
├── settings.json
└── sessions/
    ├── uuid-1.json
    └── uuid-2.json
```

### After (v2.0):
```
PostgreSQL Database:
├── sessions table       # Chat sessions with messages
├── settings table       # App settings (model, instructions)
└── agent_configs table  # Agent configuration
```

---

## 🏗️ Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    messages JSON NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Settings Table
```sql
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Agent Configs Table
```sql
CREATE TABLE agent_configs (
    id SERIAL PRIMARY KEY,
    config_data JSON NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🚀 How to Start

### Step 1: Stop Current Services

```bash
cd E:\project\data-privacy-intake-agent
docker-compose down
```

### Step 2: Start with PostgreSQL

```bash
docker-compose up --build -d
```

This will:
- ✅ Start PostgreSQL container (port 5432)
- ✅ Start Backend container (port 8000)
- ✅ Start Frontend container (port 8501)
- ✅ Auto-create all database tables
- ✅ Initialize default settings

### Step 3: Verify Database

Check if PostgreSQL is running:
```bash
docker-compose ps
```

Expected output:
```
NAME                       STATUS    PORTS
privacy-agent-postgres     Up        0.0.0.0:5432->5432/tcp
privacy-agent-backend      Up        0.0.0.0:8000->8000/tcp
privacy-agent-frontend     Up        0.0.0.0:8501->8501/tcp
```

### Step 4: Test the Application

Open browser:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

---

## 🔧 Configuration

### Environment Variables

PostgreSQL credentials are in `docker-compose.yml`:

```yaml
postgres:
  environment:
    - POSTGRES_USER=privacy_agent
    - POSTGRES_PASSWORD=privacy_agent_pass
    - POSTGRES_DB=privacy_agent_db
```

Backend automatically connects via:
```
DATABASE_URL=postgresql://privacy_agent:privacy_agent_pass@postgres:5432/privacy_agent_db
```

### Change PostgreSQL Password

Edit `docker-compose.yml`:
```yaml
postgres:
  environment:
    - POSTGRES_PASSWORD=your_secure_password
    
backend:
  environment:
    - DATABASE_URL=postgresql://privacy_agent:your_secure_password@postgres:5432/privacy_agent_db
```

Then rebuild:
```bash
docker-compose down
docker-compose up --build -d
```

---

## 🗄️ Database Management

### Connect to PostgreSQL

**Using Docker:**
```bash
docker exec -it privacy-agent-postgres psql -U privacy_agent -d privacy_agent_db
```

**Using local psql:**
```bash
psql -h localhost -p 5432 -U privacy_agent -d privacy_agent_db
```
Password: `privacy_agent_pass`

### Useful SQL Commands

**List all sessions:**
```sql
SELECT id, name, created_at, 
       jsonb_array_length(messages::jsonb) as msg_count 
FROM sessions 
ORDER BY updated_at DESC;
```

**View settings:**
```sql
SELECT * FROM settings;
```

**Check agent config:**
```sql
SELECT config_data FROM agent_configs ORDER BY id DESC LIMIT 1;
```

**Delete old sessions:**
```sql
DELETE FROM sessions WHERE updated_at < NOW() - INTERVAL '30 days';
```

---

## 💾 Backup & Restore

### Backup Database

```bash
# Backup all data
docker exec privacy-agent-postgres pg_dump -U privacy_agent privacy_agent_db > backup.sql

# Backup specific table
docker exec privacy-agent-postgres pg_dump -U privacy_agent -t sessions privacy_agent_db > sessions_backup.sql
```

### Restore Database

```bash
# Restore from backup
docker exec -i privacy-agent-postgres psql -U privacy_agent privacy_agent_db < backup.sql
```

---

## 🔄 Migration from Old JSON Files

If you had existing sessions in JSON files:

### Option 1: Manual Import (Small data)
1. Copy important conversations manually via UI
2. Old files remain in `backend/config/sessions/` (ignored)

### Option 2: Script Import (Large data)
Create `migrate_json_to_postgres.py`:
```python
import json
import psycopg2
from pathlib import Path

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="privacy_agent",
    password="privacy_agent_pass",
    database="privacy_agent_db"
)

sessions_dir = Path("backend/config/sessions")
for file in sessions_dir.glob("*.json"):
    with open(file) as f:
        data = json.load(f)
    
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO sessions (id, name, messages, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['id'],
            data['name'],
            json.dumps(data['messages']),
            data['created_at'],
            data['updated_at']
        ))

conn.commit()
conn.close()
```

Run: `python migrate_json_to_postgres.py`

---

## 🐛 Troubleshooting

### Backend won't start

**Error:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution:**
```bash
# Check if postgres is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart postgres
docker-compose restart postgres

# Wait for postgres health check
docker-compose up --build -d
```

### Database tables not created

**Error:** `relation "sessions" does not exist`

**Solution:**
```bash
# Recreate backend (will auto-create tables)
docker-compose down backend
docker-compose up --build -d backend
```

### Port 5432 already in use

**Error:** `bind: address already in use`

**Solution:**
```bash
# Stop local postgres if running
# Windows:
net stop postgresql

# Or change port in docker-compose.yml:
ports:
  - "5433:5432"  # Use 5433 on host
```

### Lost all sessions

**Solution:** Check if postgres volume exists:
```bash
docker volume ls | grep postgres
docker volume inspect data-privacy-intake-agent_postgres_data
```

If volume deleted, data is lost (restore from backup).

---

## 📈 Benefits of PostgreSQL

| Feature | JSON Files | PostgreSQL |
|---------|-----------|------------|
| **Performance** | Slow (file I/O) | Fast (indexed queries) |
| **Scalability** | Limited | High |
| **Concurrent access** | Risky | Safe (ACID) |
| **Search** | No | SQL queries |
| **Backup** | Copy files | pg_dump |
| **Production ready** | No | Yes |

---

## 🔐 Security Recommendations

For production:

1. **Change default password:**
   ```yaml
   POSTGRES_PASSWORD=your_strong_password_here
   ```

2. **Use environment variables:**
   ```yaml
   POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
   ```

3. **Restrict access:**
   ```yaml
   ports:
     - "127.0.0.1:5432:5432"  # Only localhost
   ```

4. **Enable SSL:**
   ```python
   DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
   ```

---

## 📝 API Endpoints (Unchanged)

All API endpoints remain the same:
- `GET /sessions` - List sessions
- `POST /sessions` - Create session
- `GET /sessions/{id}` - Get session
- `PUT /sessions/{id}` - Update session
- `DELETE /sessions/{id}` - Delete session
- `GET /settings` - Get settings
- `PUT /settings` - Update settings

Frontend code **no changes needed** - it works automatically!

---

## ✅ Verification Checklist

After migration, verify:

- [ ] PostgreSQL container running: `docker-compose ps`
- [ ] Backend connects to DB: Check logs for "Database initialized"
- [ ] Create new chat session in UI
- [ ] Session persists after page refresh
- [ ] Settings save correctly
- [ ] Export to Excel/MD works
- [ ] No error logs: `docker-compose logs -f backend`

---

## 📞 Need Help?

**Check logs:**
```bash
# All services
docker-compose logs -f

# Only backend
docker-compose logs -f backend

# Only postgres
docker-compose logs -f postgres
```

**Access database directly:**
```bash
docker exec -it privacy-agent-postgres psql -U privacy_agent -d privacy_agent_db
```

---

**Migration completed successfully! 🎉**

**Version:** 2.0.0  
**Database:** PostgreSQL 15  
**Status:** Production-ready
