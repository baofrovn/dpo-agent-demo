# Sample Cases for Demo

This file contains sample cases for testing and demonstrating the Data Privacy Intake Agent.

---

## Case 1: No Personal Data - Aggregated Reporting

**Case Title:** Aggregated Transaction Report Sharing

**Case Description:**
```
Team tôi muốn chia sẻ báo cáo tổng hợp số lượng giao dịch theo tháng cho đối tác, 
không có user ID, số điện thoại, email hoặc thông tin định danh khách hàng. 
Báo cáo chỉ bao gồm tổng số giao dịch, giá trị trung bình và phân bố theo khu vực.
Đối tác là công ty phân tích thị trường tại Việt Nam.
```

**English Translation:**
```
My team wants to share an aggregated monthly transaction report with a partner. 
The report does not contain user IDs, phone numbers, emails, or any customer 
identifying information. The report only includes total transaction count, 
average values, and distribution by region. The partner is a market analysis 
company in Vietnam.
```

**Expected Classification:**
- **Personal Data Involved:** Likely No (if truly aggregated and anonymized)
- **Sensitive Personal Data:** No
- **Transfer Type:** Domestic Sharing
- **Human Review Required:** Optional/Low Risk

**Key Points to Test:**
- Agent should ask for confirmation that data is truly anonymized
- Agent should verify that group sizes are large enough to prevent re-identification
- Agent should use simplified DPA checklist
- Agent should mark as lower risk
- Agent should still require basic DPA for any business data sharing

---

## Case 2: Domestic Sharing - Customer Care Services

**Case Title:** Domestic Vendor for Customer Support

**Case Description:**
```
Team tôi muốn chia sẻ họ tên, số điện thoại và lịch sử giao dịch của khách hàng 
cho vendor tại Việt Nam để chăm sóc khách hàng. Vendor sẽ gọi điện và hỗ trợ 
khách hàng về các giao dịch của họ. Dữ liệu bao gồm: tên, số điện thoại, email, 
user ID, lịch sử giao dịch (ngày, số tiền, loại giao dịch) trong 6 tháng gần nhất. 
Vendor có khoảng 50 nhân viên chăm sóc khách hàng tại văn phòng Hà Nội. 
Chúng tôi chưa có DPA với vendor này.
```

**English Translation:**
```
My team wants to share customer names, phone numbers, and transaction history 
with a vendor in Vietnam for customer care services. The vendor will call and 
support customers regarding their transactions. Data includes: name, phone, 
email, user ID, transaction history (date, amount, transaction type) for the 
last 6 months. The vendor has about 50 customer care staff in their Hanoi office. 
We don't have a DPA with this vendor yet.
```

**Expected Classification:**
- **Personal Data Involved:** Yes (clear identifiers)
- **Sensitive Personal Data:** Potentially Yes (transaction history with amounts is financial data)
- **Transfer Type:** Domestic Sharing
- **Human Review Required:** Yes (due to sensitive financial data)

**Key Points to Test:**
- Agent should identify financial transaction history as sensitive data
- Agent should flag missing DPA as critical gap
- Agent should use DPA checklist (domestic)
- Agent should request security measures from vendor
- Agent should ask about data retention period
- Agent should request evidence of user consent/notice
- Agent should mark as Medium-High risk due to sensitive data
- Agent should create data flow showing: Customer → App → Company Backend → Vendor (Vietnam)

---

## Case 3: Cross-Border Transfer - Credit Scoring

**Case Title:** Cross-Border Transfer for Credit Assessment

**Case Description:**
```
Team tôi muốn gửi user_id, số điện thoại, transaction history và credit score 
cho vendor ở Singapore qua API để chấm điểm tín dụng. Vendor này là CreditTech 
Pte Ltd, có văn phòng tại Singapore và dữ liệu sẽ được lưu trên AWS Singapore. 
Team support của vendor có thể truy cập từ Singapore và Philippines. Dữ liệu 
bao gồm: user_id, số điện thoại, email, lịch sử giao dịch 12 tháng, số dư tài khoản, 
credit score hiện tại. Khoảng 30,000 khách hàng sẽ bị ảnh hưởng. Chúng tôi đã có 
draft contract nhưng chưa có DPA. Vendor có ISO 27001 certification.
```

**English Translation:**
```
My team wants to send user_id, phone number, transaction history, and credit 
score to a vendor in Singapore via API for credit scoring. The vendor is 
CreditTech Pte Ltd, with office in Singapore and data will be stored on AWS 
Singapore. The vendor's support team can access from Singapore and Philippines. 
Data includes: user_id, phone number, email, 12-month transaction history, 
account balance, current credit score. About 30,000 customers will be affected. 
We have a draft contract but no DPA yet. The vendor has ISO 27001 certification.
```

**Expected Classification:**
- **Personal Data Involved:** Yes (clear identifiers)
- **Sensitive Personal Data:** Yes (financial data: transaction history, account balance, credit score)
- **Transfer Type:** Cross-Border Transfer (Singapore + Philippines)
- **Human Review Required:** Yes (cross-border + sensitive data + large scale)

**Key Points to Test:**
- Agent should identify multiple countries (Singapore + Philippines)
- Agent should classify as cross-border based on vendor location, storage location, and access location
- Agent should identify sensitive financial data (transaction history, balance, credit score)
- Agent should flag large scale (30,000 users) as high risk factor
- Agent should use OTIA checklist (cross-border)
- Agent should request DPA with cross-border clauses
- Agent should request evidence of user consent for cross-border transfer
- Agent should ask about Philippines sub-processor details
- Agent should mark as High Risk due to: cross-border + sensitive data + large scale
- Agent should recommend Privacy Impact Assessment
- Agent should request assessment of Singapore and Philippines data protection levels
- Agent should create data flow showing: Customer → App → Backend Vietnam → API → CreditTech Singapore → AWS Singapore, with Philippines access shown
- Agent should recommend executive approval due to risk level and scale

---

## Additional Test Cases (Optional)

### Case 4: Unclear Vendor Location

**Case Description:**
```
Chúng tôi muốn sử dụng CloudAnalytics platform để phân tích hành vi người dùng. 
Dữ liệu bao gồm user_id, hành vi click, thời gian sử dụng app. CloudAnalytics 
là một startup công nghệ nhưng chúng tôi không rõ họ ở đâu.
```

**Expected:** Agent should mark as "Need Confirmation" and ask specific questions about:
- Vendor location
- Server location
- Access location
- Data storage location

---

### Case 5: Vietnamese Vendor Using Foreign Cloud

**Case Description:**
```
Chúng tôi muốn chia sẻ dữ liệu khách hàng với công ty ABC tại Việt Nam. 
Họ sẽ xử lý dữ liệu trên hệ thống cloud của họ. ABC cho biết họ dùng 
AWS nhưng không nói rõ region nào.
```

**Expected:** Agent should:
- Ask which AWS region
- Flag potential cross-border if region is outside Vietnam
- Explain that Vietnamese company using foreign servers still counts as cross-border

---

### Case 6: Email to Foreign Partner

**Case Description:**
```
Team chúng tôi cần gửi danh sách email của 100 khách hàng VIP cho đối tác 
ở Nhật Bản qua email để mời tham gia sự kiện.
```

**Expected:** Agent should classify as cross-border transfer (even though just email)

---

### Case 7: Sensitive Data - Multiple Categories

**Case Description:**
```
Chúng tôi muốn chia sẻ dữ liệu sau với đối tác phân tích: tên, CMND, số điện thoại, 
địa chỉ nhà, lịch sử vay, lịch sử thanh toán, điểm tín dụng, thu nhập ước tính. 
Đối tác ở Việt Nam.
```

**Expected:** Agent should:
- Flag multiple sensitive data categories (CMND, financial history, credit score, income)
- Mark as very high risk even though domestic
- Require extensive security review
- Require enhanced DPA clauses
- Require explicit user consent

---

## Testing Guidelines

When testing with these cases:

1. **Test accuracy of classification:** Does agent correctly identify personal/sensitive data and domestic/cross-border?

2. **Test completeness:** Does agent identify all missing information?

3. **Test appropriate checklist:** Does agent use DPA for domestic and OTIA for cross-border?

4. **Test risk assessment:** Does agent correctly assess risk level?

5. **Test data flow:** Does agent create clear, accurate data flow diagrams?

6. **Test summary quality:** Is the summary concise and actionable?

7. **Test email quality:** Is the email professional, clear, and helpful?

8. **Test handling of ambiguity:** Does agent ask clarifying questions when information is unclear?

---

## Expected Output Quality

For each case, the agent should provide:

✅ **Clear classification** with reasoning
✅ **Specific missing information** (not generic requests)
✅ **Appropriate checklist** (DPA or OTIA)
✅ **Accurate data flow diagram** with correct nodes and flows
✅ **Risk-appropriate summary** with actionable next steps
✅ **Professional email** with specific requests

❌ Should NOT:
- Make assumptions about missing information
- Provide generic/vague requests
- Use wrong checklist type
- Miss obvious sensitive data
- Misclassify cross-border cases
- Be overly technical or use excessive jargon

---

## Demo Script

**For live demo, use this flow:**

1. **Start with Case 1 (No Personal Data):**
   - Show how agent handles low-risk case
   - Demonstrate agent asks for confirmation of anonymization
   - Show simplified output

2. **Then Case 2 (Domestic Sharing):**
   - Show identification of sensitive financial data
   - Demonstrate DPA checklist
   - Show missing information requests

3. **Finally Case 3 (Cross-Border):**
   - Show cross-border classification logic
   - Demonstrate OTIA checklist
   - Show high-risk assessment
   - Highlight comprehensive requirements

**Key message:** Agent helps Biz teams prepare complete submissions, saving Data Privacy team time and ensuring compliance.
