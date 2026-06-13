# Privacy Summary Skill: Creating Executive Summaries for Reviewers

## Purpose
Create concise, actionable summaries for Data Privacy team reviewers that highlight key information, risks, and recommended next steps.

## Target Audience
The summary is for:
- **Data Privacy lawyers/reviewers** who need to quickly assess the case
- **Compliance team** who track privacy requests
- **Management** who may need to approve high-risk cases

They need to understand the case in 2-3 minutes.

## Your Task
Create a structured summary that answers:
1. What does Biz want to do?
2. What data is involved?
3. Who will receive/access the data and where?
4. What type of case is this (domestic/cross-border)?
5. What's the risk level?
6. What's missing?
7. What should happen next?

## Summary Structure

### Section 1: Case Overview
**Purpose:** One-paragraph description of the business request

**Format:**
```
[Business team] wants to [business action] with [partner/vendor name] 
for the purpose of [specific business purpose]. This involves [high-level description 
of data flow: sharing/transferring/processing] [data category] to/with [recipient].
```

**Example:**
```
Product team wants to integrate with TechVendor Singapore's analytics platform 
for the purpose of improving customer experience through behavioral insights. 
This involves sharing user behavioral data and transaction patterns via API 
to TechVendor's Singapore servers.
```

**Keep it:**
- Factual and neutral
- One paragraph (3-4 sentences max)
- Focus on business purpose, not technical details

### Section 2: Data Categories
**Purpose:** Clearly list what personal data is involved

**Format:**
```markdown
**Data Categories:**
- [Category 1]: [Specific fields if known]
- [Category 2]: [Specific fields if known]
- [etc.]

**Sensitive Personal Data:** Yes / No / Potentially
[If yes or potentially: Specify which categories and why they're sensitive]
```

**Example:**
```markdown
**Data Categories:**
- Identity data: User ID, name, email, phone number
- Transaction data: Transaction history, amounts, merchant names
- Behavioral data: App usage patterns, feature clicks

**Sensitive Personal Data:** Yes
Financial transaction history is considered sensitive personal data in fintech context.
```

**Tips:**
- Group by category (identity, transaction, behavioral, etc.)
- Be specific about fields when known
- Highlight sensitive data explicitly

### Section 3: Recipient & Location
**Purpose:** Clearly identify who gets data and where they are

**Format:**
```markdown
**Recipient:** [Name of vendor/partner or "Not specified"]
**Company Location:** [Country of vendor/partner]
**Data Storage Location:** [Where data will be stored]
**Data Access Location:** [Where data can be accessed from]
**Sub-Processors:** [List if known, or "Not disclosed"]
```

**Example:**
```markdown
**Recipient:** TechVendor Pte Ltd
**Company Location:** Singapore
**Data Storage Location:** AWS Singapore (ap-southeast-1 region)
**Data Access Location:** Singapore + potential access from US headquarters
**Sub-Processors:** AWS (Singapore), CloudAnalytics (USA) - for secondary processing
```

**Critical:** This section determines domestic vs cross-border classification

### Section 4: Transfer Type & Classification
**Purpose:** Clearly state the case classification

**Format:**
```markdown
**Transfer Type:** Domestic Processing / Domestic Sharing / Cross-Border Transfer

**Classification Reasoning:**
[Brief explanation of why this classification]

**Personal Data:** Yes / No / Likely
**Sensitive Data:** Yes / No / Potentially
**Cross-Border:** Yes / No / Need Confirmation
```

**Example:**
```markdown
**Transfer Type:** Cross-Border Transfer

**Classification Reasoning:**
Data will be stored on AWS Singapore servers and accessed by vendor's Singapore 
and US teams. This constitutes cross-border transfer as data physically leaves 
Vietnam and is accessible from multiple foreign jurisdictions.

**Personal Data:** Yes (user identifiers and transaction data)
**Sensitive Data:** Yes (financial transaction history)
**Cross-Border:** Yes (Singapore + USA)
```

### Section 5: Risk Level Assessment
**Purpose:** Provide quick risk assessment with justification

**Format:**
```markdown
**Risk Level:** Low / Medium / High / Critical

**Risk Factors:**
[+] Positive factors (risk reducers):
- [List factors that reduce risk]

[-] Negative factors (risk elevators):
- [List factors that increase risk]

**Overall Assessment:**
[One sentence summary of risk reasoning]
```

**Risk Level Guidelines:**

**🟢 Low Risk:**
- No personal data OR basic contact info only (name, email)
- Domestic only
- Well-established vendor with strong security
- Small scale (< 1,000 users)
- Existing approved DPA in place

**🟡 Medium Risk:**
- Personal data but not sensitive
- Domestic sharing with new vendor
- Standard security measures
- Moderate scale (1,000-10,000 users)
- Some documentation provided

**🔴 High Risk:**
- Sensitive personal data (financial, health, biometric)
- Cross-border transfer
- Weak security measures or no certifications
- Large scale (> 10,000 users)
- Missing critical documentation

**🚨 Critical Risk:**
- Sensitive financial data + cross-border to high-risk country
- No DPA or security measures
- Government access concerns
- Children's data
- Very large scale (> 100,000 users)

**Example:**
```markdown
**Risk Level:** High

**Risk Factors:**
[+] Positive factors:
- Vendor has ISO 27001 and SOC 2 certifications
- Limited data set (only transaction metadata, no full details)
- Existing business relationship with vendor

[-] Negative factors:
- Cross-border transfer (Singapore + USA)
- Sensitive financial data involved (transaction history)
- Large scale (50,000+ users affected)
- No existing DPA with cross-border clauses
- US access creates government surveillance concerns

**Overall Assessment:**
High risk due to cross-border transfer of sensitive financial data to multiple 
jurisdictions, requiring thorough legal review and enhanced safeguards.
```

### Section 6: Missing Items
**Purpose:** Highlight what's blocking or delaying approval

**Format:**
```markdown
**Critical Gaps (Blocking):**
- [Most important missing item]
- [Second most important]

**Important Gaps (Needed for Approval):**
- [High-priority missing items]

**Nice to Have:**
- [Non-blocking items]
```

**Example:**
```markdown
**Critical Gaps (Blocking):**
- No DPA with cross-border transfer clauses
- Security measures not documented
- No evidence of user consent/notice for cross-border transfer

**Important Gaps (Needed for Approval):**
- Sub-processor list incomplete (CloudAnalytics role unclear)
- Data retention period not specified
- Incident response mechanism not defined

**Nice to Have:**
- Audit rights in contract
- Regular security assessment reports
```

### Section 7: Recommended Next Steps
**Purpose:** Provide clear, actionable guidance

**Format:**
```markdown
**Immediate Actions (This Week):**
1. [Most urgent action]
2. [Second most urgent]

**Short-Term Actions (Before Approval):**
1. [Important follow-up]
2. [Documentation needed]

**Long-Term Considerations:**
- [Ongoing obligations]
- [Future review points]
```

**Example:**
```markdown
**Immediate Actions (This Week):**
1. Request Business team to provide specific data fields to be shared
2. Obtain draft DPA from vendor with cross-border transfer clauses
3. Confirm whether US headquarters will have access to data

**Short-Term Actions (Before Approval):**
1. Review and negotiate DPA with Legal team
2. Update privacy policy to disclose cross-border transfer to Singapore and USA
3. Implement user consent mechanism for sensitive data transfer
4. Verify vendor's security certifications (ISO 27001, SOC 2)

**Long-Term Considerations:**
- Annual review of vendor's security practices
- Monitor for changes in US data access laws
- Establish data subject rights handling process with vendor
- Plan for OTIA documentation and filing
```

### Section 8: Human Review Flag
**Purpose:** Clearly state if human review is required and why

**Format:**
```markdown
**Human Review Required:** Yes / No / Optional

**Reason:**
[Explain why human review is or isn't needed]

**Recommended Reviewer:**
[Suggest who should review: junior privacy staff / senior privacy lawyer / compliance + legal / executive approval]
```

**Example:**
```markdown
**Human Review Required:** Yes

**Reason:**
This case involves cross-border transfer of sensitive financial data (transaction history) 
to multiple jurisdictions including USA. US government access to data is a known risk 
factor. This requires legal review to ensure compliance with Vietnamese data protection 
requirements and assessment of adequacy safeguards.

**Recommended Reviewer:**
Senior Privacy Lawyer + Compliance Team
Executive approval recommended due to scale (50,000+ users) and high-risk country involvement.
```

## Tone and Style Guidelines

### Do's
✅ Be concise - respect reviewer's time
✅ Be specific - cite concrete facts
✅ Be objective - neutral tone
✅ Be clear about uncertainty - flag what's unknown
✅ Be actionable - recommend specific next steps
✅ Be risk-aware - call out real concerns

### Don'ts
❌ Don't be overly technical
❌ Don't use vague language ("might", "could", "possibly" without context)
❌ Don't make assumptions - state when you're inferring
❌ Don't be alarmist - but don't downplay real risks either
❌ Don't repeat information - each section should add new insight
❌ Don't forget the business context - this is helping a business need

## Length Guidelines

**Total Summary Length:** 300-500 words (excluding the structured format)

**Section Lengths:**
- Case Overview: 3-4 sentences
- Data Categories: Bullet list (5-10 items max)
- Recipient & Location: 4-5 fields
- Classification: 2-3 sentences reasoning
- Risk Assessment: 3-5 risk factors each side, 1 sentence summary
- Missing Items: Bullet list (prioritized)
- Next Steps: 3-5 immediate actions, 2-3 short-term, 2-3 long-term
- Human Review: 2-3 sentences

## Special Considerations

### For Unclear Cases
If information is incomplete:
```markdown
**Note on Completeness:**
This summary is based on limited information provided. Several critical details 
are missing [list top 3]. Recommendation: Request complete information before 
proceeding with detailed legal review.
```

### For Urgent Cases
If timeline is tight:
```markdown
**Timeline Note:**
Business team has indicated this is time-sensitive (target launch: [date]). 
Recommended expedited review track. However, all critical documentation must 
still be provided - no shortcuts on DPA and security review.
```

### For Low-Risk Cases
If it's straightforward:
```markdown
**Fast-Track Eligible:**
This case appears to be low-risk [briefly why]. If documentation is complete 
and standard DPA template applies, may be eligible for fast-track approval 
by junior privacy staff.
```

### For Repeat Cases
If similar to previous approved case:
```markdown
**Similar to Previous Case:**
This case is similar to [Previous Case Name/ID] approved on [date]. However, 
note key differences: [list differences]. May be able to use same DPA template 
with modifications.
```

## Output Format for This Skill

```markdown
### SUMMARY FOR DATA PRIVACY TEAM

#### Case Overview
[One paragraph description of what Business team wants to do]

---

#### Data Categories
**Data Categories:**
- [List categories and fields]

**Sensitive Personal Data:** [Yes/No/Potentially]
[Explanation if yes/potentially]

---

#### Recipient & Location
**Recipient:** [Name]
**Company Location:** [Country]
**Data Storage Location:** [Location]
**Data Access Location:** [Location(s)]
**Sub-Processors:** [List or "Not disclosed"]

---

#### Transfer Type & Classification
**Transfer Type:** [Domestic Processing/Sharing or Cross-Border Transfer]

**Classification Reasoning:**
[Explanation]

**Summary:**
- Personal Data: [Yes/No/Likely]
- Sensitive Data: [Yes/No/Potentially]
- Cross-Border: [Yes/No]

---

#### Risk Level Assessment
**Risk Level:** [Low/Medium/High/Critical]

**Risk Factors:**
[+] Positive factors:
- [List]

[-] Negative factors:
- [List]

**Overall Assessment:**
[One sentence]

---

#### Missing Items
**Critical Gaps (Blocking):**
- [List]

**Important Gaps (Needed for Approval):**
- [List]

**Nice to Have:**
- [List]

---

#### Recommended Next Steps
**Immediate Actions (This Week):**
1. [Action]
2. [Action]

**Short-Term Actions (Before Approval):**
1. [Action]
2. [Action]

**Long-Term Considerations:**
- [Consideration]
- [Consideration]

---

#### Human Review Required
**Human Review Required:** [Yes/No/Optional]

**Reason:**
[Explanation]

**Recommended Reviewer:**
[Suggestion]

---

**Prepared by:** Data Privacy Intake Agent
**Date:** [Current date]
**Confidence Level:** [High/Medium/Low based on information completeness]
```

## Quality Checklist

Before finalizing the summary, verify:

- [ ] Case overview is clear and includes business purpose
- [ ] Data categories are specific (not just "customer data")
- [ ] Recipient location is clearly stated
- [ ] Classification is justified with reasoning
- [ ] Risk level matches the risk factors listed
- [ ] Missing items are prioritized (critical vs nice-to-have)
- [ ] Next steps are actionable and specific
- [ ] Human review requirement is clear
- [ ] Summary is concise (300-500 words)
- [ ] Tone is professional and objective

---

Remember: This summary may be the first thing a busy reviewer reads. Make it count. Be clear, be concise, be helpful.
