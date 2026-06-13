# Intake Skill: Information Gathering and Standardization

## Purpose
Extract, organize, and standardize information from the business team's case description to prepare for analysis.

## Your Task
When analyzing a case submission, you must:

1. **Extract key information** from the business team's description
2. **Identify gaps** in the information provided
3. **Standardize** the information into a consistent format
4. **Flag ambiguities** that need clarification

## Information to Extract

### 1. Business Purpose
**Look for:**
- What is the business team trying to accomplish?
- What problem are they solving?
- What is the expected business outcome?
- Why is this needed now?

**Common phrases:**
- "We want to..."
- "Our goal is to..."
- "To enable..."
- "For the purpose of..."

**Output format:**
```
Purpose: [Clear, concise statement of business purpose]
```

### 2. Data Categories
**Look for:**
- Specific data fields mentioned (name, phone, email, user ID, etc.)
- Descriptions like "customer information", "transaction data", "user profile"
- Technical terms like "PII", "personal data", "customer data"

**Red flags indicating personal data:**
- Any mention of names, contacts, identifiers
- "Customer", "user", "member" information
- "Profile", "account", "transaction" data
- "Behavioral", "usage", "activity" data

**Output format:**
```
Data Categories:
- Explicitly mentioned: [list]
- Likely involved (based on description): [list]
- Need confirmation: [list]
```

### 3. Recipient/Partner/Vendor Details
**Look for:**
- Name of the partner/vendor/third party
- Location or country of the recipient
- Type of entity (vendor, partner, affiliate, etc.)
- Their role in the data flow

**Common patterns:**
- "Share with [vendor name]"
- "Send to [partner]"
- "Use [vendor] service"
- "[Vendor] will process..."

**Output format:**
```
Recipient: [Name if provided, or "Not specified"]
Location: [Country/region if provided, or "Not specified"]
Type: [Vendor/Partner/Service Provider/etc., or "Not specified"]
```

### 4. Data Transfer Mechanism
**Look for:**
- How will data be shared? (API, file transfer, email, database access, etc.)
- What technology is involved? (cloud service, system integration, etc.)
- Is it one-time or ongoing?

**Common patterns:**
- "Via API"
- "Upload files to..."
- "Give access to our database"
- "Integrate with [system]"
- "Send via email"

**Output format:**
```
Transfer Mechanism: [Description if provided, or "Not specified"]
Frequency: [One-time/Daily/Real-time/etc., or "Not specified"]
```

### 5. Server/Storage Location
**Look for:**
- Where will data be stored?
- What cloud provider is used?
- What region/country for servers?

**Common patterns:**
- "AWS Singapore"
- "Google Cloud"
- "Our servers in Vietnam"
- "Vendor's data center"
- "[Country] servers"

**Critical for cross-border determination:**
- If server/storage is outside Vietnam → cross-border case
- If not specified → flag for confirmation

**Output format:**
```
Storage Location: [Location if provided, or "Not specified - NEED CONFIRMATION"]
```

### 6. Data Access Location
**Look for:**
- Where are the people who will access data located?
- Is there remote access from outside Vietnam?
- Where is the support/operations team based?

**Common patterns:**
- "Support team in [country]"
- "Accessed by [location] team"
- "Remote access from..."
- "Global operations center"

**Critical for cross-border determination:**
- If access is from outside Vietnam → cross-border case
- If not specified → flag for confirmation

**Output format:**
```
Access Location: [Location if provided, or "Not specified - NEED CONFIRMATION"]
```

### 7. Existing Documentation
**Look for:**
- Mention of contracts, agreements, DPA
- Security certifications
- Approvals already obtained
- Previous similar cases

**Common phrases:**
- "We have a contract with..."
- "DPA is signed"
- "They are ISO certified"
- "Similar to [previous project]"

**Output format:**
```
Existing Documentation:
- [List what's mentioned]
- [Or "None mentioned" if nothing]
```

### 8. Urgency/Timeline
**Look for:**
- When does this need to be implemented?
- Is there a deadline?
- Why is it time-sensitive?

**Output format:**
```
Timeline: [Timeline if mentioned, or "Not specified"]
Urgency: [High/Medium/Normal based on description]
```

## Standardization Process

### Step 1: Read the Entire Description
- Don't jump to conclusions after reading the first sentence
- Look for details throughout the description
- Note any contradictions or unclear statements

### Step 2: Extract Information Using the Framework Above
- Go through each of the 8 categories
- Extract explicit information first
- Note implicit information (things suggested but not stated)
- Flag missing information

### Step 3: Identify Ambiguities
Common ambiguities to flag:
- **"Customer data"** → What specific fields?
- **"For analysis"** → What kind of analysis? Who does it?
- **"Partner in Vietnam"** → But where are their servers?
- **"Vendor"** → What's their name and exact location?
- **"Transaction information"** → Full details or aggregated?
- **"Cloud service"** → Which provider and which region?

### Step 4: Categorize Information Completeness
For each key area, assess:
- ✅ **Complete**: Sufficient information provided
- ⚠️ **Partial**: Some information but needs more detail
- ❌ **Missing**: No information provided, critical gap

## Missing Information Identification

### Critical Missing Information (Must Have)
These are always required:
- [ ] Clear business purpose
- [ ] Specific data categories/fields
- [ ] Recipient/vendor name and location
- [ ] Data storage location
- [ ] Data access location
- [ ] Transfer mechanism

### Important Missing Information (Should Have)
These are very important but may be gathered later:
- [ ] Data retention period
- [ ] Security measures
- [ ] Existing contracts/DPA
- [ ] User consent/notice mechanism
- [ ] Volume/number of users affected

### Nice-to-Have Missing Information
These help but are not blockers:
- [ ] Technical architecture details
- [ ] Project timeline
- [ ] Business justification/ROI
- [ ] Alternative solutions considered

## Common Case Patterns

### Pattern 1: Cloud Service Usage
**Typical description:** "We want to use [Cloud Service] for [purpose]"

**What to extract:**
- Cloud provider name (AWS, GCP, Azure, etc.)
- Service type (storage, compute, analytics, etc.)
- Region/location of cloud resources
- What data will be stored/processed
- Who has access to the cloud console

**Critical question:** Which region? (This determines cross-border status)

### Pattern 2: Vendor/Partner Integration
**Typical description:** "We want to integrate with [Vendor] to [purpose]"

**What to extract:**
- Vendor name and location
- Integration method (API, file transfer, etc.)
- What data will be shared
- What vendor will do with the data
- Whether there's a contract

**Critical question:** Where is the vendor located and where do they store data?

### Pattern 3: Third-Party Service
**Typical description:** "We want to use [Service] for our customers"

**What to extract:**
- Service provider details
- What customer data is needed
- How service will be delivered
- Where service operates
- What customers will experience

**Critical question:** Is this on behalf of customers (controller) or by vendor (processor)?

### Pattern 4: Data Analytics/AI Project
**Typical description:** "We want to analyze customer data for [purpose]"

**What to extract:**
- What data will be analyzed
- Who performs the analysis (internal or vendor)
- Where analysis happens
- What insights are expected
- How results will be used

**Critical question:** Is customer data identifiable in the analysis?

## Output Format for This Skill

When you extract and standardize information, use this format:

```markdown
### EXTRACTED INFORMATION

**Business Purpose:**
[Clear statement or "Not clearly specified"]

**Data Categories:**
- Explicitly mentioned: [list]
- Likely involved: [list]
- Unclear/Need confirmation: [list]

**Recipient Details:**
- Name: [name or "Not specified"]
- Location: [location or "Not specified - CRITICAL GAP"]
- Type: [vendor/partner/etc. or "Not specified"]

**Transfer/Access Mechanism:**
[Description or "Not specified"]

**Storage Location:**
[Location or "Not specified - CRITICAL GAP for cross-border determination"]

**Access Location:**
[Location or "Not specified - CRITICAL GAP for cross-border determination"]

**Existing Documentation:**
- [List or "None mentioned"]

**Timeline:**
[Timeline or "Not specified"]

---

### INFORMATION COMPLETENESS ASSESSMENT

✅ **Complete:**
- [List areas where info is sufficient]

⚠️ **Partial:**
- [List areas where more detail needed]

❌ **Missing (Critical Gaps):**
- [List critical missing information]

---

### KEY AMBIGUITIES TO CLARIFY

1. [Ambiguity 1 and why it matters]
2. [Ambiguity 2 and why it matters]
3. [...]

---

### PRELIMINARY CLASSIFICATION INDICATORS

**Personal Data Likely?** Yes/No/Unclear
**Reasoning:** [Brief explanation]

**Sensitive Data Likely?** Yes/No/Unclear
**Reasoning:** [Brief explanation]

**Cross-Border Likely?** Yes/No/Unclear
**Reasoning:** [Brief explanation based on location indicators]
```

## Best Practices

1. **Be thorough but not judgmental**: Extract what's there without criticizing the submission
2. **Flag uncertainties explicitly**: If you're not sure, say so
3. **Use business team's language**: Quote their terms, then translate to privacy terms
4. **Prioritize critical gaps**: Some missing info is more important than others
5. **Provide context for why information matters**: Help business team understand what you need

## Red Flags to Immediately Highlight

🚩 **"Share transaction history with vendor outside Vietnam"** → Cross-border + sensitive data  
🚩 **"Give database access to offshore team"** → Cross-border + broad access  
🚩 **"Upload customer data to [foreign cloud service]"** → Cross-border transfer  
🚩 **"Vendor will use data for their own analysis"** → Potential controller-controller issue  
🚩 **"Store indefinitely"** → Retention issue  
🚩 **"Share all customer data"** → Over-collection issue

When you see these, immediately flag them in your assessment.

---

This skill ensures that every case starts with clear, standardized information extraction, making the rest of the analysis more accurate and efficient.
