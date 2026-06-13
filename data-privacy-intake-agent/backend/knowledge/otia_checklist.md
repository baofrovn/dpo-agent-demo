# Offshore Transfer Impact Assessment (OTIA) Checklist

## Purpose
This checklist applies to **cross-border data transfer cases** where personal data is transferred to, stored in, or accessed from **outside Vietnam**.

Use this checklist when:
- Transferring data to a partner/vendor located outside Vietnam
- Storing data on servers/cloud infrastructure outside Vietnam
- Granting access to data by personnel located outside Vietnam
- Using services that route data through systems outside Vietnam

This is in addition to (not instead of) the domestic DPA checklist requirements.

---

## Critical Requirements for Cross-Border Transfer

### 1. Name and Details of Data Recipient
- [ ] **Full legal name of the receiving entity**
  - Description: Complete company/organization name that will receive data
  - Why it's needed: Must identify who is responsible for data protection abroad
  - What to provide:
    - Legal entity name (as registered)
    - Company registration number
    - Type of entity (corporation, partnership, government agency, etc.)
    - Relationship to your company (vendor, partner, subsidiary, etc.)

### 2. Country/Jurisdiction of Data Recipient
- [ ] **Specific country where data will be transferred/stored/accessed**
  - Description: Geographic location of data recipient and data storage
  - Why it's needed: Different countries have different data protection laws
  - What to provide:
    - Primary country of recipient's operations
    - Country where data will be stored
    - Countries from which data may be accessed
  - ⚠️ **High-risk countries**: Those without adequate data protection laws or with government surveillance concerns
  - 🟢 **Lower-risk countries**: EU/EEA, Singapore, Japan, South Korea (with adequacy recognition or strong laws)

### 3. Purpose of Cross-Border Transfer
- [ ] **Specific business reason for transferring data outside Vietnam**
  - Description: Why data must leave Vietnam
  - Why it's needed: Cross-border transfer must be necessary and proportionate
  - What to provide: Clear justification such as:
    - "To use [vendor name]'s cloud infrastructure for data storage"
    - "To enable global customer support services"
    - "To perform advanced analytics using [vendor]'s platform"
    - "To comply with group-wide IT systems"
  - ⚠️ **Red flag**: "For convenience" or unclear business necessity

### 4. Categories of Personal Data to be Transferred
- [ ] **Exhaustive list of data fields that will leave Vietnam**
  - Description: Exact personal data that will cross borders
  - Why it's needed: Must minimize cross-border data flows
  - What to provide: Detailed list such as:
    - Identification data (name, email, phone, user ID)
    - Transaction data (amounts, dates, merchant names)
    - Financial data (account numbers, credit scores)
    - Behavioral data (usage patterns, preferences)
  - ⚠️ **Critical**: If sensitive data (financial, biometric, health) will be transferred, this requires highest level of review

### 5. Data Subject Groups Affected
- [ ] **Who will be affected by this cross-border transfer**
  - Description: Categories of users/customers whose data will be transferred
  - Why it's needed: Must assess impact on different user groups
  - What to provide: Description such as:
    - "All active customers" (specify number)
    - "Loan applicants only" (specify number)
    - "Premium/VIP customers" (specify number)
    - "Customers who consented to international transfers"
  - ⚠️ **Important**: Children's data (under 16) requires special handling

### 6. Mechanism of Data Transfer
- [ ] **How data will technically cross the border**
  - Description: Technical method of data transfer
  - Why it's needed: Different mechanisms have different risks
  - What to provide: Detailed description such as:
    - API integration (specify protocol, encryption)
    - File transfer (specify format, encryption, frequency)
    - Database replication (specify method, encryption)
    - Email (specify encryption, who has access)
    - Cloud storage (specify provider, region, access controls)
    - Direct access to Vietnam systems (specify VPN, access controls)
  - Security requirements:
    - Must use encryption in transit (TLS 1.2+)
    - Must use secure authentication
    - Must log all transfers

### 7. Data Retention Period
- [ ] **How long data will be stored outside Vietnam**
  - Description: Duration of data storage abroad
  - Why it's needed: Longer retention = higher risk
  - What to provide:
    - "Data will be stored for [X] months/years"
    - "Data will be deleted within [X] days after purpose is fulfilled"
    - "Data will be retained in accordance with [specific legal requirement]"
  - Best practice: Shortest period necessary for the purpose

### 8. Data Processing Agreement with Cross-Border Clauses
- [ ] **DPA specifically addresses cross-border transfer**
  - Description: Contract includes provisions for international data transfer
  - Why it's needed: Standard DPA may not cover cross-border requirements
  - What to provide: DPA with specific clauses on:
    - Acknowledgment that data crosses borders
    - Recipient's commitments to Vietnam data protection principles
    - Applicable law and jurisdiction
    - Standard Contractual Clauses (SCCs) if applicable
    - Compliance with recipient country's laws
    - Handling of conflicts between laws
  - ⚠️ **Required**: This is not optional for cross-border transfers

### 9. Security Measures During Transfer and Storage
- [ ] **Enhanced security for cross-border data flows**
  - Description: Technical and organizational measures to protect data abroad
  - Why it's needed: Higher risk of unauthorized access when data leaves Vietnam
  - What to provide: Detailed security measures including:
    - **Encryption**:
      - Data in transit: TLS 1.2+ or equivalent
      - Data at rest: AES-256 or equivalent
    - **Access Controls**:
      - Multi-factor authentication required
      - Role-based access controls
      - Least privilege principle
      - Access logging and monitoring
    - **Network Security**:
      - Firewall protection
      - Intrusion detection/prevention
      - DDoS protection
    - **Physical Security**:
      - Secure data centers
      - Access control to facilities
      - 24/7 monitoring
    - **Certifications**:
      - ISO 27001 (information security)
      - SOC 2 Type II (security, availability, confidentiality)
      - ISO 27018 (cloud privacy)
      - Other relevant certifications
  - Minimum acceptable: Encryption (transit + rest) + MFA + access logs + reputable data center

### 10. Sub-Processor List and Locations
- [ ] **All sub-contractors and their countries disclosed**
  - Description: Any other parties that will access data and their locations
  - Why it's needed: Sub-processors may be in different countries with different risks
  - What to provide: For each sub-processor:
    - Name of sub-processor
    - Country/location
    - What they do with the data
    - Security measures they implement
    - Whether there's a DPA with them
  - ⚠️ **Critical**: Each additional country/sub-processor increases complexity

### 11. Data Subject Rights Handling Mechanism
- [ ] **How users can exercise rights regarding their data abroad**
  - Description: Process for users to access, correct, delete, or object to processing of data stored abroad
  - Why it's needed: Users' rights must be protected regardless of data location
  - What to provide: Description of:
    - How users submit requests (email, web form, etc.)
    - Timeframe for responding (e.g., 30 days)
    - How recipient will facilitate rights requests
    - How data will be corrected/deleted in foreign systems
    - Point of contact for users
  - Typical clause: "Recipient will assist Company in responding to data subject rights requests within 15 business days"

### 12. Incident Response and Breach Notification Mechanism
- [ ] **Clear process for handling data breaches abroad**
  - Description: What happens if data is breached in the foreign country
  - Why it's needed: Breaches abroad may be harder to detect and respond to
  - What to provide: Incident response plan covering:
    - Recipient must notify Company within 72 hours of discovery
    - Detailed incident information requirements
    - Cooperation in breach investigation
    - Notification to Vietnamese authorities (Company's responsibility)
    - Notification to affected users
    - Remediation measures
    - Liability and indemnification
  - ⚠️ **Important**: Vietnamese data protection authority must be notified per local law

### 13. Evidence of User Consent or Notice for Cross-Border Transfer
- [ ] **Users are informed and have consented (if required)**
  - Description: Users must know their data is going abroad
  - Why it's needed: Cross-border transfer of personal data may require explicit consent
  - What to provide:
    - Updated privacy policy mentioning cross-border transfer
    - Specific countries where data will be transferred
    - Screenshot of consent mechanism (if consent is required)
    - Evidence of how users are notified
    - Opt-out mechanism (if applicable)
  - When consent is required:
    - Transfer of sensitive personal data
    - Transfer to countries without adequate protection
    - Transfer for purposes not disclosed at collection
  - When notice is sufficient:
    - Transfer necessary for contract performance
    - Transfer to countries with adequate protection
    - Transfer disclosed in privacy policy at collection

### 14. Assessment of Recipient's Data Protection Level
- [ ] **Evaluation of data protection standards in recipient country**
  - Description: Analysis of whether recipient country has adequate data protection
  - Why it's needed: Transfers to countries with weak protection require extra safeguards
  - What to provide: Assessment covering:
    - **Adequacy Decision**: Does Vietnam recognize recipient country as adequate?
    - **Legal Framework**: What data protection laws exist in recipient country?
    - **Enforcement**: Are data protection laws enforced?
    - **Government Access**: Can government access data without due process?
    - **Redress**: Can users seek legal remedies in recipient country?
    - **Recipient's Practices**: Does recipient comply with international standards?
  - Risk levels:
    - 🟢 **Low risk**: EU/EEA countries, countries with adequacy decisions
    - 🟡 **Medium risk**: Countries with data protection laws (Singapore, Japan, South Korea)
    - 🔴 **High risk**: Countries without data protection laws, countries with broad surveillance
  - Mitigating measures for high-risk countries:
    - Strong contractual commitments
    - Enhanced encryption and security
    - Limited data transfer (only essential data)
    - Regular audits
    - Consider alternative solutions within Vietnam

---

## Additional Requirements Based on Risk Level

### For High-Risk Transfers (Sensitive Data or High-Risk Countries)
- [ ] Executive approval obtained
- [ ] Privacy Impact Assessment (PIA) conducted
- [ ] Alternative solutions within Vietnam evaluated and documented
- [ ] Enhanced security measures implemented (beyond minimum)
- [ ] Explicit user consent obtained (not just notice)
- [ ] Regular audits scheduled (at least annually)
- [ ] Exit strategy documented (how to bring data back to Vietnam if needed)

### For Medium-Risk Transfers (Non-Sensitive Data to Moderate-Risk Countries)
- [ ] Management approval obtained
- [ ] Standard security measures verified
- [ ] Users notified in privacy policy
- [ ] Periodic reviews scheduled (every 2 years)

### For Lower-Risk Transfers (Non-Sensitive Data to Low-Risk Countries)
- [ ] Standard approval process followed
- [ ] Basic security requirements met
- [ ] Privacy policy updated

---

## Legal Basis Assessment

Which legal basis applies to this cross-border transfer?

- [ ] **Consent**: User has explicitly agreed to cross-border transfer
- [ ] **Contract Performance**: Transfer is necessary to provide service user requested
- [ ] **Legal Obligation**: Transfer required by law
- [ ] **Public Interest**: Transfer necessary for important public interest
- [ ] **Legitimate Interest**: Transfer necessary for legitimate business interest (must balance against user rights)
- [ ] **Other**: [Specify]

**Recommended**: For most cross-border transfers, use **Consent** or **Contract Performance** as legal basis.

---

## Transfer Safeguards Checklist

Which safeguards are in place for this cross-border transfer?

- [ ] **Standard Contractual Clauses (SCCs)**: Pre-approved contract terms for international transfers
- [ ] **Binding Corporate Rules (BCRs)**: Group-wide data protection policies (for transfers within corporate group)
- [ ] **Adequacy Decision**: Recipient country recognized as providing adequate protection
- [ ] **Specific Consent**: Users explicitly consented to this specific transfer
- [ ] **Certification Schemes**: Recipient certified under recognized privacy frameworks (e.g., APEC CBPR)
- [ ] **Code of Conduct**: Recipient adheres to approved industry code of conduct

**Minimum requirement**: At least ONE safeguard must be in place.

---

## Cross-Border Transfer Risk Matrix

| Risk Factor | Low Risk | Medium Risk | High Risk |
|-------------|----------|-------------|-----------|
| **Data Type** | Name, email only | User ID, transaction data | Financial data, biometric, health |
| **Recipient Country** | EU/EEA, Singapore | Japan, South Korea, Australia | Countries without data protection laws |
| **Volume** | < 1,000 users | 1,000 - 10,000 users | > 10,000 users |
| **Retention** | < 1 year | 1-5 years | > 5 years |
| **Recipient Security** | ISO 27001 + SOC 2 | Some certifications | No certifications |
| **Government Access** | Due process required | Limited government access | Broad government surveillance |

**Overall Risk**: Count the number of high-risk factors above.
- **0-1 high-risk factors**: Proceed with standard approvals
- **2-3 high-risk factors**: Requires senior management approval + enhanced safeguards
- **4+ high-risk factors**: Requires executive approval + Privacy Impact Assessment + consider alternatives

---

## Submission Checklist for Data Privacy Team

Before submitting for cross-border transfer review, ensure you have:

- [ ] Completed ALL 14 items above (not just some)
- [ ] Attached draft DPA with cross-border clauses
- [ ] Provided evidence of security measures (certifications, audit reports)
- [ ] Assessed recipient country's data protection level
- [ ] Identified legal basis for transfer
- [ ] Identified applicable safeguards
- [ ] Updated privacy policy draft to mention cross-border transfer
- [ ] Obtained consent mechanism (if required)
- [ ] Calculated risk level
- [ ] Documented why this transfer is necessary
- [ ] Explored alternatives within Vietnam
- [ ] Prepared for 2-4 weeks review time (cross-border cases take longer)

---

## Common Issues and How to Avoid Them

**Issue 1: "We didn't know this was cross-border transfer"**
- Solution: Always check where vendor is located, where servers are, and where data can be accessed from

**Issue 2: "Vendor is in Vietnam but uses AWS Singapore"**
- Solution: This IS cross-border transfer. Focus on where data is stored/accessed, not where vendor is registered

**Issue 3: "We already signed the contract without DPA"**
- Solution: Negotiate an amendment to add DPA clauses. Do not proceed without DPA.

**Issue 4: "Vendor says their privacy policy is enough"**
- Solution: Not sufficient. A bilateral DPA is required by law.

**Issue 5: "Users already agreed to our privacy policy"**
- Solution: Check if your privacy policy specifically mentions cross-border transfer to [specific country]. If not, update it.

**Issue 6: "This is standard industry practice"**
- Solution: Industry practice doesn't override legal requirements. Full compliance is needed.

---

## Timeline Expectations

Cross-border transfer reviews typically take longer than domestic cases:

- **Simple case** (non-sensitive data, low-risk country, existing DPA template): 2 weeks
- **Standard case** (sensitive data, medium-risk country, standard vendor): 3-4 weeks
- **Complex case** (high-risk country, new vendor, large volume): 6-8 weeks or more

Plan accordingly and submit early.

---

## Next Steps After Approval

1. **Execute DPA** with cross-border clauses
2. **Update privacy policy** and obtain user consent (if required)
3. **Implement security measures** as agreed
4. **Document the transfer** in cross-border transfer registry
5. **Set up monitoring** and periodic reviews
6. **Train team members** on cross-border data handling procedures
7. **Establish incident response** plan with clear escalation path

---

**Remember**: Cross-border data transfer is high-risk. Do not proceed without complete documentation and Data Privacy team approval.
