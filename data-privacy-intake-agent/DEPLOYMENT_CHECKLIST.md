# Deployment Checklist - Customizable Rules System

Use this checklist to ensure proper deployment and security.

## Pre-Deployment

### Development Environment

- [ ] Python 3.11+ installed
- [ ] PostgreSQL database running
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (Streamlit)
- [ ] `.env` file created with all required variables

### Environment Variables

- [ ] `DATABASE_URL` configured correctly
- [ ] `JWT_SECRET_KEY` set (use `openssl rand -base64 32`)
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` configured (default: 1440)
- [ ] `LLM_API_KEY` configured
- [ ] `LLM_MODEL` configured
- [ ] `LLM_BASE_URL` configured (if not OpenAI)

### Database Setup

- [ ] PostgreSQL server is running
- [ ] Database created (`privacy_agent_db`)
- [ ] Database user created with permissions
- [ ] Connection string tested

### Initial Setup

- [ ] Backend started successfully (`python main.py`)
- [ ] Database tables created automatically
- [ ] Default admin user created
- [ ] Migration script run (`python -m scripts.migrate_rules`)
- [ ] Rules imported successfully
- [ ] Frontend started successfully (`streamlit run app.py`)
- [ ] Admin Panel login works

## Security Checklist

### Development

- [ ] Default admin password is `admin123` (acceptable for dev)
- [ ] JWT_SECRET_KEY can be simple for local testing
- [ ] HTTP is acceptable for localhost

### Production

- [ ] **CRITICAL**: JWT_SECRET_KEY changed to cryptographically random string
- [ ] **CRITICAL**: Default admin password changed or new admin created
- [ ] **CRITICAL**: HTTPS enabled for all endpoints
- [ ] Database credentials are strong
- [ ] Database access restricted by IP/firewall
- [ ] CORS origins restricted (not `allow_origins=["*"]`)
- [ ] Environment variables not committed to git
- [ ] `.env` file in `.gitignore`
- [ ] Secrets stored in secure vault (AWS Secrets, Azure Key Vault, etc.)
- [ ] Regular database backups configured
- [ ] Backup retention policy defined
- [ ] Disaster recovery plan documented

### Additional Security

- [ ] Rate limiting configured (if high traffic)
- [ ] Monitoring and alerting set up
- [ ] Logs reviewed regularly
- [ ] Audit logs monitored for suspicious activity
- [ ] Failed login attempts tracked
- [ ] Password complexity policy enforced
- [ ] Token expiration appropriate for use case
- [ ] Consider 2FA for admin access (future enhancement)

## Functionality Testing

### Authentication

- [ ] Can login with valid credentials
- [ ] Cannot login with invalid credentials
- [ ] JWT token expires after configured time
- [ ] Protected endpoints reject unauthenticated requests
- [ ] Logout works correctly

### Checklist Items

- [ ] Can view all checklist items
- [ ] Can filter by category (DPA/OTIA/GENERAL)
- [ ] Can filter by status (Active/Inactive)
- [ ] Can create new checklist item
- [ ] Can edit existing checklist item
- [ ] Can delete checklist item (soft delete)
- [ ] Display order works correctly
- [ ] Changes appear immediately

### Screening Questions

- [ ] Can view all questions
- [ ] Can create new question
- [ ] Can edit existing question
- [ ] Can delete question
- [ ] Different question types work (yes_no, multiple_choice, text)
- [ ] Display order works correctly

### Sensitive Keywords

- [ ] Can view all keywords
- [ ] Keywords grouped by category
- [ ] Can create new keyword
- [ ] Can edit existing keyword
- [ ] Can delete keyword
- [ ] Categories work correctly

### Audit Logs

- [ ] Audit logs capture CREATE actions
- [ ] Audit logs capture UPDATE actions
- [ ] Audit logs capture DELETE actions
- [ ] Old vs new values shown correctly
- [ ] User attribution works
- [ ] Timestamps accurate
- [ ] Filtering works (by table, limit)

### Agent Integration

- [ ] Agent loads rules from database
- [ ] Agent uses latest rules immediately after changes
- [ ] Agent falls back to Markdown if database fails
- [ ] Chat functionality works with new rules
- [ ] Generated output includes database rules

## Performance Testing

### Database

- [ ] Query performance acceptable (<100ms for most queries)
- [ ] Indexes created on key columns
- [ ] Connection pooling configured
- [ ] No connection leaks

### API

- [ ] Endpoints respond in <500ms
- [ ] No timeout errors
- [ ] Error handling works correctly
- [ ] Large result sets paginated

### Frontend

- [ ] Admin Panel loads in <3 seconds
- [ ] No JavaScript errors in console
- [ ] Form submissions responsive
- [ ] No UI lag when editing

## Data Validation

### Initial Migration

- [ ] DPA checklist items imported (expected: ~10-13 items)
- [ ] OTIA checklist items imported (expected: ~14 items)
- [ ] Screening questions imported (expected: 7 questions)
- [ ] Sensitive keywords imported (expected: 10+ keywords)
- [ ] No duplicate items
- [ ] All fields populated correctly
- [ ] Display order logical

### Data Integrity

- [ ] Foreign key constraints work
- [ ] Soft deletes don't break relations
- [ ] UUID generation works
- [ ] Timestamps auto-populate
- [ ] Enum values validated
- [ ] Required fields enforced

## Documentation

- [ ] `QUICK_START.md` reviewed
- [ ] `CUSTOMIZABLE_RULES_GUIDE.md` reviewed
- [ ] `IMPLEMENTATION_SUMMARY.md` reviewed
- [ ] Environment variables documented
- [ ] Backup procedures documented
- [ ] Disaster recovery plan documented
- [ ] User training materials prepared (if needed)
- [ ] API documentation accessible
- [ ] Admin credentials documented securely

## Backup & Recovery

- [ ] Database backup procedure tested
- [ ] Backup restoration tested
- [ ] Backup schedule configured
- [ ] Backup storage secured
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined
- [ ] Disaster recovery runbook created

## Monitoring & Maintenance

- [ ] Application logs configured
- [ ] Error tracking set up (Sentry, etc.)
- [ ] Performance monitoring configured (APM)
- [ ] Database monitoring configured
- [ ] Disk space monitoring configured
- [ ] Alerting thresholds defined
- [ ] On-call procedures documented
- [ ] Maintenance windows scheduled
- [ ] Update procedures documented

## User Acceptance

- [ ] Admin users trained on new panel
- [ ] Users can login successfully
- [ ] Users can perform CRUD operations
- [ ] Users understand audit logs
- [ ] Users comfortable with UI
- [ ] Feedback collected
- [ ] Issues documented
- [ ] Support contact provided

## Go-Live Checklist

### Pre-Launch (1 week before)

- [ ] All above sections completed
- [ ] Staging environment tested thoroughly
- [ ] Performance testing passed
- [ ] Security review completed
- [ ] Backup procedures tested
- [ ] Rollback plan documented
- [ ] Team briefed on launch

### Launch Day

- [ ] Final backup taken
- [ ] Monitoring active
- [ ] Support team ready
- [ ] Rollback plan accessible
- [ ] Deploy to production
- [ ] Smoke tests passed
- [ ] Users notified
- [ ] Documentation published

### Post-Launch (1 week after)

- [ ] Monitor error rates
- [ ] Monitor performance
- [ ] Review audit logs
- [ ] Collect user feedback
- [ ] Address critical issues
- [ ] Update documentation
- [ ] Team retrospective

## Rollback Plan

If critical issues arise:

1. [ ] Communicate issue to stakeholders
2. [ ] Stop accepting new changes in Admin Panel
3. [ ] Backup current database
4. [ ] Restore previous database backup
5. [ ] Restart backend with previous code
6. [ ] Verify functionality
7. [ ] Communicate resolution
8. [ ] Investigate root cause
9. [ ] Fix and retest
10. [ ] Plan re-deployment

## Sign-Off

**Deployed By:** _____________________ **Date:** _____________________

**Reviewed By:** _____________________ **Date:** _____________________

**Approved By:** _____________________ **Date:** _____________________

---

## Notes

Record any issues, deviations, or special circumstances:

_____________________________________________________________________________

_____________________________________________________________________________

_____________________________________________________________________________

---

**Status: [ ] Ready for Deployment [ ] Deployed [ ] Verified**
