"""
Authentication helpers for Streamlit frontend
"""
import streamlit as st
import requests
from typing import Optional, Dict


def init_session_state():
    """Initialize session state for authentication"""
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = None
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.auth_token is not None


def login(backend_url: str, username: str, password: str) -> tuple[bool, str]:
    """
    Login user and store token in session state
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        response = requests.post(
            f"{backend_url}/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.auth_token = data["access_token"]
            
            # Get user info
            user_info = get_current_user(backend_url)
            if user_info:
                st.session_state.current_user = user_info
                return True, "Login successful!"
            else:
                return False, "Failed to get user information"
        elif response.status_code == 401:
            return False, "Incorrect username or password"
        else:
            return False, f"Login failed: {response.status_code}"
    except Exception as e:
        return False, f"Error connecting to server: {str(e)}"


def logout():
    """Logout user and clear session state"""
    st.session_state.auth_token = None
    st.session_state.current_user = None


def get_auth_headers() -> Dict[str, str]:
    """Get authorization headers for API requests"""
    if st.session_state.auth_token:
        return {"Authorization": f"Bearer {st.session_state.auth_token}"}
    return {}


def get_current_user(backend_url: str) -> Optional[Dict]:
    """Get current user information"""
    try:
        if not st.session_state.auth_token:
            return None
        
        response = requests.get(
            f"{backend_url}/auth/me",
            headers=get_auth_headers(),
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception:
        return None


def show_login_page(backend_url: str):
    """Display login page"""
    st.markdown("""
        <div class="welcome-box" style="text-align: center;">
            <h2>🔒 Admin Login</h2>
            <p>Please login to access the Admin Panel</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    success, message = login(backend_url, username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("---")
        st.info("💡 Default credentials: admin / admin123")
        st.caption("(Change password after first login)")
