import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Admin Panel - Privacy Chatbot",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Admin Panel")
st.caption("Quản lý System Prompt, Knowledge Base, và Skills của Agent")

# Helper functions
def get_system_prompt():
    """Get current system prompt"""
    try:
        response = requests.get(f"{BACKEND_URL}/system-prompt", timeout=10)
        if response.status_code == 200:
            return response.json().get("content", "")
    except:
        pass
    return ""


def update_system_prompt(content: str):
    """Update system prompt"""
    try:
        response = requests.put(
            f"{BACKEND_URL}/system-prompt",
            json={"content": content},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False


def get_knowledge_files():
    """Get list of knowledge files"""
    try:
        response = requests.get(f"{BACKEND_URL}/knowledge", timeout=10)
        if response.status_code == 200:
            return response.json().get("files", [])
    except:
        pass
    return []


def get_knowledge_file(filename: str):
    """Get content of a knowledge file"""
    try:
        response = requests.get(f"{BACKEND_URL}/knowledge/{filename}", timeout=10)
        if response.status_code == 200:
            return response.json().get("content", "")
    except:
        pass
    return ""


def update_knowledge_file(filename: str, content: str):
    """Update a knowledge file"""
    try:
        response = requests.put(
            f"{BACKEND_URL}/knowledge/{filename}",
            json={"content": content},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False


# Tabs
tab1, tab2, tab3 = st.tabs(["📝 System Prompt", "📚 Knowledge Base", "🎯 Skills"])

# Tab 1: System Prompt
with tab1:
    st.header("📝 System Prompt")
    st.markdown("""
    System prompt là instruction chính cho agent. Nó định nghĩa:
    - Vai trò của agent
    - Cách trả lời
    - Output format
    - Quy tắc chung
    """)
    
    current_prompt = get_system_prompt()
    
    if current_prompt:
        edited_prompt = st.text_area(
            "Edit System Prompt:",
            value=current_prompt,
            height=400,
            key="system_prompt_editor"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.button("💾 Save", use_container_width=True, type="primary"):
                if update_system_prompt(edited_prompt):
                    st.success("✅ System prompt đã được cập nhật!")
                    st.balloons()
                else:
                    st.error("❌ Không thể cập nhật system prompt")
        
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.rerun()
        
        st.divider()
        
        # Preview
        with st.expander("👁️ Preview (First 500 chars)", expanded=False):
            st.code(edited_prompt[:500] + "..." if len(edited_prompt) > 500 else edited_prompt)
    else:
        st.warning("⚠️ Không thể load system prompt. Kiểm tra backend connection.")


# Tab 2: Knowledge Base
with tab2:
    st.header("📚 Knowledge Base")
    st.markdown("""
    Knowledge base chứa các rules, checklists, và definitions mà agent sử dụng để phân tích cases.
    """)
    
    files = get_knowledge_files()
    knowledge_files = [f for f in files if f["type"] == "knowledge"]
    
    if knowledge_files:
        # File selector
        selected_file = st.selectbox(
            "Chọn file để edit:",
            options=[f["name"] for f in knowledge_files],
            format_func=lambda x: f"📄 {x}",
            key="knowledge_file_selector"
        )
        
        if selected_file:
            st.subheader(f"Editing: {selected_file}")
            
            content = get_knowledge_file(selected_file)
            
            if content:
                edited_content = st.text_area(
                    "Edit content:",
                    value=content,
                    height=400,
                    key=f"knowledge_editor_{selected_file}"
                )
                
                col1, col2, col3 = st.columns([1, 1, 4])
                
                with col1:
                    if st.button("💾 Save Changes", use_container_width=True, type="primary", key="save_knowledge"):
                        if update_knowledge_file(selected_file, edited_content):
                            st.success(f"✅ {selected_file} đã được cập nhật!")
                            st.balloons()
                        else:
                            st.error(f"❌ Không thể cập nhật {selected_file}")
                
                with col2:
                    if st.button("🔄 Reload", use_container_width=True, key="reload_knowledge"):
                        st.rerun()
                
                st.divider()
                
                # Info
                st.info(f"""
                **File:** {selected_file}  
                **Type:** Knowledge Base  
                **Lines:** {len(edited_content.splitlines())}  
                **Characters:** {len(edited_content)}
                """)
            else:
                st.warning(f"⚠️ Không thể load content của {selected_file}")
    else:
        st.warning("⚠️ Không tìm thấy knowledge files.")


# Tab 3: Skills
with tab3:
    st.header("🎯 Agent Skills")
    st.markdown("""
    Skills là các instructions cụ thể cho từng task mà agent thực hiện:
    - Intake skill: Trích xuất thông tin
    - Classification skills: Phân loại dữ liệu
    - Generation skills: Tạo output
    """)
    
    files = get_knowledge_files()
    skill_files = [f for f in files if f["type"] == "skill"]
    
    if skill_files:
        # File selector
        selected_skill = st.selectbox(
            "Chọn skill để edit:",
            options=[f["name"] for f in skill_files],
            format_func=lambda x: f"🎯 {x}",
            key="skill_file_selector"
        )
        
        if selected_skill:
            st.subheader(f"Editing: {selected_skill}")
            
            content = get_knowledge_file(selected_skill)
            
            if content:
                edited_content = st.text_area(
                    "Edit skill:",
                    value=content,
                    height=400,
                    key=f"skill_editor_{selected_skill}"
                )
                
                col1, col2, col3 = st.columns([1, 1, 4])
                
                with col1:
                    if st.button("💾 Save Changes", use_container_width=True, type="primary", key="save_skill"):
                        if update_knowledge_file(selected_skill, edited_content):
                            st.success(f"✅ {selected_skill} đã được cập nhật!")
                            st.balloons()
                        else:
                            st.error(f"❌ Không thể cập nhật {selected_skill}")
                
                with col2:
                    if st.button("🔄 Reload", use_container_width=True, key="reload_skill"):
                        st.rerun()
                
                st.divider()
                
                # Info
                st.info(f"""
                **File:** {selected_skill}  
                **Type:** Agent Skill  
                **Lines:** {len(edited_content.splitlines())}  
                **Characters:** {len(edited_content)}
                """)
                
                # Preview sections
                with st.expander("📋 File Structure", expanded=False):
                    lines = edited_content.splitlines()
                    sections = [line for line in lines if line.startswith("#")]
                    if sections:
                        st.markdown("\n".join(sections))
                    else:
                        st.info("No markdown headers found")
            else:
                st.warning(f"⚠️ Không thể load content của {selected_skill}")
    else:
        st.warning("⚠️ Không tìm thấy skill files.")


# Sidebar
with st.sidebar:
    st.header("ℹ️ Hướng dẫn")
    
    st.markdown("""
    ### System Prompt
    - Định nghĩa vai trò của agent
    - Cách agent trả lời
    - Format output
    
    ### Knowledge Base
    - **privacy_rules.md**: Định nghĩa dữ liệu cá nhân
    - **dpa_checklist.md**: Checklist cho domestic cases
    - **otia_checklist.md**: Checklist cho cross-border
    
    ### Skills
    - **intake_skill.md**: Trích xuất info
    - **privacy_classification_skill.md**: Phân loại data
    - **transfer_classification_skill.md**: Domestic vs cross-border
    - **checklist_generation_skill.md**: Tạo checklist
    - **data_flow_generation_skill.md**: Vẽ diagram
    - **privacy_summary_skill.md**: Tóm tắt
    - **email_generation_skill.md**: Draft email
    """)
    
    st.divider()
    
    st.warning("""
    ⚠️ **Lưu ý:**
    - Changes có hiệu lực ngay lập tức
    - Backup files trước khi edit
    - Test kỹ sau khi thay đổi
    """)
    
    st.divider()
    
    if st.button("🏠 Về Chat", use_container_width=True):
        st.switch_page("app.py")


# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>Admin Panel v2.0 | Quản lý Agent Configuration</p>
</div>
""", unsafe_allow_html=True)
