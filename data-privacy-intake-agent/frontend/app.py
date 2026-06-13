import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Sample cases
SAMPLE_CASES = {
    "No Personal Data": """Team tôi muốn chia sẻ báo cáo tổng hợp số lượng giao dịch theo tháng cho đối tác, không có user ID, số điện thoại, email hoặc thông tin định danh khách hàng. Báo cáo chỉ bao gồm tổng số giao dịch, giá trị trung bình và phân bố theo khu vực. Đối tác là công ty phân tích thị trường tại Việt Nam.""",
    
    "Domestic Sharing": """Team tôi muốn chia sẻ họ tên, số điện thoại và lịch sử giao dịch của khách hàng cho vendor tại Việt Nam để chăm sóc khách hàng. Vendor sẽ gọi điện và hỗ trợ khách hàng về các giao dịch của họ. Dữ liệu bao gồm: tên, số điện thoại, email, user ID, lịch sử giao dịch (ngày, số tiền, loại giao dịch) trong 6 tháng gần nhất. Vendor có khoảng 50 nhân viên chăm sóc khách hàng tại văn phòng Hà Nội. Chúng tôi chưa có DPA với vendor này.""",
    
    "Cross-Border Transfer": """Team tôi muốn gửi user_id, số điện thoại, transaction history và credit score cho vendor ở Singapore qua API để chấm điểm tín dụng. Vendor này là CreditTech Pte Ltd, có văn phòng tại Singapore và dữ liệu sẽ được lưu trên AWS Singapore. Team support của vendor có thể truy cập từ Singapore và Philippines. Dữ liệu bao gồm: user_id, số điện thoại, email, lịch sử giao dịch 12 tháng, số dư tài khoản, credit score hiện tại. Khoảng 30,000 khách hàng sẽ bị ảnh hưởng. Chúng tôi đã có draft contract nhưng chưa có DPA. Vendor có ISO 27001 certification."""
}

# Page configuration
st.set_page_config(
    page_title="Data Privacy Intake Agent",
    page_icon="🔒",
    layout="wide",
)

# Title and description
st.title("🔒 Data Privacy Intake Agent")

st.markdown("""
This agent helps Biz/Product teams prepare privacy review requests before submission to the Data Privacy team.

**What this agent does:**
- Classifies data privacy cases (domestic vs cross-border, personal data vs sensitive data)
- Identifies missing information
- Generates required document checklist
- Creates data flow diagrams
- Provides summary for Data Privacy reviewers
- Suggests email to request additional information
""")

st.divider()

# Sidebar with sample cases
with st.sidebar:
    st.header("📋 Sample Cases")
    st.markdown("Click a sample case to load it:")
    
    for case_name, case_text in SAMPLE_CASES.items():
        if st.button(case_name, key=f"sample_{case_name}", use_container_width=True):
            st.session_state.case_description = case_text
    
    st.divider()
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Version:** 1.0.0 MVP  
    **Backend:** FastAPI  
    **LLM:** Configurable via API
    
    **Note:** This is a preliminary analysis tool. Final approval requires human review by the Data Privacy legal team.
    """)

# Main input area
st.header("📝 Describe Your Case")

case_description = st.text_area(
    "Enter your data privacy case description:",
    value=st.session_state.get("case_description", ""),
    height=150,
    placeholder="Example: We want to share customer transaction data with Vendor XYZ for analytics purposes...",
    key="case_input"
)

# Update session state
if case_description:
    st.session_state.case_description = case_description

# Analyze button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    analyze_button = st.button("🔍 Analyze Case", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.session_state.case_description = ""
    st.rerun()

# Analysis section
if analyze_button:
    if not case_description.strip():
        st.error("⚠️ Please enter a case description before analyzing.")
    else:
        with st.spinner("🤖 Analyzing your case... This may take 10-30 seconds..."):
            try:
                # Call backend API
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": case_description},
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "No response from agent")
                    
                    st.success("✅ Analysis Complete!")
                    st.divider()
                    
                    # Display result
                    st.header("📊 Analysis Result")
                    
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
                        label="📥 Download Analysis",
                        data=answer,
                        file_name="privacy_analysis.md",
                        mime="text/markdown",
                        use_container_width=False
                    )
                    
                else:
                    st.error(f"❌ Error: Backend returned status code {response.status_code}")
                    st.error(f"Details: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Please ensure the backend is running.")
                st.info(f"Backend URL: {BACKEND_URL}")
                st.code("docker-compose up -d", language="bash")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The analysis is taking longer than expected. Please try again.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p><strong>Important Notice:</strong> This preliminary analysis is provided to help you prepare documentation. 
    Final approval must be obtained from the Data Privacy legal team after human review.</p>
    <p>Data Privacy Intake Agent MVP | Built for AI Competition</p>
</div>
""", unsafe_allow_html=True)
