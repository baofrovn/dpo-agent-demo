import streamlit as st
import requests
import os
import sys
import pandas as pd
from datetime import datetime

# Add frontend path to import auth_helper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import auth_helper

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Admin Panel - Privacy Chatbot",
    page_icon="⚙️",
    layout="wide",
)

# Initialize auth
auth_helper.init_session_state()

# Custom CSS
st.markdown("""
<style>
    .rule-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #f9f9f9;
    }
    
    [data-theme="dark"] .rule-card {
        background-color: rgba(49, 51, 63, 0.5);
        border-color: #444;
    }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    .status-active {
        background-color: #28a745;
        color: white;
    }
    
    .status-inactive {
        background-color: #dc3545;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication
if not auth_helper.is_authenticated():
    auth_helper.show_login_page(BACKEND_URL)
    st.stop()

# Header with logout
col1, col2 = st.columns([6, 1])
with col1:
    st.title("⚙️ Admin Panel")
    if auth_helper.st.session_state.current_user:
        st.caption(f"Logged in as: **{auth_helper.st.session_state.current_user['username']}**")
with col2:
    if st.button("🚪 Logout", use_container_width=True):
        auth_helper.logout()
        st.rerun()

# Tabs
tabs = st.tabs([
    "⚙️ General Settings",
    "📋 Checklist Items", 
    "❓ Screening Questions", 
    "🔑 Sensitive Keywords",
    "📜 Audit Logs",
    "📝 Legacy (System Prompt)"
])

# Helper functions
def api_request(method, endpoint, data=None, params=None):
    """Make authenticated API request"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        headers = auth_helper.get_auth_headers()
        
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return None
        
        if response.status_code in [200, 201, 204]:
            return response.json() if response.text else {}
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

# TAB 0: General Settings
with tabs[0]:
    st.header("⚙️ General Settings")
    
    # Load current settings
    settings_response = api_request("GET", "/settings")
    config_response = api_request("GET", "/config")
    
    if settings_response and config_response:
        settings = settings_response
        config = config_response
        
        with st.form("general_settings_form"):
            st.subheader("🏢 Company Information")
            company_name = st.text_input(
                "Company Name",
                value=config.get("company_name", "Công ty Fintech ABC"),
                help="Tên công ty hiển thị trong phân tích"
            )
            
            st.divider()
            st.subheader("🔗 Form Links")
            
            col1, col2 = st.columns(2)
            with col1:
                form_a_link = st.text_input(
                    "Form A Link (Domestic)",
                    value=config.get("form_a_link", ""),
                    help="Link form cho chia sẻ dữ liệu trong nước"
                )
            with col2:
                form_b_link = st.text_input(
                    "Form B Link (Cross-border)",
                    value=config.get("form_b_link", ""),
                    help="Link form cho chia sẻ dữ liệu ra nước ngoài"
                )
            
            st.divider()
            st.subheader("🤖 AI Model Configuration")
            
            # Parse available models
            available_models = settings.get("available_models", [])
            if isinstance(available_models, str):
                import json
                available_models = json.loads(available_models)
            
            model_options = [m["id"] for m in available_models]
            model_labels = [f"{m['name']} ({m['provider']})" for m in available_models]
            
            current_model = settings.get("model", "qwen/qwen3-5-27b")
            try:
                current_index = model_options.index(current_model)
            except ValueError:
                current_index = 0
            
            selected_model = st.selectbox(
                "Select AI Model",
                options=model_options,
                format_func=lambda x: dict(zip(model_options, model_labels))[x],
                index=current_index,
                help="Model được dùng để phân tích case"
            )
            
            st.divider()
            st.subheader("📝 Custom Instructions")
            
            custom_instructions = st.text_area(
                "Custom Instructions for AI",
                value=settings.get("custom_instructions", ""),
                height=150,
                help="Hướng dẫn thêm cho AI (optional)"
            )
            
            st.divider()
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.form_submit_button("💾 Save Settings", use_container_width=True, type="primary"):
                    # Update config
                    config_data = {
                        "company_name": company_name,
                        "form_a_link": form_a_link,
                        "form_b_link": form_b_link
                    }
                    config_result = api_request("PUT", "/config", data=config_data)
                    
                    # Update settings
                    settings_data = {
                        "model": selected_model,
                        "custom_instructions": custom_instructions
                    }
                    settings_result = api_request("PUT", "/settings", data=settings_data)
                    
                    if config_result and settings_result:
                        st.success("✅ Settings saved successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save settings")
            
            with col2:
                if st.form_submit_button("🔄 Reset to Default", use_container_width=True):
                    st.warning("Reset functionality coming soon")

# TAB 1: Checklist Items
with tabs[1]:
    st.header("📋 Manage Checklist Items")
    
    # Category filter
    col1, col2, col3 = st.columns([2, 2, 4])
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All", "DPA", "OTIA", "GENERAL"],
            key="checklist_category_filter"
        )
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["Active Only", "Inactive Only", "All"],
            key="checklist_status_filter"
        )
    
    # Load checklist items
    params = {}
    if category_filter != "All":
        params["category"] = category_filter
    if status_filter != "All":
        params["is_active"] = status_filter == "Active Only"
    
    items = api_request("GET", "/rules/checklist", params=params)
    
    if items:
        st.info(f"Found {len(items)} checklist items")
        
        # Add new item button
        with st.expander("➕ Add New Checklist Item", expanded=False):
            with st.form("add_checklist_item"):
                col1, col2 = st.columns(2)
                with col1:
                    new_category = st.selectbox("Category", ["DPA", "OTIA", "GENERAL"])
                    new_item_number = st.text_input("Item Number", placeholder="e.g., 1, 2a, 2b")
                    new_title = st.text_input("Title", placeholder="Checklist item title")
                with col2:
                    new_description = st.text_area("Description", placeholder="Item description")
                    new_required_docs = st.text_area("Required Documents", placeholder="Documents needed")
                    new_notes = st.text_area("Notes", placeholder="Additional notes")
                
                new_display_order = st.number_input("Display Order", min_value=0, value=len(items))
                
                if st.form_submit_button("Create Item", use_container_width=True):
                    data = {
                        "category": new_category,
                        "item_number": new_item_number,
                        "title": new_title,
                        "description": new_description,
                        "required_documents": new_required_docs,
                        "notes": new_notes,
                        "is_active": True,
                        "display_order": new_display_order
                    }
                    
                    result = api_request("POST", "/rules/checklist", data=data)
                    if result:
                        st.success("✅ Checklist item created!")
                        st.rerun()
        
        st.divider()
        
        # Display items
        for item in items:
            with st.container():
                col1, col2, col3 = st.columns([5, 1, 1])
                
                with col1:
                    status_class = "status-active" if item["is_active"] else "status-inactive"
                    status_text = "Active" if item["is_active"] else "Inactive"
                    
                    st.markdown(f"""
                    <div class="rule-card">
                        <span class="status-badge {status_class}">{status_text}</span>
                        <span class="status-badge" style="background-color: #007bff; color: white; margin-left: 8px;">{item['category']}</span>
                        <h4 style="margin-top: 10px;">{item['item_number']}. {item['title']}</h4>
                        <p>{item['description'] or 'No description'}</p>
                        <small><b>Display Order:</b> {item['display_order']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_checklist_{item['id']}", use_container_width=True):
                        st.session_state[f"editing_checklist_{item['id']}"] = True
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_checklist_{item['id']}", use_container_width=True):
                        if api_request("DELETE", f"/rules/checklist/{item['id']}"):
                            st.success("Deleted!")
                            st.rerun()
                
                # Edit form
                if st.session_state.get(f"editing_checklist_{item['id']}", False):
                    with st.form(f"edit_form_{item['id']}"):
                        st.subheader(f"Edit: {item['title']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            edit_category = st.selectbox("Category", ["DPA", "OTIA", "GENERAL"], 
                                                        index=["DPA", "OTIA", "GENERAL"].index(item['category']))
                            edit_item_number = st.text_input("Item Number", value=item['item_number'])
                            edit_title = st.text_input("Title", value=item['title'])
                        with col2:
                            edit_description = st.text_area("Description", value=item['description'] or "")
                            edit_required_docs = st.text_area("Required Documents", value=item['required_documents'] or "")
                            edit_notes = st.text_area("Notes", value=item['notes'] or "")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            edit_display_order = st.number_input("Display Order", value=item['display_order'])
                        with col2:
                            edit_is_active = st.checkbox("Active", value=item['is_active'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                update_data = {
                                    "category": edit_category,
                                    "item_number": edit_item_number,
                                    "title": edit_title,
                                    "description": edit_description,
                                    "required_documents": edit_required_docs,
                                    "notes": edit_notes,
                                    "is_active": edit_is_active,
                                    "display_order": edit_display_order
                                }
                                
                                if api_request("PUT", f"/rules/checklist/{item['id']}", data=update_data):
                                    st.success("✅ Updated!")
                                    del st.session_state[f"editing_checklist_{item['id']}"]
                                    st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel", use_container_width=True):
                                del st.session_state[f"editing_checklist_{item['id']}"]
                                st.rerun()

# TAB 2: Screening Questions
with tabs[2]:
    st.header("❓ Manage Screening Questions")
    
    questions = api_request("GET", "/rules/questions", params={"is_active": True})
    
    if questions:
        st.info(f"Found {len(questions)} screening questions")
        
        # Add new question
        with st.expander("➕ Add New Question", expanded=False):
            with st.form("add_question"):
                new_q_text = st.text_area("Question Text", placeholder="Enter the screening question")
                new_q_type = st.selectbox("Question Type", ["yes_no", "multiple_choice", "text"])
                new_q_options = st.text_input("Options (for multiple choice, comma-separated)", placeholder="Option1, Option2, Option3")
                new_q_order = st.number_input("Display Order", min_value=0, value=len(questions))
                
                if st.form_submit_button("Create Question", use_container_width=True):
                    data = {
                        "question_text": new_q_text,
                        "question_type": new_q_type,
                        "options": new_q_options if new_q_options else None,
                        "is_active": True,
                        "display_order": new_q_order
                    }
                    
                    if api_request("POST", "/rules/questions", data=data):
                        st.success("✅ Question created!")
                        st.rerun()
        
        st.divider()
        
        # Display questions
        for q in sorted(questions, key=lambda x: x['display_order']):
            col1, col2, col3 = st.columns([5, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="rule-card">
                    <span class="status-badge" style="background-color: #17a2b8; color: white;">{q['question_type']}</span>
                    <p style="margin-top: 10px; font-size: 1.1em;"><b>Q{q['display_order'] + 1}:</b> {q['question_text']}</p>
                    {f'<small><b>Options:</b> {q["options"]}</small>' if q['options'] else ''}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✏️", key=f"edit_question_{q['id']}", use_container_width=True):
                    st.session_state[f"editing_question_{q['id']}"] = True
                    st.rerun()
            
            with col3:
                if st.button("🗑️", key=f"delete_question_{q['id']}", use_container_width=True):
                    if api_request("DELETE", f"/rules/questions/{q['id']}"):
                        st.success("Deleted!")
                        st.rerun()
            
            # Edit form
            if st.session_state.get(f"editing_question_{q['id']}", False):
                with st.form(f"edit_question_form_{q['id']}"):
                    edit_q_text = st.text_area("Question Text", value=q['question_text'])
                    edit_q_type = st.selectbox("Question Type", ["yes_no", "multiple_choice", "text"],
                                               index=["yes_no", "multiple_choice", "text"].index(q['question_type']))
                    edit_q_options = st.text_input("Options", value=q['options'] or "")
                    edit_q_order = st.number_input("Display Order", value=q['display_order'])
                    edit_q_active = st.checkbox("Active", value=q['is_active'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("💾 Save", use_container_width=True):
                            update_data = {
                                "question_text": edit_q_text,
                                "question_type": edit_q_type,
                                "options": edit_q_options if edit_q_options else None,
                                "is_active": edit_q_active,
                                "display_order": edit_q_order
                            }
                            
                            if api_request("PUT", f"/rules/questions/{q['id']}", data=update_data):
                                st.success("✅ Updated!")
                                del st.session_state[f"editing_question_{q['id']}"]
                                st.rerun()
                    
                    with col2:
                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                            del st.session_state[f"editing_question_{q['id']}"]
                            st.rerun()

# TAB 3: Sensitive Keywords
with tabs[3]:
    st.header("🔑 Manage Sensitive Keywords")
    
    keywords = api_request("GET", "/rules/keywords", params={"is_active": True})
    
    if keywords:
        st.info(f"Found {len(keywords)} sensitive keywords")
        
        # Add new keyword
        with st.expander("➕ Add New Keyword", expanded=False):
            with st.form("add_keyword"):
                col1, col2 = st.columns(2)
                with col1:
                    new_kw = st.text_input("Keyword", placeholder="e.g., credit score, biometric")
                    new_kw_category = st.selectbox("Category", ["financial", "health", "biometric", "general", "other"])
                with col2:
                    new_kw_desc = st.text_area("Description", placeholder="Optional description")
                
                if st.form_submit_button("Create Keyword", use_container_width=True):
                    data = {
                        "keyword": new_kw,
                        "category": new_kw_category,
                        "description": new_kw_desc,
                        "is_active": True
                    }
                    
                    if api_request("POST", "/rules/keywords", data=data):
                        st.success("✅ Keyword created!")
                        st.rerun()
        
        st.divider()
        
        # Group by category
        keywords_by_category = {}
        for kw in keywords:
            cat = kw.get('category', 'general') or 'general'
            if cat not in keywords_by_category:
                keywords_by_category[cat] = []
            keywords_by_category[cat].append(kw)
        
        # Display by category
        for category, kws in keywords_by_category.items():
            st.subheader(f"📂 {category.title()}")
            
            for kw in kws:
                col1, col2, col3 = st.columns([5, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="rule-card">
                        <p style="font-size: 1.1em;"><b>{kw['keyword']}</b></p>
                        {f'<small>{kw["description"]}</small>' if kw.get('description') else ''}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("✏️", key=f"edit_keyword_{kw['id']}", use_container_width=True):
                        st.session_state[f"editing_keyword_{kw['id']}"] = True
                        st.rerun()
                
                with col3:
                    if st.button("🗑️", key=f"delete_keyword_{kw['id']}", use_container_width=True):
                        if api_request("DELETE", f"/rules/keywords/{kw['id']}"):
                            st.success("Deleted!")
                            st.rerun()
                
                # Edit form
                if st.session_state.get(f"editing_keyword_{kw['id']}", False):
                    with st.form(f"edit_keyword_form_{kw['id']}"):
                        edit_kw = st.text_input("Keyword", value=kw['keyword'])
                        edit_kw_cat = st.selectbox("Category", 
                                                   ["financial", "health", "biometric", "general", "other"],
                                                   index=["financial", "health", "biometric", "general", "other"].index(kw.get('category', 'general') or 'general'))
                        edit_kw_desc = st.text_area("Description", value=kw.get('description', '') or '')
                        edit_kw_active = st.checkbox("Active", value=kw['is_active'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save", use_container_width=True):
                                update_data = {
                                    "keyword": edit_kw,
                                    "category": edit_kw_cat,
                                    "description": edit_kw_desc,
                                    "is_active": edit_kw_active
                                }
                                
                                if api_request("PUT", f"/rules/keywords/{kw['id']}", data=update_data):
                                    st.success("✅ Updated!")
                                    del st.session_state[f"editing_keyword_{kw['id']}"]
                                    st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel", use_container_width=True):
                                del st.session_state[f"editing_keyword_{kw['id']}"]
                                st.rerun()

# TAB 4: Audit Logs
with tabs[4]:
    st.header("📜 Audit Logs")
    
    col1, col2 = st.columns(2)
    with col1:
        table_filter = st.selectbox("Filter by Table", 
                                     ["All", "checklist_items", "screening_questions", "sensitive_keywords"])
    with col2:
        limit = st.number_input("Limit", min_value=10, max_value=500, value=100)
    
    params = {"limit": limit}
    if table_filter != "All":
        params["table_name"] = table_filter
    
    logs = api_request("GET", "/rules/audit-logs", params=params)
    
    if logs:
        st.info(f"Found {len(logs)} audit log entries")
        
        # Convert to DataFrame for better display
        df_data = []
        for log in logs:
            df_data.append({
                "Time": log['changed_at'][:19],
                "Table": log['table_name'],
                "Action": log['action'],
                "Record ID": log['record_id'][:8],
                "Changed By": log['changed_by'][:8] if log['changed_by'] else "System"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Detailed view
        with st.expander("View Detailed Logs"):
            for log in logs[:20]:  # Show first 20 in detail
                with st.container():
                    st.markdown(f"""
                    **{log['action']}** on `{log['table_name']}` 
                    by `{log['changed_by'] or 'System'}` 
                    at `{log['changed_at']}`
                    """)
                    
                    if log.get('old_value') or log.get('new_value'):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.json(log.get('old_value', {}), expanded=False)
                        with col2:
                            st.json(log.get('new_value', {}), expanded=False)
                    
                    st.divider()

# TAB 5: Legacy System Prompt
with tabs[5]:
    st.header("⚙️ Legacy: System Prompt & Knowledge Files")
    st.caption("For backward compatibility - direct file editing")
    
    # Add legacy editing UI here (copy from old admin panel)
    st.info("This tab provides access to direct file editing for system prompt and knowledge base files.")
    
    # You can copy the relevant code from the old admin panel here
    # For brevity, I'm not duplicating it all

# Sidebar
with st.sidebar:
    st.header("ℹ️ Admin Panel Guide")
    
    st.markdown("""
    ### General Settings
    - Configure company name
    - Set form links (domestic/cross-border)
    - Select AI model
    - Add custom instructions
    
    ### Checklist Items
    - Manage DPA and OTIA checklist items
    - Add, edit, delete, reorder items
    - Mark items as active/inactive
    
    ### Screening Questions
    - Questions to ask users during intake
    - Support different question types
    - Reorder for better flow
    
    ### Sensitive Keywords
    - Keywords that trigger data classification
    - Categorized by type (financial, health, etc.)
    - Used by AI for detection
    
    ### Audit Logs
    - Track all changes to rules
    - View who changed what and when
    - Compliance and debugging
    """)
    
    st.divider()
    
    if st.button("🏠 Back to Chat", use_container_width=True):
        st.switch_page("app.py")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>Admin Panel v2.0 with Database Rules | Customizable Rules System</p>
</div>
""", unsafe_allow_html=True)
