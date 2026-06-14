# Quick Start Guide - Customizable Rules System

Get the customizable rules system up and running in 5 minutes!

## Prerequisites

- Python 3.11+
- PostgreSQL database running
- Existing Data Privacy Intake Agent installation

## Step 1: Install New Dependencies (1 min)

```bash
cd backend
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 python-multipart==0.0.6
```

## Step 2: Configure Environment Variables (1 min)

Add to your `backend/.env` file:

```bash
# Generate a secret key (run in terminal):
# openssl rand -base64 32

JWT_SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

Keep existing DATABASE_URL and LLM settings.

## Step 3: Start Backend (1 min)

```bash
cd backend
python main.py
```

The backend will:
- ✅ Create new database tables automatically
- ✅ Create default admin user (username: `admin`, password: `admin123`)
- ✅ Initialize default settings

Look for success message:
```
INFO:     Application startup complete.
```

## Step 4: Migrate Existing Rules (1 min)

Open a new terminal:

```bash
cd backend
python -m scripts.migrate_rules
```

When prompted, type `yes` to confirm.

The script will:
- ✅ Import DPA checklist items from Markdown
- ✅ Import OTIA checklist items from Markdown
- ✅ Import screening questions from config
- ✅ Import sensitive keywords from config

Look for success message:
```
✓ Migration completed successfully!
```

## Step 5: Start Frontend & Login (1 min)

```bash
cd frontend
streamlit run app.py
```

1. Navigate to **Admin Panel** (in sidebar or top menu)
2. Login with:
   - Username: `admin`
   - Password: `admin123`

## Verification

You should now see:

✅ **Checklist Items Tab**: ~10-13 DPA items + ~14 OTIA items
✅ **Screening Questions Tab**: 7 default questions
✅ **Sensitive Keywords Tab**: 10+ keywords grouped by category
✅ **Audit Logs Tab**: Migration events

## Quick Tour

### Try These Actions:

1. **Edit a Checklist Item**
   - Go to Checklist Items tab
   - Click "✏️ Edit" on any item
   - Change the title or description
   - Click "💾 Save Changes"
   - Check Audit Logs tab to see your change logged

2. **Add a Screening Question**
   - Go to Screening Questions tab
   - Click "➕ Add New Question"
   - Enter: "Có yêu cầu Security review không?"
   - Type: yes_no
   - Click "Create Question"

3. **Add a Sensitive Keyword**
   - Go to Sensitive Keywords tab
   - Click "➕ Add New Keyword"
   - Enter: "passport number"
   - Category: general
   - Click "Create Keyword"

4. **View Change History**
   - Go to Audit Logs tab
   - See all your changes tracked
   - View old vs new values

## Test the Agent

1. Go back to main Chat interface (click "🏠 Back to Chat")
2. Start a new chat
3. Ask: "Tôi muốn chia sẻ dữ liệu khách hàng cho đối tác ABC ở Việt Nam"
4. The agent will use your database rules!

## Important Security Note

⚠️ **CHANGE THE DEFAULT PASSWORD!**

The default admin password (`admin123`) is for initial setup only.

**To change (recommended):**
1. Create a new admin user via API or database
2. Delete the default admin user
3. Or implement password change UI (future enhancement)

**Production deployment:**
- Use a strong JWT_SECRET_KEY (32+ random bytes)
- Use HTTPS
- Strong admin password
- Regular backups

## Common Issues

### Issue: "Module not found"
**Solution:** Make sure you're in the right directory and installed dependencies

### Issue: "Could not connect to database"
**Solution:** Check your DATABASE_URL in .env and ensure PostgreSQL is running

### Issue: Migration script shows "Already exists" errors
**Solution:** This is normal if running migration twice. Data is already imported.

### Issue: Login fails
**Solution:** 
- Check backend is running (`http://localhost:8000/health`)
- Try default credentials: admin / admin123
- Check browser console for errors

### Issue: Rules not showing in Admin Panel
**Solution:**
- Verify you ran the migration script
- Check API endpoint: `http://localhost:8000/rules/checklist`
- Clear browser cache and reload

## What's Next?

Now that the system is running, you can:

- ✅ Customize checklist items for your organization
- ✅ Add more screening questions
- ✅ Build your keyword library
- ✅ Monitor all changes via audit logs
- ✅ Train users on the Admin Panel

## Full Documentation

For detailed documentation, see:
- [`CUSTOMIZABLE_RULES_GUIDE.md`](CUSTOMIZABLE_RULES_GUIDE.md) - Complete usage guide
- [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md) - Technical details

## Need Help?

1. Check the troubleshooting section in `CUSTOMIZABLE_RULES_GUIDE.md`
2. Review audit logs for clues
3. Check backend logs for error messages
4. Verify database state

---

**Congratulations!** 🎉 Your customizable rules system is now live!

You can now manage all privacy rules through a user-friendly UI without touching code or Markdown files.
