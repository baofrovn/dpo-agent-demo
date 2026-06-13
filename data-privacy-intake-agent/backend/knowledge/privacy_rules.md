# Privacy Rules and Definitions

## 1. What is Personal Data?

**Personal Data (Dữ liệu cá nhân)** is any information relating to an identified or identifiable natural person (data subject).

### Categories of Personal Data

#### Direct Identifiers
Information that directly identifies a person:
- Full name (first name, last name, middle name)
- Phone number (mobile, landline)
- Email address
- National ID number (CMND/CCCD)
- Passport number
- Social security number
- Driver's license number
- Tax identification number

#### Indirect Identifiers
Information that can identify a person when combined with other data:
- User ID, customer ID, account ID
- Device ID, IMEI, MAC address
- IP address
- Cookie identifiers, advertising IDs
- Order number or transaction ID (when linkable to a person)
- Account numbers

#### Behavioral and Usage Data
- App usage patterns
- Browsing history
- Search history
- Purchase history
- Product preferences
- Click streams
- Session recordings
- Feature usage analytics

#### Location Data
- GPS coordinates
- Real-time location tracking
- Home address
- Work address
- Frequently visited locations
- Check-in data
- Geolocation history

#### Transaction and Financial Data
- Transaction history
- Payment records
- Order history
- Account balance
- Spending patterns
- Credit history
- Loan records

#### Communication Data
- Messages, SMS, chat logs
- Email content
- Call logs, call recordings
- Contact lists
- Social media interactions

## 2. What is Sensitive Personal Data?

**Sensitive Personal Data (Dữ liệu cá nhân nhạy cảm)** requires heightened protection due to higher privacy risks.

### Categories of Sensitive Personal Data

#### Financial Information
- **Bank account numbers**
- **Credit card numbers, debit card numbers**
- **Credit scores, credit ratings**
- **Income level, salary information**
- **Asset information, investment portfolios**
- **Loan details, debt information**
- **Transaction history with financial details**
- **Payment methods and financial authentication**

#### Authentication and Security Data
- Passwords, PINs, security codes
- Biometric data (fingerprints, facial recognition, iris scans, voice prints)
- Security questions and answers
- Two-factor authentication codes
- Encryption keys

#### Health and Medical Data
- Medical records, health conditions
- Prescription information, medication history
- Lab results, diagnostic information
- Hospital visit records
- Health insurance information
- Mental health data
- Disability information

#### Government-Issued Identification
- National ID numbers (CMND/CCCD numbers)
- Passport numbers
- Social security numbers
- Tax identification numbers
- Driver's license numbers

#### Children's Data
- Personal data of individuals under 16 years old
- Student records
- Parental consent information

#### Other High-Risk Data
- Ethnic origin, race
- Political opinions
- Religious or philosophical beliefs
- Trade union membership
- Sexual orientation
- Criminal records or allegations

## 3. Data Classification Rules

### Rule 1: If In Doubt, It's Personal Data
When uncertain whether data qualifies as personal data, treat it as personal data and request confirmation from the Data Privacy team.

### Rule 2: Aggregated Data May Not Be Personal Data
- If data is truly aggregated and anonymized (e.g., "total number of transactions per month" with no identifiers), it may not be personal data
- However, if the aggregation can be reversed or if the group size is small enough to identify individuals, it remains personal data
- Always confirm that aggregated data cannot be de-anonymized

### Rule 3: "User ID" and Similar Identifiers Are Personal Data
- User IDs, customer IDs, device IDs are personal data because they can identify individuals
- Even pseudonymized or hashed identifiers are personal data if they can be linked back to individuals

### Rule 4: Financial Data Is Always Sensitive
Any data related to financial transactions, accounts, credit, payments, or economic status is considered sensitive personal data for fintech companies.

### Rule 5: Multiple Non-Sensitive Data Points Can Become Sensitive
- A single data point may seem non-sensitive, but combining multiple data points can reveal sensitive information
- Example: Location + time + purchase history can reveal sensitive behavioral patterns

## 4. Cross-Border Transfer Recognition Rules

### Rule 1: Recipient Location
If the recipient, partner, vendor, or third party is located outside Vietnam, it is a cross-border transfer.

**Indicators:**
- Vendor company registered outside Vietnam
- Vendor headquarters outside Vietnam
- Contracting entity outside Vietnam

### Rule 2: Server/Infrastructure Location
If data is stored on servers or cloud infrastructure located outside Vietnam, it is a cross-border transfer.

**Indicators:**
- AWS regions outside Vietnam (e.g., Singapore, Japan, US)
- Google Cloud, Azure, or other cloud providers with non-Vietnam regions
- Data centers outside Vietnam
- CDN with edge servers outside Vietnam

### Rule 3: Data Access Location
If personnel or systems located outside Vietnam can access the data, it is a cross-border transfer.

**Indicators:**
- Support teams based outside Vietnam
- Development teams outside Vietnam with production access
- Remote access from outside Vietnam
- API endpoints accessible from outside Vietnam

### Rule 4: Data Transmission Route
If data transits through systems or networks outside Vietnam, even temporarily, it may be considered cross-border transfer.

**Indicators:**
- API calls routed through foreign servers
- Email or file transfers via foreign email providers
- Data synchronization with foreign systems

### Rule 5: When Location Is Unclear
If any of the following is unclear, mark as "Need Confirmation" and ask the business team:
- Where is the vendor located?
- Where are the servers located?
- Where is data stored?
- Who has access to data and where are they located?
- What is the data transmission path?

## 5. Human Review Requirements

### Mandatory Human Review Cases

**Category 1: Sensitive Personal Data**
- Any case involving financial data (transaction history, credit scores, bank accounts)
- Any case involving authentication data (passwords, biometric data)
- Any case involving health data
- Any case involving children's data
- Any case involving government ID numbers

**Category 2: Cross-Border Transfers**
- Any transfer of personal data outside Vietnam
- Any storage of personal data on foreign servers
- Any access to personal data by foreign personnel
- Any data sharing with foreign partners/vendors

**Category 3: High-Risk Operations**
- New or unfamiliar use cases
- Large-scale data processing (affecting > 10,000 data subjects)
- Automated decision-making or profiling
- Data sharing with multiple third parties
- Permanent or long-term data transfers (> 5 years retention)

**Category 4: Unclear or Incomplete Information**
- Purpose of processing is unclear
- Data categories are not specified
- Recipient details are missing
- Security measures are not documented
- No existing contract or DPA

**Category 5: Regulatory Uncertainty**
- New regulations or legal requirements
- Uncertain compliance requirements
- Potential conflict with other laws
- Novel business models or technologies

### Optional Human Review Cases

**Low-Risk Cases:**
- No personal data involved (confirmed aggregated/anonymized data)
- Internal data processing with no external sharing
- Well-established processes with existing approvals
- Technical changes with no new privacy implications

## 6. Consent and Notice Requirements

### When Consent May Be Required
- Collection of sensitive personal data
- Cross-border transfer of personal data
- Sharing data with third parties for new purposes
- Using data for purposes beyond original collection purpose
- Automated decision-making or profiling

### When Notice Is Required
- At the point of data collection
- Before any new use of data
- Before sharing data with third parties
- Before cross-border transfer

### What Notice Should Include
- Identity of data controller
- Purpose of data processing
- Categories of personal data
- Recipients or categories of recipients
- Cross-border transfer (if applicable)
- Retention period
- Data subject rights
- How to exercise rights

## 7. Data Retention Rules

### General Principle
Personal data should not be retained longer than necessary for the purpose for which it was collected.

### Recommended Maximum Retention Periods
- **Transaction data**: 5-7 years (for accounting and legal requirements)
- **Customer account data**: While account is active + 2 years after closure
- **Marketing data**: While consent is valid + 6 months after consent withdrawal
- **Log data**: 6-12 months
- **Backup data**: Same retention as primary data

### Factors to Consider
- Legal and regulatory requirements
- Business necessity
- Data subject rights
- Storage costs and security risks

## 8. Security Requirements

### Minimum Security Measures
- Encryption in transit (TLS/SSL)
- Encryption at rest for sensitive data
- Access controls and authentication
- Logging and monitoring
- Regular security assessments
- Incident response plan
- Data backup and recovery

### Enhanced Security for Sensitive Data
- Multi-factor authentication
- Data masking and tokenization
- Encryption for all data (not just in transit)
- Stricter access controls (least privilege principle)
- Regular penetration testing
- Security certifications (ISO 27001, SOC 2, etc.)

## 9. Third-Party Data Processing

### Key Requirements
- Data Processing Agreement (DPA) must be in place
- Third party must commit to same security standards
- Third party must not use data for own purposes
- Sub-processors must be disclosed and approved
- Incident notification obligations must be defined
- Data subject rights mechanisms must be established

### Red Flags
- No DPA or weak data protection clauses
- Vendor refuses to commit to security standards
- Unclear sub-processor arrangements
- Vendor in jurisdiction with weak data protection laws
- Vendor with history of data breaches

## 10. Common Mistakes to Avoid

1. **Assuming data is anonymous when it's not**: User IDs, device IDs, and IP addresses are personal data
2. **Ignoring cross-border data flows**: Cloud services often involve cross-border transfers
3. **Forgetting about data in transit**: API calls, emails, and file transfers may cross borders
4. **Not documenting the legal basis**: Always document why data processing is lawful
5. **Overlooking sub-processors**: Third parties may use other third parties
6. **Underestimating scope**: Small pilots can quickly scale to affect many users
7. **Not involving Data Privacy team early**: Early review prevents costly delays later

## 11. Decision Tree for Quick Classification

```
Is personal data involved?
├─ No → Low risk, optional privacy review
└─ Yes → Continue to next question

Is sensitive personal data involved (financial, health, biometric, etc.)?
├─ Yes → HIGH RISK → Mandatory human review
└─ No → Continue to next question

Is this cross-border transfer (recipient/server/access outside Vietnam)?
├─ Yes → HIGH RISK → Mandatory human review
└─ No → Continue to next question

Is there an existing DPA and clear documentation?
├─ No → MEDIUM RISK → Human review recommended
└─ Yes → LOW-MEDIUM RISK → Prepare checklist and submit for review
```

---

**Note**: These rules are guidelines for initial classification. The Data Privacy legal team makes all final determinations on compliance requirements.
