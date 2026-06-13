import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Sample cases
SAMPLE_CASES = {
    "🟢 No Personal Data": """Team tôi muốn chia sẻ báo cáo tổng hợp số lượng giao dịch theo tháng cho đối tác, không có user ID, số điện thoại, email hoặc thông tin định danh khách hàng. Báo cáo chỉ bao gồm tổng số giao dịch, giá trị trung bình và phân bố theo khu vực. Đối tác là công ty phân tích thị trường tại Việt Nam.""",
    
    "🟡 Domestic Sharing": """Team tôi muốn chia sẻ họ tên, số điện thoại và lịch sử giao dịch của khách hàng cho vendor tại Việt Nam để chăm sóc khách hàng. Vendor sẽ gọi điện và hỗ trợ khách hàng về các giao dịch của họ. Dữ liệu bao gồm: tên, số điện thoại, email, user ID, lịch sử giao dịch (ngày, số tiền, loại giao dịch) trong 6 tháng gần nhất. Vendor có khoảng 50 nhân viên chăm sóc khách hàng tại văn phòng Hà Nội. Chúng tôi chưa có DPA với vendor này.""",
    
    "🔴 ANT Singapore (Demo)": """Team em muốn hợp tác với đối tác ANT Singapore để tư vấn credit scoring. Dữ liệu dự kiến chia sẻ gồm user_id_hash, transaction_count, transaction_amount, BNPL_payment_amt, device_id. Dữ liệu gửi qua API hằng ngày. Đối tác lưu 12 tháng để tư vấn scoring. Chưa rõ có DPA chưa. Không biết cần chuẩn bị gì trước khi gửi Data Privacy review?"""
}

# Page configuration
st.set_page_config(
    page_title="Privacy Intake Triage Agent",
    page_icon="🔒",
    layout="wide",
)

# Title and description
st.title("🔒 Privacy Intake Triage Agent")
st.caption("Agent sàng lọc yêu cầu chia sẻ dữ liệu trước khi gửi Data Privacy review")

st.markdown("""
Giúp Biz/PO xác định nhanh case chia sẻ dữ liệu thuộc nhóm nào, cần chuẩn bị hồ sơ gì và gửi đúng form cho Data Privacy review.

**Agent này sẽ:**
- Hỏi câu sàng lọc nếu thiếu thông tin
- Phân loại case: Không có dữ liệu cá nhân / Trong nước / Nước ngoài
- Đưa checklist hồ sơ cần chuẩn bị
- Gửi đúng link form (Form A hoặc Form B)
- Tạo summary để Biz copy gửi Data Privacy team
""")

st.divider()

# Sidebar with sample cases
with st.sidebar:
    st.header("📋 Demo Cases")
    st.markdown("Chọn case mẫu để test:")
    
    for case_name, case_text in SAMPLE_CASES.items():
        if st.button(case_name, key=f"sample_{case_name}", use_container_width=True):
            st.session_state.case_description = case_text
    
    st.divider()
    
    st.markdown("### 📝 Hướng dẫn Demo")
    st.markdown("""
    1. Click **🔴 ANT Singapore** (case chính)
    2. Click **Phân Tích Case**
    3. Xem kết quả phân loại
    
    **3 loại kết quả:**
    - Không có dữ liệu cá nhân
    - Chia sẻ trong nước → Form A
    - Chia sẻ nước ngoài → Form B
    """)
    
    st.divider()
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Version:** 1.0.0 MVP  
    **For:** AI Competition Demo
    
    ⚠️ Đây là phân loại sơ bộ. Kết luận cuối cùng cần Data Privacy team xác nhận.
    """)

# Main input area
st.header("📝 Mô Tả Case Của Bạn")

case_description = st.text_area(
    "Nhập mô tả case cần Data Privacy review:",
    value=st.session_state.get("case_description", ""),
    height=150,
    placeholder="Ví dụ: Team em muốn chia sẻ dữ liệu cho đối tác ABC để làm XYZ...",
    key="case_input"
)

# Update session state
if case_description:
    st.session_state.case_description = case_description

# Analyze button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    analyze_button = st.button("🔍 Phân Tích Case", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Xóa", use_container_width=True)

if clear_button:
    st.session_state.case_description = ""
    st.rerun()

# Analysis section
if analyze_button:
    if not case_description.strip():
        st.error("⚠️ Vui lòng nhập mô tả case trước khi phân tích.")
    else:
        with st.spinner("🤖 Agent đang phân tích case... Vui lòng chờ 10-30 giây..."):
            try:
                # Call backend API
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": case_description},
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "Không có phản hồi từ agent")
                    
                    st.success("✅ Phân Tích Hoàn Tất!")
                    st.divider()
                    
                    # Display result
                    st.header("📊 Kết Quả Phân Tích")
                    
                    # Check if answer contains mermaid diagram
                    if "```mermaid" in answer:
                        # Split by mermaid sections
                        parts = answer.split("```mermaid")
                        
                        for i, part in enumerate(parts):
                            if i == 0:
                                # Before first mermaid
                                st.markdown(part)
                            else:
                                # Extract mermaid code and rest
                                if "```" in part:
                                    mermaid_code, rest = part.split("```", 1)
                                    
                                    # Display mermaid diagram
                                    st.markdown("**Data Flow Diagram:**")
                                    st.code(mermaid_code.strip(), language="mermaid")
                                    
                                    # Try to render with mermaid (fallback to code if not supported)
                                    try:
                                        st.markdown(f"""
                                        ```mermaid
                                        {mermaid_code.strip()}
                                        ```
                                        """)
                                    except:
                                        pass
                                    
                                    # Display rest of content
                                    if rest:
                                        st.markdown(rest)
                    else:
                        # No mermaid, just display as markdown
                        st.markdown(answer)
                    
                    # Download button for results
                    st.divider()
                    st.download_button(
                        label="📥 Tải Kết Quả",
                        data=answer,
                        file_name="privacy_analysis.md",
                        mime="text/markdown",
                        use_container_width=False
                    )
                    
                else:
                    st.error(f"❌ Lỗi: Backend trả về status code {response.status_code}")
                    st.error(f"Chi tiết: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Không thể kết nối backend. Vui lòng đảm bảo backend đang chạy.")
                st.info(f"Backend URL: {BACKEND_URL}")
                st.code("docker-compose up -d", language="bash")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout. Phân tích đang mất nhiều thời gian hơn dự kiến. Vui lòng thử lại.")
            except Exception as e:
                st.error(f"❌ Đã xảy ra lỗi: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p><strong>⚠️ Lưu ý quan trọng:</strong> Đây là phân loại sơ bộ từ Agent để giúp bạn chuẩn bị hồ sơ. 
    Kết luận cuối cùng cần được Data Privacy team xác nhận chính thức sau khi review đầy đủ.</p>
    <p>Privacy Intake Triage Agent MVP | Built for AI Competition</p>
</div>
""", unsafe_allow_html=True)
