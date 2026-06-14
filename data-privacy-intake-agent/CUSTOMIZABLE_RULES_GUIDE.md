# Customizable Rules System - Implementation Complete

## Overview

The Data Privacy Intake Agent now features a fully customizable rules system that allows administrators to manage all rules through a structured database-backed UI, replacing the previous Markdown-only approach.

## What's New

### Backend Features

1. **Database Models**
   - `users` - Admin authentication
   - `checklist_items` - Structured DPA/OTIA checklist rules
   - `screening_questions` - Customizable intake questions
   - `sensitive_keywords` - Data classification keywords
   - `rule_audit_logs` - Complete change history

2. **JWT Authentication**
   - Secure admin access with JWT tokens
   - Password hashing with bcrypt
   - Token-based API protection

3. **RESTful Rules API**
   - Full CRUD operations for all rule types
   - Filtering, sorting, and pagination
   - Bulk import for keywords
   - Reordering support

4. **Dynamic Rule Loading**
   - Agent loads rules from database at runtime
   - Backward compatible with Markdown files
   - Fallback mechanism for resilience

### Frontend Features

1. **Admin Login**
   - Secure authentication
   - Session management
   - Default credentials: `admin` / `admin123`

2. **Structured Rules Management**
   - **Checklist Items Tab**: Add, edit, delete DPA/OTIA items
   - **Screening Questions Tab**: Manage intake questions
   - **Sensitive Keywords Tab**: Categorized keyword management
   - **Audit Logs Tab**: View complete change history
   - **Legacy Tab**: Direct file editing (backward compatible)

3. **Rich UI Features**
   - Inline editing forms
   - Category and status filtering
   - Drag-and-drop reordering (via display_order)
   - Visual status badges
   - Real-time updates

## Installation & Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `python-jose[cryptography]` - JWT handling
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - Form data support

### 2. Environment Variables

Add to your `.env` file:

```bash
# JWT Configuration (IMPORTANT: Change in production!)
JWT_SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# Database (existing)
DATABASE_URL=postgresql://privacy_agent:privacy_agent_pass@localhost:5432/privacy_agent_db

# LLM API (existing)
LLM_API_KEY=your-api-key
LLM_MODEL=gpt-4o-mini
```

### 3. Initialize Database

The database tables will be created automatically on first run:

```bash
cd backend
python main.py
```

Default admin user will be created:
- Username: `admin`
- Password: `admin123`
- **⚠️ IMPORTANT: Change this password after first login!**

### 4. Migrate Existing Rules

To import existing Markdown rules into the database:

```bash
cd backend
python -m scripts.migrate_rules
```

This will:
- Parse `dpa_checklist.md` and `otia_checklist.md`
- Import screening questions from agent config
- Import sensitive keywords
- Create default admin user if needed

**Note:** Run this only once! It creates new records, not updates.

## Usage Guide

### Admin Panel Access

1. Start the backend:
   ```bash
   cd backend
   python main.py
   ```

2. Start the frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. Navigate to Admin Panel (sidebar or URL: `http://localhost:8501/⚙️_Admin_Panel`)

4. Login with credentials:
   - Username: `admin`
   - Password: `admin123`

### Managing Checklist Items

**Add New Item:**
1. Click "➕ Add New Checklist Item" expander
2. Fill in:
   - Category: DPA, OTIA, or GENERAL
   - Item Number: e.g., "1", "2a", "2b"
   - Title: Short checklist item name
   - Description: Detailed explanation
   - Required Documents: What to provide
   - Notes: Additional information
   - Display Order: Position in list
3. Click "Create Item"

**Edit Item:**
1. Click "✏️ Edit" next to any item
2. Modify fields as needed
3. Toggle Active/Inactive status
4. Click "💾 Save Changes"

**Delete Item:**
- Click "🗑️ Delete" (soft delete - sets is_active=false)

**Filtering:**
- Filter by Category: DPA, OTIA, GENERAL, All
- Filter by Status: Active Only, Inactive Only, All

### Managing Screening Questions

**Add New Question:**
1. Click "➕ Add New Question" expander
2. Enter question text
3. Select question type:
   - `yes_no` - Simple yes/no question
   - `multiple_choice` - Options provided
   - `text` - Free text answer
4. Add options if multiple choice (comma-separated)
5. Set display order
6. Click "Create Question"

**Edit/Delete:**
- Same as checklist items
- Questions are displayed in display order

**Best Practices:**
- Keep questions clear and specific
- Use yes/no for simple decisions
- Order questions logically (context → details)
- Start with broad questions, then narrow down

### Managing Sensitive Keywords

**Add New Keyword:**
1. Click "➕ Add New Keyword" expander
2. Enter keyword (e.g., "credit score", "biometric")
3. Select category:
   - `financial` - Banking, payment, credit data
   - `health` - Medical, health records
   - `biometric` - Fingerprint, face recognition
   - `general` - Other personal data
4. Add optional description
5. Click "Create Keyword"

**Viewing:**
- Keywords are grouped by category
- Easy to scan and manage by type

**Bulk Import:**
- API endpoint available: `POST /rules/keywords/import`
- Format: JSON array of keyword objects

### Audit Logs

**View Changes:**
1. Go to Audit Logs tab
2. Filter by:
   - Table name (checklist_items, screening_questions, keywords)
   - Limit (number of entries)
3. View summary table or detailed JSON diffs

**What's Logged:**
- CREATE - New rule added
- UPDATE - Rule modified (shows old vs new values)
- DELETE - Rule soft deleted
- Who changed it (user ID)
- When it was changed (timestamp)

**Use Cases:**
- Compliance auditing
- Debugging rule changes
- Reverting mistakes
- Understanding rule evolution

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user info |
| POST | `/auth/logout` | Logout (client discards token) |

### Checklist Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rules/checklist` | List all checklist items |
| GET | `/rules/checklist/{id}` | Get single item |
| POST | `/rules/checklist` | Create new item |
| PUT | `/rules/checklist/{id}` | Update item |
| DELETE | `/rules/checklist/{id}` | Soft delete item |
| POST | `/rules/checklist/reorder` | Reorder items |

### Screening Questions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rules/questions` | List all questions |
| GET | `/rules/questions/{id}` | Get single question |
| POST | `/rules/questions` | Create new question |
| PUT | `/rules/questions/{id}` | Update question |
| DELETE | `/rules/questions/{id}` | Soft delete question |
| POST | `/rules/questions/reorder` | Reorder questions |

### Sensitive Keywords

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rules/keywords` | List all keywords |
| GET | `/rules/keywords/{id}` | Get single keyword |
| POST | `/rules/keywords` | Create new keyword |
| PUT | `/rules/keywords/{id}` | Update keyword |
| DELETE | `/rules/keywords/{id}` | Soft delete keyword |
| POST | `/rules/keywords/import` | Bulk import keywords |

### Audit Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rules/audit-logs` | List audit logs |

**Query Parameters:**
- `category` - Filter checklist items by DPA/OTIA/GENERAL
- `is_active` - Filter by active status (true/false)
- `table_name` - Filter audit logs by table
- `limit` - Limit number of audit log results

## Architecture

### Data Flow

```
User → Admin Panel UI (Streamlit)
         ↓
      Auth Check (JWT)
         ↓
    Rules API (FastAPI)
         ↓
    CRUD Operations
         ↓
    PostgreSQL Database
         ↓
    Agent Service (loads rules)
         ↓
    LLM Prompt (rules embedded)
```

### Database Schema

**users**
- id (UUID), username, password_hash, is_active
- Authentication and authorization

**checklist_items**
- id (UUID), category (DPA/OTIA/GENERAL), item_number, title
- description, required_documents, notes
- is_active, display_order, created_by
- Structured checklist rules

**screening_questions**
- id (UUID), question_text, question_type (yes_no/multiple_choice/text)
- options (JSON), is_active, display_order
- Dynamic intake questions

**sensitive_keywords**
- id (UUID), keyword, category, description, is_active
- Data classification triggers

**rule_audit_logs**
- id (UUID), table_name, record_id, action (CREATE/UPDATE/DELETE)
- old_value (JSONB), new_value (JSONB), changed_by, changed_at
- Complete change history

### Backward Compatibility

The system maintains backward compatibility:

1. **Markdown Fallback**: If database is empty or fails, agent falls back to Markdown files
2. **Legacy Tab**: Direct file editing still available in Admin Panel
3. **Migration Script**: One-time import from Markdown to database
4. **Privacy Rules**: Complex rule definitions still loaded from `privacy_rules.md`

## Security Considerations

### Production Deployment

**MUST DO:**

1. **Change JWT Secret Key**
   ```bash
   JWT_SECRET_KEY=$(openssl rand -base64 32)
   ```
   Add to production `.env` file

2. **Change Default Admin Password**
   - Login with admin/admin123
   - Change password immediately
   - Or create new admin and delete default

3. **Use HTTPS**
   - Always use HTTPS in production
   - JWT tokens are bearer tokens (vulnerable over HTTP)

4. **Environment Variables**
   - Never commit `.env` files
   - Use secrets management (AWS Secrets, Azure Key Vault, etc.)

5. **Database Security**
   - Use strong database password
   - Restrict database access by IP
   - Regular backups

### Security Features

- ✅ Password hashing with bcrypt (salt rounds: 12)
- ✅ JWT tokens with expiration (default: 24 hours)
- ✅ Soft deletes (data not physically removed)
- ✅ Audit logging of all changes
- ✅ CORS protection in FastAPI
- ✅ SQL injection protection (SQLAlchemy ORM)

## Troubleshooting

### Cannot Login to Admin Panel

**Problem:** Login fails with "Incorrect username or password"

**Solutions:**
1. Check default credentials: `admin` / `admin123`
2. Verify backend is running: `http://localhost:8000/health`
3. Check database connection
4. Run migration script to create default user:
   ```bash
   python -m scripts.migrate_rules
   ```

### Rules Not Loading in Agent

**Problem:** Agent not using database rules

**Solutions:**
1. Check database has rules (use Admin Panel)
2. Verify database session passed to agent service
3. Check agent service logs for errors
4. Ensure backward compatibility: Markdown files still exist as fallback

### Migration Script Fails

**Problem:** `python -m scripts.migrate_rules` fails

**Solutions:**
1. Ensure backend dependencies installed: `pip install -r requirements.txt`
2. Check database connection in `.env`
3. Verify markdown files exist in `backend/knowledge/`
4. Check Python path includes backend directory

### Admin Panel Shows No Data

**Problem:** Admin panel loads but shows empty lists

**Solutions:**
1. Run migration script if first time setup
2. Check API connectivity: `http://localhost:8000/rules/checklist`
3. Verify authentication (JWT token valid)
4. Check browser console for JavaScript errors

### API Returns 401 Unauthorized

**Problem:** API requests return 401 even after login

**Solutions:**
1. Check JWT token in session state
2. Token may have expired (default: 24 hours)
3. Logout and login again
4. Check `JWT_SECRET_KEY` is consistent (don't change it!)

## Performance Considerations

### Database Queries

- Indexes on: `category`, `is_active`, `display_order`, `keyword`
- Use filters to reduce result sets
- Pagination available for audit logs

### Agent Performance

- Rules loaded from database on each request
- Consider caching for high-traffic deployments
- Fallback to cached version if DB unavailable

### Recommendations

- **Small datasets (<1000 rules)**: Current implementation is fine
- **Large datasets (>1000 rules)**: Consider caching layer (Redis)
- **High traffic**: Use connection pooling (already configured)

## Future Enhancements

Potential improvements for future versions:

1. **User Management UI**
   - Create/edit/delete admin users
   - Role-based access control (Admin, Editor, Viewer)
   - Password change form in UI

2. **Advanced Features**
   - Rule versioning and rollback
   - Export rules to JSON/CSV
   - Import rules from external sources
   - Approval workflow for rule changes

3. **AI Improvements**
   - Rule effectiveness analytics
   - Suggest new rules based on cases
   - Automated rule optimization

4. **Integration**
   - Webhook notifications on rule changes
   - Slack/Teams integration
   - API for external rule management

## Support

For issues or questions:

1. Check troubleshooting section above
2. Review audit logs for clues
3. Check backend logs: `docker logs privacy-backend`
4. Verify database state: `psql` into database

## Migration Checklist

If upgrading from v1.0 (Markdown-only) to v2.0 (Database):

- [ ] Backup existing Markdown files
- [ ] Install new Python dependencies
- [ ] Update `.env` with JWT_SECRET_KEY
- [ ] Start backend (creates new tables)
- [ ] Run migration script to import rules
- [ ] Test Admin Panel login
- [ ] Verify rules loaded in agent
- [ ] Change default admin password
- [ ] Test creating/editing rules
- [ ] Monitor audit logs

---

**Congratulations!** You now have a fully customizable rules system for your Data Privacy Intake Agent. 🎉
