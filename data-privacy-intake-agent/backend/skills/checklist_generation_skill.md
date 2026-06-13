# Checklist Generation Skill: Document Requirements

## Purpose
Generate appropriate document checklist based on the case classification, highlighting priority items and identifying gaps.

## Your Task
Based on the case classification (domestic vs cross-border, personal vs sensitive data), generate a practical, prioritized checklist of required documents and information.

## Checklist Selection Logic

### Decision Flow

```
Is this cross-border transfer?
├─ Yes → Use OTIA CHECKLIST (cross-border checklist)
│         Include all 14 OTIA items
│         Mark high-priority items
│         Add specific questions based on case
│
└─ No → Is personal data involved?
    ├─ Yes → Use DPA CHECKLIST (domestic checklist)
    │         Include all 10-13 DPA items
    │         Mark high-priority items
    │         Add specific questions based on case
    │
    └─ No → MINIMAL CHECKLIST
              Basic documentation for no-PII cases
              Request confirmation of anonymization
```

### If Classification is "Need Confirmation"
Present BOTH checklists with explanation:
- "If this is domestic sharing, you'll need: [DPA checklist]"
- "If this is cross-border transfer, you'll need: [OTIA checklist]"
- "Priority: First clarify the classification questions"

## Priority Levels

Mark each checklist item with priority:

### 🔴 **Critical (P0)** - Must have before any approval
These are absolute requirements; case cannot proceed without them.

**For ALL cases:**
- Business purpose
- Data categories
- Recipient details
- DPA or data protection clauses

**For cross-border cases, also critical:**
- Recipient country
- Storage location
- Cross-border DPA clauses
- User consent/notice mechanism

### 🟡 **High Priority (P1)** - Needed for approval
These are very important and will be requested during review.

**For ALL cases:**
- Security measures
- Retention period
- Incident response obligations

**For cross-border cases, also high priority:**
- Data protection level assessment
- Transfer mechanism details
- Sub-processor list with locations

### 🟢 **Important (P2)** - Should have for complete review
These strengthen the case and speed up approval.

**For ALL cases:**
- Audit rights
- Data subject rights handling
- Sub-processor list
- Evidence of consent/notice

## DPA Checklist Template (Domestic Cases)

Use this for domestic sharing/processing:

```markdown
### Required Documents and Information

#### 🔴 Critical - Must Have

- [ ] **Contract or Master Service Agreement (MSA)**
  - Status: [Provided / In Draft / Not Yet / Not Mentioned]
  - Action: [If missing: "Please provide signed contract or latest draft"]

- [ ] **Data Processing Agreement (DPA) or Data Protection Clauses**
  - Status: [Provided / In Draft / Not Yet / Not Mentioned]
  - Action: [If missing: "Please provide DPA or highlight data protection clauses in contract"]
  - Note: This is legally required for any sharing of personal data

- [ ] **Purpose of Data Processing**
  - Status: [Clear / Partially Clear / Unclear]
  - Current understanding: [Summarize what you understood]
  - Action: [If unclear: "Please provide detailed business purpose including what the partner will do with the data"]

- [ ] **Categories of Personal Data**
  - Status: [Specific fields listed / General description / Not specified]
  - Current understanding: [List what you know]
  - Action: [If missing: "Please provide exhaustive list of specific data fields (e.g., name, email, phone, user ID, transaction amounts, etc.)"]
  - Important: If sensitive data, mark as "⚠️ SENSITIVE DATA INVOLVED"

#### 🟡 High Priority - Needed for Approval

- [ ] **Roles and Responsibilities**
  - Status: [Defined / Partially Defined / Not Defined]
  - Action: [If missing: "Please clarify if vendor is Data Processor (processing on your behalf) or independent Data Controller"]

- [ ] **Data Retention Period**
  - Status: [Specified / Not Specified]
  - Current understanding: [State if provided]
  - Action: [If missing: "Please specify how long data will be retained by the partner"]

- [ ] **Security and Confidentiality Measures**
  - Status: [Documented / Partially Documented / Not Documented]
  - Current understanding: [List known security measures]
  - Action: [If missing: "Please provide details on: (1) Encryption (in transit and at rest), (2) Access controls, (3) Security certifications (ISO 27001, SOC 2, etc.)"]

- [ ] **Incident Response and Breach Notification**
  - Status: [Defined / Not Defined]
  - Action: [If missing: "Please ensure contract includes breach notification obligations (timeframe, process, responsibilities)"]

#### 🟢 Important - Should Have

- [ ] **Sub-Processor List** (if applicable)
  - Status: [Provided / Not Provided / Not Applicable]
  - Action: [If applicable but missing: "Please list any sub-contractors who will access data, including their names and locations"]
  - ⚠️ If sub-processors are outside Vietnam, this becomes cross-border case!

- [ ] **Data Subject Rights Handling Mechanism**
  - Status: [Defined / Not Defined]
  - Action: [If missing: "Please establish process for handling user requests (access, deletion, correction)"]

- [ ] **Data Return or Deletion Upon Termination**
  - Status: [Specified / Not Specified]
  - Action: [If missing: "Please specify what happens to data when contract ends (deletion or return within X days)"]

- [ ] **Audit Rights**
  - Status: [Included in contract / Not Included]
  - Action: [If missing: "Consider including right to audit vendor's data handling practices"]

- [ ] **Evidence of User Consent or Notice**
  - Status: [Provided / Not Provided]
  - Current notice status: [Summarize]
  - Action: [If missing: "Please provide copy of privacy policy or user notice mentioning this data sharing"]
```

## OTIA Checklist Template (Cross-Border Cases)

Use this for cross-border transfers (in ADDITION to DPA items):

```markdown
### Cross-Border Transfer Requirements

**⚠️ This is a cross-border data transfer case. Additional requirements apply.**

#### 🔴 Critical - Must Have for Cross-Border

- [ ] **Name and Legal Details of Data Recipient**
  - Status: [Provided / Partial / Not Provided]
  - Current information: [What you know]
  - Action: [If missing: "Please provide: (1) Full legal name, (2) Company registration number, (3) Country of registration"]

- [ ] **Country/Jurisdiction of Recipient**
  - Status: [Specified / Not Specified]
  - Current information: [What you know]
  - Action: [If missing: "Please specify: (1) Country of recipient company, (2) Country where data will be stored, (3) Countries from which data may be accessed"]

- [ ] **Purpose of Cross-Border Transfer**
  - Status: [Clear / Unclear]
  - Current understanding: [Summarize]
  - Action: [If missing: "Please justify why data must leave Vietnam (business necessity)"]

- [ ] **Categories of Personal Data to be Transferred**
  - Status: [Specific / General / Not Specified]
  - Current understanding: [List what you know]
  - Action: [If missing: "Please provide exhaustive list of data fields that will cross borders"]
  - Important: If sensitive financial data, mark as "🚨 SENSITIVE FINANCIAL DATA - HIGHEST RISK"

- [ ] **DPA with Cross-Border Transfer Clauses**
  - Status: [Provided / In Draft / Not Yet]
  - Action: [If missing: "Please ensure DPA specifically addresses cross-border transfer, including: (1) Acknowledgment of international transfer, (2) Applicable law, (3) Recipient's commitments to Vietnam data protection principles"]
  - Note: Standard DPA is not sufficient; must have cross-border specific clauses

- [ ] **Evidence of User Consent or Notice for Cross-Border Transfer**
  - Status: [Provided / Not Provided]
  - Action: [If missing: "Please provide: (1) Updated privacy policy mentioning cross-border transfer to [specific country], (2) User consent mechanism if sensitive data or high-risk country"]

#### 🟡 High Priority - Needed for Approval

- [ ] **Data Subject Groups Affected**
  - Status: [Specified / Not Specified]
  - Current understanding: [What you know]
  - Action: [If missing: "Please specify which users are affected and how many (e.g., 'all active customers - ~50,000 users')"]

- [ ] **Mechanism of Data Transfer**
  - Status: [Described / Not Described]
  - Current understanding: [What you know]
  - Action: [If missing: "Please describe technical transfer method: (1) API/file transfer/database access, (2) Frequency (real-time/daily/one-time), (3) Encryption in transit"]

- [ ] **Data Retention Period**
  - Status: [Specified / Not Specified]
  - Action: [If missing: "Please specify how long data will be stored outside Vietnam"]

- [ ] **Security Measures During Transfer and Storage**
  - Status: [Documented / Not Documented]
  - Current understanding: [List known measures]
  - Action: [If missing: "Please provide: (1) Encryption (transit: TLS 1.2+, at rest: AES-256), (2) Access controls (MFA, RBAC), (3) Certifications (ISO 27001, SOC 2), (4) Data center security"]

- [ ] **Sub-Processor List and Locations**
  - Status: [Provided / Not Provided]
  - Action: [If missing: "Please list all sub-processors, their countries, and their roles. Each additional country adds complexity."]

- [ ] **Assessment of Recipient's Data Protection Level**
  - Status: [Provided / Not Provided]
  - Action: [If missing: "Please assess: (1) Does recipient country have data protection laws? (2) Are they enforced? (3) Can government access data without due process? (4) What is recipient's compliance track record?"]

#### 🟢 Important - Should Have

- [ ] **Data Subject Rights Handling Mechanism**
  - Action: [If missing: "Please describe how users can exercise rights (access, deletion, correction) for data stored abroad"]

- [ ] **Incident Response for Cross-Border Breaches**
  - Action: [If missing: "Please ensure process for breach notification (72-hour notification requirement, cooperation in investigation)"]
```

## Checklist Customization Based on Case Details

### If Sensitive Financial Data is Involved
Add these extra items:
```markdown
#### Additional Requirements for Sensitive Financial Data

- [ ] **Enhanced Security Certification**
  - Required: ISO 27001, SOC 2 Type II, or equivalent
  - Action: "Please provide evidence of security certifications"

- [ ] **Explicit User Consent for Sensitive Data**
  - Action: "Please provide evidence that users explicitly consented to sharing of financial data"

- [ ] **Enhanced Encryption**
  - Required: Data must be encrypted both in transit AND at rest
  - Action: "Please confirm encryption standards (TLS 1.2+ for transit, AES-256 for at rest)"
```

### If High-Risk Country
Add:
```markdown
#### Additional Requirements for High-Risk Country Transfer

- [ ] **Privacy Impact Assessment (PIA)**
  - Action: "A formal PIA is required for transfers to [country name]"

- [ ] **Alternative Solutions Analysis**
  - Action: "Please document why data cannot stay in Vietnam and what alternatives were considered"

- [ ] **Enhanced Contractual Safeguards**
  - Action: "Please include additional contractual protections due to high-risk destination"
```

### If Large Scale (>10,000 users)
Add:
```markdown
#### Additional Requirements for Large-Scale Processing

- [ ] **Executive Approval**
  - Action: "This case affects >10,000 users and requires executive sign-off"

- [ ] **Phased Rollout Plan**
  - Action: "Please provide plan for gradual rollout with monitoring"
```

## Identifying What's Already Provided

For each checklist item, assess current status:

### Status Indicators

**✅ Provided:**
- Information is explicitly mentioned
- Documents are attached or referenced
- Details are clear and sufficient

**🟡 Partially Provided:**
- Some information given but incomplete
- Needs more detail
- General description without specifics

**❌ Not Provided:**
- No mention in the case description
- Critical gap
- Must be obtained

**❓ Unclear:**
- Contradictory information
- Vague description
- Needs clarification

### Example Assessment

If case says: "We have a contract with the vendor"
- Contract: ✅ **Provided** (mentioned)
- DPA: ❓ **Unclear** (does contract include DPA clauses?)
- Data categories: ❌ **Not Provided** (not mentioned)

## Output Format for This Skill

```markdown
### REQUIRED DOCUMENT CHECKLIST

**Case Type:** [Domestic Sharing / Cross-Border Transfer / TBD]

**Checklist Applied:** [DPA Checklist / OTIA Checklist / Both (pending classification)]

---

[Insert appropriate checklist template from above]

---

### Current Documentation Status Summary

**Documents Provided or Mentioned:**
- [List what business team has mentioned or provided]

**Critical Gaps (🔴 P0):**
- [List all critical missing items]
- These must be provided before review can proceed

**High Priority Gaps (🟡 P1):**
- [List all high-priority missing items]
- These will be needed for approval

**Nice to Have (🟢 P2):**
- [List important but not blocking items]

---

### Estimated Documentation Completeness

**Overall Status:** [X%] complete

**Breakdown:**
- Critical items (P0): [X/Y] provided
- High-priority items (P1): [X/Y] provided
- Important items (P2): [X/Y] provided

**Assessment:**
- **Ready for review:** [Yes/No] - [Brief explanation]
- **Estimated time to complete:** [If items are missing, estimate how long to gather]

---

### Next Steps for Business Team

**Immediate Actions (Complete First):**
1. [Most critical missing item]
2. [Second most critical]
3. [Third most critical]

**Follow-Up Actions:**
1. [High-priority items]
2. [Other important items]

**Timeline Recommendation:**
- Critical items: Provide within [X] days
- All P0+P1 items: Provide within [Y] days for timely review
```

## Best Practices

1. **Be specific in action items**: Don't just say "provide security info"; say "provide details on encryption (TLS version, algorithms), access controls, and security certifications"

2. **Acknowledge what's provided**: Give credit for what business team has already done

3. **Prioritize ruthlessly**: Make it clear what's blocking vs nice-to-have

4. **Provide context**: Explain WHY each item is needed

5. **Be realistic**: Don't ask for documentation that doesn't exist or isn't relevant

6. **Adapt to case specifics**: Don't just copy-paste standard checklist; customize based on case details

## Common Mistakes to Avoid

❌ Asking for every possible document without prioritization
✅ Focus on critical items first

❌ Generic requests like "provide more information"
✅ Specific requests like "provide list of data fields: name, email, phone, etc."

❌ Ignoring what's already provided
✅ Acknowledge provided items and focus on gaps

❌ Same checklist for all cases
✅ Customize based on domestic/cross-border, sensitive/non-sensitive

---

Remember: The checklist should be helpful, not overwhelming. Prioritize and provide clear guidance.
