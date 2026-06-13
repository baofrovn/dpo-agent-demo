# Admin Panel Guide

## 🎉 New Feature: Web-based Agent Configuration Editor

Bây giờ bạn có thể **edit prompts, knowledge base, và skills** trực tiếp qua web UI - không cần vào source code!

---

## 🚀 How to Access

### From Chat Page:
1. Mở sidebar
2. Scroll xuống dưới cùng
3. Click button **"⚙️ Admin Panel"**

### Direct URL:
```
http://localhost:8501/⚙️_Admin_Panel
```

---

## 📋 Features

### 1. **System Prompt Editor** 📝

Edit main system prompt của agent:

**What it controls:**
- Vai trò của agent (Data Privacy Intake Assistant)
- Cách agent trả lời
- Output format (markdown structure)
- Tone và style

**How to use:**
1. Go to **"📝 System Prompt"** tab
2. Edit content trong text area
3. Click **"💾 Save"**
4. Changes có hiệu lực ngay lập tức!

**Example edits:**
```markdown
# Before
You are a helpful Data Privacy assistant.

# After
You are a STRICT Data Privacy compliance officer.
Always prioritize security and legal requirements.
```

---

### 2. **Knowledge Base Editor** 📚

Edit 3 knowledge files:

#### **privacy_rules.md**
- Định nghĩa dữ liệu cá nhân
- Sensitive personal data
- Ví dụ về từng loại data

**Use case:** Thêm/sửa definitions theo regulations của công ty

#### **dpa_checklist.md**
- Checklist cho domestic data sharing
- Required documents
- DPA requirements

**Use case:** Customize checklist theo process nội bộ

#### **otia_checklist.md**
- Checklist cho cross-border transfer
- OTIA requirements
- Country-specific rules

**Use case:** Thêm requirements cho các country mới

**How to use:**
1. Go to **"📚 Knowledge Base"** tab
2. Select file từ dropdown
3. Edit content
4. Click **"💾 Save Changes"**

---

### 3. **Skills Editor** 🎯

Edit 7 agent skills:

| Skill | Purpose |
|-------|---------|
| **intake_skill.md** | Trích xuất information từ user input |
| **privacy_classification_skill.md** | Phân loại personal data vs sensitive data |
| **transfer_classification_skill.md** | Domestic vs cross-border classification |
| **checklist_generation_skill.md** | Generate checklist dựa trên case type |
| **data_flow_generation_skill.md** | Create mermaid diagram |
| **privacy_summary_skill.md** | Generate executive summary |
| **email_generation_skill.md** | Draft follow-up email |

**How to use:**
1. Go to **"🎯 Skills"** tab
2. Select skill từ dropdown
3. Edit instructions
4. Click **"💾 Save Changes"**

**Example edit:**
```markdown
# In email_generation_skill.md

# Before
Use polite tone.

# After
Use VERY formal tone.
Address as "Kính gửi Anh/Chị".
End with "Trân trọng cảm ơn".
```

---

## 🔄 How Changes Take Effect

### Immediate (No restart needed):
- ✅ System Prompt changes
- ✅ Knowledge Base edits
- ✅ Skills modifications

### On next message:
- Agent will use updated prompts/knowledge/skills
- No need to restart containers
- No need to reload page

### Test changes:
1. Make edit in Admin Panel
2. Click Save
3. Go back to Chat page
4. Send a new message
5. Observe behavior changes

---

## 💡 Use Cases

### 1. **Customize for Your Company**

Edit company-specific info:
```markdown
# In dpa_checklist.md
Add:
- Contact legal team at legal@yourcompany.com
- Use internal form: https://forms.yourcompany.com/dpa
```

### 2. **Add New Regulations**

Update for new laws:
```markdown
# In privacy_rules.md
Add section:
## Vietnam PDPA 2024 Updates
- New consent requirements
- Data breach notification within 72h
```

### 3. **Change Agent Tone**

Make it more strict/casual:
```markdown
# In system_prompt.md
Add:
- Always use formal Vietnamese
- Never use emojis
- Highlight risks in RED
```

### 4. **Add New Data Types**

Recognize custom data:
```markdown
# In privacy_classification_skill.md
Add:
- loyalty_points: Not personal data
- customer_tier: Not personal data
- spending_pattern: Sensitive personal data
```

---

## 📊 File Structure Reference

```
backend/
├── prompts/
│   └── system_prompt.md       # Main agent instructions
│
├── knowledge/
│   ├── privacy_rules.md       # Data definitions
│   ├── dpa_checklist.md       # Domestic checklist
│   └── otia_checklist.md      # Cross-border checklist
│
└── skills/
    ├── intake_skill.md
    ├── privacy_classification_skill.md
    ├── transfer_classification_skill.md
    ├── checklist_generation_skill.md
    ├── data_flow_generation_skill.md
    ├── privacy_summary_skill.md
    └── email_generation_skill.md
```

---

## ⚠️ Best Practices

### Before Editing:
1. **Backup original content** (copy to notepad)
2. **Understand the file** (read comments/structure)
3. **Plan your changes** (know what you want to achieve)

### While Editing:
1. **Use markdown format** (maintain ## headers, - lists)
2. **Keep structure** (don't break sections)
3. **Test incrementally** (small changes, test, repeat)

### After Editing:
1. **Save changes**
2. **Test immediately** with sample case
3. **Check output quality**
4. **Rollback if needed** (paste backup, save again)

---

## 🐛 Troubleshooting

### Changes not taking effect?

**Solution 1:** Reload agent config
```bash
docker-compose restart backend
```

**Solution 2:** Clear browser cache
```
Ctrl + F5 (hard refresh)
```

**Solution 3:** Check backend logs
```bash
docker-compose logs -f backend
```

### File won't save?

**Check:**
- Backend is running: `http://localhost:8000/health`
- File permissions are OK
- Content is valid markdown
- No special characters causing issues

### Content looks broken?

**Fix:**
- Restore from backup
- Check markdown syntax
- Ensure proper line breaks
- Remove any invalid characters

---

## 🔐 Security Notes

### Who should have access?
- ✅ Data Privacy Team leads
- ✅ Compliance officers
- ✅ System administrators
- ❌ Regular business users (use Chat only)

### Production considerations:
1. **Add authentication** to Admin Panel
2. **Version control** edits (git commit after changes)
3. **Audit log** who changed what
4. **Approval workflow** for critical changes

---

## 📸 Screenshots

### Admin Panel Navigation:
```
Sidebar → [⚙️ Admin Panel] button → Admin page
```

### Tabs:
- 📝 System Prompt - Edit main instructions
- 📚 Knowledge Base - Edit rules & checklists
- 🎯 Skills - Edit individual skills

### Editor Features:
- Large text area (400px height)
- Line & character counter
- Save & Reload buttons
- Structure preview (for skills)

---

## 🎯 Quick Tasks

### Task 1: Make agent more strict
```
Go to: System Prompt tab
Add: "Always flag ANY data sharing as high risk"
Save → Test
```

### Task 2: Add new country to cross-border checklist
```
Go to: Knowledge Base → otia_checklist.md
Add section: "## Singapore-specific requirements"
Add: "- Check MAS regulations"
Save → Test with Singapore case
```

### Task 3: Change email tone
```
Go to: Skills → email_generation_skill.md
Modify: Tone section to "Very formal and urgent"
Save → Test email generation
```

---

## ✅ Verification

After making changes, verify:

1. **Save confirmation:** ✅ Green success message appears
2. **Backend logs:** No errors in `docker-compose logs backend`
3. **Chat test:** Send test message, check if behavior changed
4. **Output quality:** Review full response for correctness

---

## 📞 Support

**Need help?**
- Check backend logs: `docker-compose logs -f backend`
- Test API: `curl http://localhost:8000/knowledge`
- Restore backup if broken
- Contact dev team

---

**Admin Panel v2.0**  
**Built for:** Easy agent customization  
**Status:** ✅ Production ready
