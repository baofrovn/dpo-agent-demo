# Transfer Classification Skill: Domestic vs Cross-Border Determination

## Purpose
Classify whether a data processing case involves domestic processing, domestic sharing, or cross-border transfer based on location analysis.

## Critical Importance
This classification determines:
- Which checklist to use (DPA vs OTIA)
- Risk level (cross-border = higher risk)
- Regulatory requirements
- Approval process complexity

**Getting this wrong has serious consequences**, so be thorough.

## Your Task
Analyze the case and classify it as:
1. **Domestic Processing** - All processing within Vietnam, no external sharing
2. **Domestic Sharing** - Sharing with partners/vendors in Vietnam
3. **Cross-Border Transfer** - Data leaves Vietnam in any way
4. **Need Confirmation** - Cannot determine without more information

## The Three Location Tests

To classify correctly, evaluate these three dimensions:

### Test 1: Recipient Location Test
**Question:** Where is the recipient/partner/vendor located?

**Indicators of Cross-Border:**
- Vendor company registered outside Vietnam
- Vendor headquarters outside Vietnam
- Contracting entity outside Vietnam
- Partner/vendor explicitly in another country

**Example phrases:**
- "Share with [Vendor] in Singapore"
- "Vendor is a US company"
- "Partner based in Japan"
- "[Foreign company name]"

**Classification:**
- Recipient outside Vietnam → **Cross-Border Transfer**
- Recipient in Vietnam → Continue to Test 2
- Recipient location unclear → Flag "Need Confirmation"

### Test 2: Storage/Server Location Test
**Question:** Where will the data be stored?

**Indicators of Cross-Border:**
- Servers outside Vietnam
- Cloud provider region outside Vietnam
- Data center outside Vietnam
- Foreign hosting service

**Common cloud indicators:**
- "AWS Singapore" → Cross-border
- "AWS Vietnam" → Domestic
- "Google Cloud" → Need to check region
- "Azure" → Need to check region
- "US-based cloud service" → Cross-border
- "Regional servers" → Need clarification on which region

**Classification:**
- Data stored outside Vietnam → **Cross-Border Transfer**
- Data stored in Vietnam → Continue to Test 3
- Storage location unclear → Flag "Need Confirmation"

**Important:** Even if vendor is in Vietnam, if they use foreign servers, it's still cross-border!

### Test 3: Access Location Test
**Question:** Who can access the data and where are they located?

**Indicators of Cross-Border:**
- Support team outside Vietnam
- Development team outside Vietnam with production access
- Remote access from foreign offices
- Global operations center outside Vietnam
- Personnel based abroad can view/access data

**Example phrases:**
- "Vendor has support team in India"
- "Global tech support"
- "Offshore development team"
- "Access by headquarters in [foreign country]"

**Classification:**
- Access from outside Vietnam → **Cross-Border Transfer**
- Access only from within Vietnam → Domestic
- Access location unclear → Flag "Need Confirmation"

## Classification Logic

### If ANY of the three tests indicate cross-border → It's Cross-Border Transfer

**Example:**
- Vendor in Vietnam ✓
- But uses AWS Singapore ✗
→ **Classification: Cross-Border Transfer**

**Example:**
- Vendor in Singapore ✗
→ **Classification: Cross-Border Transfer** (no need to check other tests)

### All three tests indicate domestic → Determine if Processing or Sharing

**Domestic Processing:**
- Data stays within company's own systems in Vietnam
- No external parties involved
- Internal data processing only

**Domestic Sharing:**
- Data shared with external parties (vendors/partners) in Vietnam
- Servers/storage in Vietnam
- Access only from Vietnam

## Classification Matrix

| Recipient Location | Storage Location | Access Location | Classification |
|-------------------|------------------|-----------------|----------------|
| Vietnam | Vietnam | Vietnam | Domestic Sharing |
| Vietnam | Vietnam | Foreign | **Cross-Border Transfer** |
| Vietnam | Foreign | Vietnam | **Cross-Border Transfer** |
| Vietnam | Foreign | Foreign | **Cross-Border Transfer** |
| Foreign | Any | Any | **Cross-Border Transfer** |
| Unclear | Any | Any | **Need Confirmation** |
| Any | Unclear | Any | **Need Confirmation** |
| Any | Any | Unclear | **Need Confirmation** |

## Common Tricky Scenarios

### Scenario 1: Vietnamese Vendor Using Foreign Cloud
**Case:** "Share data with Vietnam-based vendor who uses AWS Singapore"

**Analysis:**
- Recipient location: Vietnam ✓
- Storage location: Singapore ✗
- Classification: **Cross-Border Transfer**

**Reasoning:** Data physically leaves Vietnam when stored on Singapore servers, even if the vendor company is Vietnamese.

### Scenario 2: Foreign Company with Vietnam Operations
**Case:** "Integrate with [Foreign Company] Vietnam branch"

**Analysis:**
- Recipient: Foreign company with Vietnam branch - **Unclear**
- Need to ask: Where is data stored? Who accesses it? Is it isolated to Vietnam branch?

**If data stays in Vietnam branch only:** Potentially domestic
**If HQ can access or data syncs to HQ:** Cross-border

**Classification:** **Need Confirmation** (ask about data access and storage)

### Scenario 3: SaaS Platform with Unclear Location
**Case:** "Use [SaaS Platform] for customer data management"

**Analysis:**
- Platform location: Not specified
- Need to ask: Where are the platform's servers? What region will be used?

**Classification:** **Need Confirmation**

**Questions to ask:**
- What region/data center will be used?
- Where is data stored?
- Where is the support team located?

### Scenario 4: Email to Foreign Partner
**Case:** "Send customer reports via email to partner's Singapore office"

**Analysis:**
- Recipient location: Singapore ✗
- Classification: **Cross-Border Transfer**

**Reasoning:** Even simple email transfers count if recipient is abroad.

### Scenario 5: Backup to Foreign Cloud
**Case:** "Backup customer data to AWS Singapore as disaster recovery"

**Analysis:**
- Storage location: Singapore ✗
- Classification: **Cross-Border Transfer**

**Reasoning:** Backups are still cross-border transfers, even if they're just for emergency.

### Scenario 6: API Call Routing Through Foreign Servers
**Case:** "API integration with vendor; API is hosted outside Vietnam"

**Analysis:**
- Data transit location: Outside Vietnam ✗
- Classification: **Cross-Border Transfer**

**Reasoning:** If data transits through foreign servers, even temporarily, it may be considered cross-border.

### Scenario 7: Vendor with Multiple Locations
**Case:** "Partner with offices in Vietnam, Singapore, and Thailand"

**Analysis:**
- **Critical questions:**
  - Which entity will we contract with?
  - Where will data be stored?
  - Which office's staff will access data?

**Classification:** **Need Confirmation** until these are clarified.

## Red Flags that Usually Mean Cross-Border

🚩 Any mention of:
- AWS (without "Vietnam" explicitly stated)
- Google Cloud, Azure, or other major cloud providers (check region)
- "Global" or "international" services
- Foreign company names
- "Offshore" teams
- "Regional hub" outside Vietnam
- Foreign countries mentioned

When you see these, default to either:
- **Cross-Border Transfer** (if clear), or
- **Need Confirmation** (if unclear which region)

## When Location is Ambiguous

### Common Ambiguous Phrases
- "Cloud storage" → Which cloud? Which region?
- "Vendor" → Where located?
- "Third-party service" → Where hosted?
- "Partner" → Where based?
- "Analytics platform" → Where hosted?

### Your Response
**Classification:** Need Confirmation

**Questions to ask:**
- "What is the name and location of the vendor/partner?"
- "Where will the data be stored (which country/region)?"
- "Where is the support/operations team that will access this data located?"
- "If using cloud services, which provider and which region?"

## Output Format for This Skill

```markdown
### TRANSFER TYPE CLASSIFICATION

#### Classification Result

**Transfer Type:** Domestic Processing / Domestic Sharing / Cross-Border Transfer / Need Confirmation

---

#### Three-Test Analysis

**Test 1: Recipient Location**
- Finding: [Vietnam / Outside Vietnam / Unclear]
- Evidence: [Quote from case description or "Not specified"]
- Assessment: [Pass/Fail/Unclear]

**Test 2: Storage/Server Location**
- Finding: [Vietnam / Outside Vietnam / Unclear]
- Evidence: [Quote from case description or "Not specified"]
- Assessment: [Pass/Fail/Unclear]

**Test 3: Access Location**
- Finding: [Vietnam / Outside Vietnam / Unclear]
- Evidence: [Quote from case description or "Not specified"]
- Assessment: [Pass/Fail/Unclear]

---

#### Classification Reasoning

[Provide clear explanation of why you classified it this way. Reference specific 
evidence from the three tests. If cross-border, be explicit about which test(s) failed.]

**Key Evidence:**
- [Bullet points of key evidence that determined classification]

---

#### Confidence Level

**Confidence:** High / Medium / Low

**Why this confidence level:**
[Explain what makes you confident or uncertain]

---

#### If "Need Confirmation" - Specific Questions

- [ ] [Specific question about recipient location]
- [ ] [Specific question about storage location]
- [ ] [Specific question about access location]

---

#### Implications of This Classification

**Applicable Checklist:** 
[DPA Checklist for domestic / OTIA Checklist for cross-border / TBD pending confirmation]

**Risk Level Adjustment:**
[Cross-border transfers automatically elevate risk level]

**Human Review Required:**
[Yes for cross-border / Depends on other factors for domestic]
```

## Integration with Other Skills

### Impact on Checklist Generation
- Domestic → Use DPA Checklist
- Cross-Border → Use OTIA Checklist
- Need Confirmation → List both possibilities

### Impact on Risk Assessment
- Cross-border automatically increases risk level
- Cross-border + sensitive data = highest risk
- Cross-border to high-risk countries = extra scrutiny

### Impact on Summary
- Cross-border cases require more detailed summary
- Must highlight countries involved
- Must emphasize regulatory requirements

## Common Mistakes to Avoid

❌ **Mistake 1:** "Vendor is in Vietnam so it's domestic"
- Wrong if vendor uses foreign servers or has foreign access

❌ **Mistake 2:** "Just a small data transfer, doesn't count as cross-border"
- Any cross-border transfer counts, regardless of volume

❌ **Mistake 3:** "Data is encrypted so location doesn't matter"
- Location still matters; encryption is separate requirement

❌ **Mistake 4:** "It's just for backup/testing so it's not a real transfer"
- Backups and test data are still cross-border transfers

❌ **Mistake 5:** Assuming cloud provider region without confirmation
- Always ask which specific region will be used

## Quick Reference Decision Tree

```
START: Analyze case description

Is recipient explicitly outside Vietnam?
├─ Yes → CROSS-BORDER TRANSFER
└─ No or Unclear → Continue

Is storage/server explicitly outside Vietnam?
├─ Yes → CROSS-BORDER TRANSFER
└─ No or Unclear → Continue

Is data access from outside Vietnam?
├─ Yes → CROSS-BORDER TRANSFER
└─ No or Unclear → Continue

Is recipient, storage, AND access confirmed to be in Vietnam?
├─ Yes → DOMESTIC (Sharing or Processing depending on external party involvement)
└─ No → NEED CONFIRMATION (Ask specific questions about unclear locations)

Is there external party involved?
├─ Yes → DOMESTIC SHARING
└─ No → DOMESTIC PROCESSING
```

---

**Remember:** When in doubt, lean toward classifying as cross-border or requesting confirmation. It's better to be cautious with cross-border classification than to miss a cross-border transfer.
