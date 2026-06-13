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

## Case 3: Cross-Border Transfer - Credit Scoring (Demo Case Chính)

**Case Title:** Cross-Border Transfer for Credit Assessment with ANT Singapore

**Case Description (Dùng cho Demo):**
```
Team em muốn hợp tác với đối tác ANT Singapore để tư vấn credit scoring. 
Dữ liệu dự kiến chia sẻ gồm user_id_hash, transaction_count, transaction_amount, 
BNPL_payment_amt, device_id. Dữ liệu gửi qua API hằng ngày. Không biết cần 
chuẩn bị gì trước khi gửi Data Privacy review?
```

**Case Description (Version đầy đủ sau khi Biz bổ sung):**
```
Đối tác ở Singapore. Fields gồm user_id_hash, transaction_count, transaction_amount, 
BNPL_payment_amt, device_id. Gửi qua API hằng ngày. Đối tác lưu 12 tháng để 
tư vấn scoring. Chưa rõ có DPA chưa.
```

**English Translation:**
```
My team wants to partner with ANT Singapore for credit scoring advisory. 
Data to be shared includes user_id_hash, transaction_count, transaction_amount, 
BNPL_payment_amt, device_id. Data sent via API daily. Not sure what to prepare 
before submitting for Data Privacy review?
```

**Expected Agent Flow:**

1. **Agent nhận request** → thấy thiếu một số thông tin
2. **Agent hỏi lại:**
   - Đối tác ở Việt Nam hay nước ngoài?
   - Dữ liệu có liên quan khách hàng không?
   - Đối tác lưu dữ liệu bao lâu?
   - Đã có DPA chưa?
3. **Biz bổ sung thông tin**
4. **Agent phân loại và output đầy đủ**

**Expected Classification Table:**

| Câu hỏi | Kết quả sơ bộ |
|---------|---------------|
| Có chia sẻ dữ liệu cho đối tác không? | Có |
| Có dữ liệu cá nhân không? | Có khả năng có |
| Có dữ liệu cá nhân nhạy cảm không? | Có khả năng có (dữ liệu giao dịch/tài chính/BNPL) |
| Chia sẻ trong nước hay ngoài nước? | Ngoài nước (Singapore) |
| Cần Data Privacy review không? | Có |
| Cần Legal/DPA review không? | Có |
| Cần Security review không? | Có |
| Cần xem xét OTIA không? | Có khả năng cần |

**Expected Form:** Form B – Cross-border Data Sharing Intake Form

**Expected Summary:**
```
Tóm tắt request gửi Data Privacy:
Team Biz/PO dự kiến chia sẻ dữ liệu cho ANT Singapore để phục vụ mục đích tư vấn 
credit scoring. Dữ liệu dự kiến gồm user_id_hash, transaction_count, transaction_amount, 
BNPL_payment_amt, device_id. Dữ liệu được gửi qua API hằng ngày và đối tác dự kiến 
lưu trong 12 tháng. Agent phân loại sơ bộ đây là hoạt động chia sẻ dữ liệu cá nhân 
ra nước ngoài, có khả năng liên quan dữ liệu tài chính/giao dịch nên cần Data Privacy, 
Legal và Security review trước khi triển khai.
```

**Key Points to Test:**
- Agent should recognize this as cross-border (Singapore)
- Agent should identify BNPL data as sensitive financial data
- Agent should use Form B link
- Agent should use OTIA checklist
- Agent should generate summary in the correct format
- Agent should include disclaimer about Privacy team confirmation

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

## Demo Script (Khuyến nghị)

**Cho live demo, sử dụng flow này:**

### Demo Chính: Case ANT Singapore (Cross-Border)

**Bước 1: Biz hỏi Agent**
```
Team em muốn hợp tác với đối tác ANT Singapore để tư vấn credit scoring. 
Dữ liệu dự kiến chia sẻ gồm user_id_hash, transaction_count, transaction_amount, 
BNPL_payment_amt, device_id. Dữ liệu gửi qua API hằng ngày. Không biết cần 
chuẩn bị gì trước khi gửi Data Privacy review?
```

**Bước 2: Agent có thể hỏi lại (nếu cần)**
- Đối tác lưu dữ liệu bao lâu?
- Đã có DPA chưa?

**Bước 3: Biz bổ sung**
```
Đối tác lưu 12 tháng để tư vấn scoring. Chưa rõ có DPA chưa.
```

**Bước 4: Agent output đầy đủ**
- Bảng phân loại
- Checklist hồ sơ
- Link Form B
- Summary để copy gửi Privacy team

### Demo Phụ (Nếu có thời gian)

1. **Case No Personal Data** - Cho thấy Agent xử lý low-risk case
2. **Case Domestic** - Cho thấy Form A và DPA checklist

**Key message:** Agent không thay thế Data Privacy review, mà giúp chuẩn hóa đầu vào, giảm hỏi đáp lặp lại và đưa Privacy vào sớm hơn trước khi sản phẩm triển khai.
