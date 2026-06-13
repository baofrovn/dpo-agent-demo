# Privacy Classification Skill: Personal and Sensitive Data Identification

## Purpose
Determine whether personal data and sensitive personal data are involved in the case, with clear reasoning and confidence levels.

## Your Task
Based on the extracted information, classify:
1. Whether personal data is involved
2. Whether sensitive personal data is involved
3. Provide reasoning for each classification
4. Indicate confidence level

## Classification Framework

### Step 1: Personal Data Classification

**Question:** Does this case involve personal data?

**Answer Options:**
- **Yes** - Clearly involves personal data
- **Likely** - Strong indicators of personal data but needs confirmation
- **Potentially** - Unclear, depends on specifics
- **No** - Does not involve personal data (rare)
- **Need Confirmation** - Cannot determine without more information

### Personal Data Indicators

#### DEFINITE Personal Data (Always "Yes")
- Name (first name, last name, full name)
- Phone number
- Email address
- National ID number (CMND/CCCD)
- Passport number
- User ID, customer ID, account ID
- Device ID, IMEI, MAC address
- IP address
- Transaction records linked to individuals
- Location data (GPS, address)
- Biometric data (fingerprint, facial recognition)
- Any data that can identify a specific person

#### LIKELY Personal Data (Answer "Likely")
- "Customer information" without specifics
- "User profiles"
- "Account data"
- "Transaction history" (usually linkable to individuals)
- "Behavioral data"
- "App usage data"
- "Customer preferences"

#### POTENTIALLY Personal Data (Answer "Potentially")
- "Analytics data" - depends if identifiable
- "Aggregate reports" - depends if truly anonymized
- "Session data" - depends if linked to users
- "Device data" - depends if linkable to individuals

#### NOT Personal Data (Answer "No")
- Truly aggregated statistics (e.g., "total transactions per day")
- Anonymized data that cannot be re-identified
- System performance metrics with no user link
- Generic business data with no individual link

**Important:** When in doubt between "Likely" and "Potentially", choose "Likely" and ask for confirmation.

### Step 2: Sensitive Personal Data Classification

**Question:** Does this case involve sensitive personal data?

**Answer Options:**
- **Yes** - Clearly involves sensitive personal data
- **Potentially** - May involve sensitive data based on context
- **Likely Not** - Probably not sensitive (but still personal)
- **No** - Does not involve sensitive personal data
- **Need Confirmation** - Cannot determine without more information

### Sensitive Personal Data Indicators

#### DEFINITE Sensitive Personal Data (Always "Yes")

**Financial Data:**
- Bank account numbers
- Credit card numbers, debit card numbers
- Credit scores, credit ratings
- Loan information, debt records
- Transaction history with amounts
- Income or salary information
- Financial statements
- Investment portfolios

**Authentication Data:**
- Passwords, PINs, security codes
- Biometric data (fingerprints, facial recognition, iris scans, voice prints)
- Security questions and answers
- Authentication tokens

**Health Data:**
- Medical records
- Health conditions, diagnoses
- Prescription information
- Hospital records
- Health insurance information

**Government IDs:**
- National ID numbers (CMND/CCCD)
- Passport numbers
- Social security numbers
- Driver's license numbers

#### POTENTIALLY Sensitive Personal Data (Answer "Potentially")

**For Fintech Context:**
- "Transaction history" → Likely sensitive (financial)
- "Payment information" → Likely sensitive (financial)
- "Customer financial profile" → Likely sensitive
- "Credit assessment data" → Likely sensitive
- "Account balance" → Likely sensitive
- "Spending patterns" → Potentially sensitive (reveals financial behavior)

**Location Data:**
- Real-time GPS tracking → Potentially sensitive
- Home/work address → Potentially sensitive
- Location history → Potentially sensitive

**Communication Data:**
- Email content → Potentially sensitive depending on content
- Chat messages → Potentially sensitive
- Call recordings → Potentially sensitive

#### NOT Sensitive Personal Data (Answer "No")
- Name and email only (personal but not sensitive)
- Phone number only (personal but not sensitive)
- User ID only (personal but not sensitive)
- General preferences (not financial/health related)

### Special Rule for Fintech Companies

**In a fintech context, assume financial data is involved unless clearly stated otherwise.**

If the case mentions:
- Customers/users of a fintech product
- Transactions, payments, loans, credit
- Banking, financial services
- Account information

→ Assume sensitive personal data (financial) is **likely** or **potentially** involved.

Always flag for confirmation if not explicitly stated.

## Reasoning Framework

### Good Reasoning Examples

**Example 1: Clear Personal Data**
```
Classification: Personal Data - Yes
Reasoning: The case explicitly mentions sharing "customer name, phone number, and email" 
which are direct identifiers of individuals. These clearly constitute personal data.
```

**Example 2: Likely Personal Data**
```
Classification: Personal Data - Likely
Reasoning: The case mentions sharing "user profile information" and "transaction history" 
without specifying exact fields. These terms typically include personal identifiers. 
Confirmation of specific data fields is needed.
```

**Example 3: Sensitive Data in Fintech**
```
Classification: Sensitive Personal Data - Yes
Reasoning: The case involves "transaction history" and "credit scores" for fintech 
customers. Both are financial data, which is considered sensitive personal data. 
Transaction history reveals financial behavior and credit scores are explicitly sensitive.
```

**Example 4: Potentially Sensitive**
```
Classification: Sensitive Personal Data - Potentially
Reasoning: The case mentions "user behavioral data" in the context of a loan application 
platform. Depending on what behaviors are tracked, this could reveal financial situation 
or creditworthiness, making it potentially sensitive. Need confirmation of what specific 
behaviors are tracked.
```

### Bad Reasoning Examples (Avoid These)

❌ **Too vague:**
```
Classification: Personal Data - Yes
Reasoning: Because it involves customers.
```
Better: Specify WHAT customer information is involved and WHY it's personal data.

❌ **Assumptions without evidence:**
```
Classification: Sensitive Personal Data - Yes
Reasoning: It's a fintech company so it must be sensitive.
```
Better: Identify the SPECIFIC data categories that make it sensitive.

❌ **Circular reasoning:**
```
Classification: Personal Data - Yes
Reasoning: The data is personal because it's about persons.
```
Better: Explain WHICH data elements identify individuals.

## Confidence Level Assessment

Always indicate your confidence level in the classification:

### High Confidence
- Specific data fields are explicitly listed
- Data categories are clearly described
- Context makes classification obvious

**Indicator phrases:**
- "The case explicitly states..."
- "Specific fields mentioned include..."
- "It is clear that..."

### Medium Confidence
- General descriptions provided but not detailed
- Reasonable inference based on context
- Standard patterns recognized

**Indicator phrases:**
- "Based on the description of [X], this likely includes..."
- "In the context of [fintech/etc.], this typically involves..."
- "The mention of [Y] suggests..."

### Low Confidence
- Vague descriptions
- Critical information missing
- Multiple interpretations possible

**Indicator phrases:**
- "Without more details, it's difficult to confirm..."
- "The description is unclear about..."
- "This could be [X] or [Y] depending on..."

**When confidence is low → Always mark as "Need Confirmation"**

## Output Format for This Skill

```markdown
### PRIVACY CLASSIFICATION

#### Personal Data Assessment

**Classification:** Yes / Likely / Potentially / No / Need Confirmation

**Reasoning:**
[Explain what indicators led to this classification. Be specific about which data elements 
or descriptions led to this conclusion. Quote relevant parts of the case description.]

**Confidence Level:** High / Medium / Low

**Specific Data Elements Identified:**
- [List the personal data categories you identified]
- [Be as specific as possible]

---

#### Sensitive Personal Data Assessment

**Classification:** Yes / Potentially / Likely Not / No / Need Confirmation

**Reasoning:**
[Explain what indicators led to this classification. For fintech cases, specifically 
address financial data. Be explicit about why certain data is considered sensitive.]

**Confidence Level:** High / Medium / Low

**Specific Sensitive Data Categories:**
- [List the sensitive categories: financial, biometric, health, etc.]
- [Explain why each is sensitive]

---

#### Confirmation Needed

**If classification is uncertain, list specific questions:**
- [ ] What specific data fields will be shared/processed?
- [ ] Does this include financial transaction details?
- [ ] Does this include authentication information?
- [ ] [Other specific questions based on case]
```

## Decision Trees

### Decision Tree 1: Is Personal Data Involved?

```
Does the case mention specific identifiers (name, email, phone, ID, user ID)?
├─ Yes → Classification: "Yes" (High confidence)
└─ No → Continue

Does the case mention "customer data", "user information", "account data"?
├─ Yes → Classification: "Likely" (Medium confidence, needs field confirmation)
└─ No → Continue

Does the case mention data that could be linked to individuals (device data, session data)?
├─ Yes → Classification: "Potentially" (Low-Medium confidence, needs clarification)
└─ No → Continue

Is the data truly aggregated/anonymized with no identifiers?
├─ Yes → Classification: "No" (but confirm it cannot be de-anonymized)
└─ Unclear → Classification: "Need Confirmation"
```

### Decision Tree 2: Is Sensitive Personal Data Involved?

```
For FINTECH companies:

Does the case mention financial data (transactions, credit, accounts, payments)?
├─ Yes → Classification: "Yes" or "Potentially" (High confidence for sensitive)
└─ No → Continue

Does the case mention biometric, health, or government ID data?
├─ Yes → Classification: "Yes" (High confidence)
└─ No → Continue

Does the case mention authentication data (passwords, security codes)?
├─ Yes → Classification: "Yes" (High confidence)
└─ No → Continue

Is only basic contact information mentioned (name, email, phone)?
├─ Yes → Classification: "Likely Not" (personal but not sensitive)
└─ No → Continue

Is data category unclear?
└─ Classification: "Need Confirmation"
```

## Common Scenarios

### Scenario 1: Marketing Use Case
**Case:** "Share name and email with marketing partner in Vietnam"

**Classification:**
- Personal Data: Yes (High confidence) - Name and email are direct identifiers
- Sensitive Data: No (High confidence) - These are basic contact details, not sensitive

### Scenario 2: Transaction Analysis
**Case:** "Send transaction data to analytics vendor for spending pattern analysis"

**Classification:**
- Personal Data: Likely (Medium confidence) - Transaction data usually linkable to users
- Sensitive Data: Potentially (Medium confidence) - Financial transactions are sensitive, need to confirm if amounts/details included

### Scenario 3: Cloud Storage
**Case:** "Store customer information on AWS Singapore"

**Classification:**
- Personal Data: Likely (Medium confidence) - "Customer information" is vague but typically includes identifiers
- Sensitive Data: Need Confirmation (Low confidence) - Depends on what customer information includes

### Scenario 4: Aggregated Reports
**Case:** "Share monthly report showing total number of transactions and average transaction value by region"

**Classification:**
- Personal Data: No (High confidence) - If truly aggregated with no identifiers
- Sensitive Data: No (High confidence) - Aggregated statistics are not sensitive
- **But ask for confirmation:** Is the data truly anonymized? Are group sizes large enough to prevent re-identification?

## Integration with Other Skills

After classifying personal/sensitive data:
- Feed results to **Transfer Classification Skill** (affects risk level)
- Feed results to **Checklist Generation Skill** (determines which checklist)
- Feed results to **Privacy Summary Skill** (key component of summary)

If sensitive data is involved:
- Automatically flag for human review
- Escalate to higher risk category
- Require enhanced security measures

---

Remember: In ambiguous cases, it's better to classify as personal/sensitive and confirm later than to miss potential privacy risks.
