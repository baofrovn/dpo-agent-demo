import os
import httpx
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class AgentService:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.base_path = Path(__file__).parent
        
        self.system_prompt = self._load_system_prompt()
        self.knowledge_base = self._load_knowledge_base()
    
    def reload_config(self):
        """Reload configuration files"""
        self.system_prompt = self._load_system_prompt()
        self.knowledge_base = self._load_knowledge_base()
    
    def set_model(self, model: str):
        """Set the LLM model to use"""
        self.model = model
        
    def _load_file(self, filepath: str) -> str:
        """Load content from a file"""
        try:
            path = self.base_path / filepath
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")
            return ""
    
    def _save_file(self, filepath: str, content: str):
        """Save content to a file"""
        path = self.base_path / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _load_system_prompt(self) -> str:
        """Load the system prompt"""
        return self._load_file("prompts/system_prompt.md")
    
    def _load_knowledge_base(self) -> str:
        """Load all knowledge base files and combine them"""
        knowledge_files = [
            "knowledge/privacy_rules.md",
            "knowledge/dpa_checklist.md",
            "knowledge/otia_checklist.md",
        ]
        
        skill_files = [
            "skills/intake_skill.md",
            "skills/privacy_classification_skill.md",
            "skills/transfer_classification_skill.md",
            "skills/checklist_generation_skill.md",
            "skills/data_flow_generation_skill.md",
            "skills/privacy_summary_skill.md",
            "skills/email_generation_skill.md",
        ]
        
        combined_knowledge = "\n\n# KNOWLEDGE BASE\n\n"
        
        for file in knowledge_files:
            content = self._load_file(file)
            if content:
                combined_knowledge += f"\n## {file}\n\n{content}\n"
        
        combined_knowledge += "\n\n# SKILLS AND INSTRUCTIONS\n\n"
        
        for file in skill_files:
            content = self._load_file(file)
            if content:
                combined_knowledge += f"\n## {file}\n\n{content}\n"
        
        return combined_knowledge
    
    def get_system_prompt(self) -> str:
        """Get current system prompt"""
        return self.system_prompt
    
    def update_system_prompt(self, content: str):
        """Update and save system prompt"""
        self._save_file("prompts/system_prompt.md", content)
        self.system_prompt = content
    
    def get_knowledge_file(self, filename: str) -> str:
        """Get content of a knowledge base file"""
        # Check in knowledge folder first
        knowledge_path = f"knowledge/{filename}"
        if (self.base_path / knowledge_path).exists():
            return self._load_file(knowledge_path)
        
        # Check in skills folder
        skills_path = f"skills/{filename}"
        if (self.base_path / skills_path).exists():
            return self._load_file(skills_path)
        
        raise FileNotFoundError(f"File {filename} not found")
    
    def update_knowledge_file(self, filename: str, content: str):
        """Update a knowledge base file"""
        # Determine the correct path
        knowledge_path = f"knowledge/{filename}"
        skills_path = f"skills/{filename}"
        
        if (self.base_path / knowledge_path).exists():
            self._save_file(knowledge_path, content)
        elif (self.base_path / skills_path).exists():
            self._save_file(skills_path, content)
        else:
            # Default to knowledge folder for new files
            self._save_file(knowledge_path, content)
        
        # Reload knowledge base
        self.knowledge_base = self._load_knowledge_base()
    
    def list_knowledge_files(self) -> list:
        """List all knowledge base and skill files"""
        files = []
        
        # Knowledge files
        knowledge_dir = self.base_path / "knowledge"
        if knowledge_dir.exists():
            for f in knowledge_dir.glob("*.md"):
                files.append({
                    "name": f.name,
                    "type": "knowledge",
                    "path": f"knowledge/{f.name}"
                })
        
        # Skill files
        skills_dir = self.base_path / "skills"
        if skills_dir.exists():
            for f in skills_dir.glob("*.md"):
                files.append({
                    "name": f.name,
                    "type": "skill",
                    "path": f"skills/{f.name}"
                })
        
        return files
    
    def _build_config_context(self, config: Optional[dict] = None) -> str:
        """Build additional context from config"""
        if not config:
            return ""
        
        context = "\n\n# DYNAMIC CONFIGURATION\n\n"
        
        if config.get("company_name"):
            context += f"**Company Name:** {config['company_name']}\n\n"
        
        if config.get("form_a_link"):
            context += f"**Form A Link (Domestic):** {config['form_a_link']}\n\n"
        
        if config.get("form_b_link"):
            context += f"**Form B Link (Cross-Border):** {config['form_b_link']}\n\n"
        
        if config.get("custom_instructions"):
            context += f"**Custom Instructions:**\n{config['custom_instructions']}\n\n"
        
        if config.get("screening_questions"):
            context += "**Screening Questions to Ask:**\n"
            for q in config["screening_questions"]:
                context += f"- {q}\n"
            context += "\n"
        
        if config.get("sensitive_data_keywords"):
            context += f"**Sensitive Data Keywords:** {', '.join(config['sensitive_data_keywords'])}\n\n"
        
        return context
    
    async def call_llm(self, user_message: str, config: Optional[dict] = None, conversation_history: Optional[list] = None) -> str:
        """Call LLM API with system prompt, conversation history, and user message"""
        if not self.api_key:
            return self._get_mock_response(user_message, config)
        
        try:
            config_context = self._build_config_context(config)
            full_system_prompt = f"{self.system_prompt}\n\n{self.knowledge_base}{config_context}"
            
            # Build messages array with conversation history
            messages = [{"role": "system", "content": full_system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 4000,
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            return self._get_mock_response(user_message, config)
    
    def _get_mock_response(self, user_message: str, config: Optional[dict] = None) -> str:
        """Return a mock response when API key is not available"""
        form_a_link = config.get("form_a_link", "https://company.form/privacy-domestic-intake") if config else "https://company.form/privacy-domestic-intake"
        form_b_link = config.get("form_b_link", "https://company.form/privacy-cross-border-intake") if config else "https://company.form/privacy-cross-border-intake"
        
        return f"""# Kết Quả Phân Tích Case (MOCK RESPONSE)

**⚠️ Lưu ý: Đây là mock response. Cấu hình LLM_API_KEY để có phân tích AI thực.**

---

## A. Bảng Phân Loại Sơ Bộ

| Câu hỏi | Kết quả sơ bộ |
|---------|---------------|
| Có chia sẻ dữ liệu cho đối tác không? | Có khả năng có |
| Có dữ liệu cá nhân không? | Có khả năng có |
| Có dữ liệu cá nhân nhạy cảm không? | Cần xác nhận |
| Chia sẻ trong nước hay ngoài nước? | Cần xác nhận |
| Cần Data Privacy review không? | Có |
| Cần Legal/DPA review không? | Có khả năng cần |
| Cần Security review không? | Có khả năng cần |
| Cần xem xét OTIA không? | Cần xác nhận |

---

## B. Lý Do Phân Loại

Dựa trên thông tin từ request:

```
{user_message[:200]}...
```

Cần bổ sung thêm thông tin để phân loại chính xác:
- Vị trí đối tác (trong nước/nước ngoài)
- Loại dữ liệu cụ thể
- Phương thức truyền dữ liệu

---

## C. Thông Tin Còn Thiếu

Để xác định đúng checklist, vui lòng cho biết:
- [ ] Đối tác nhận dữ liệu ở Việt Nam hay nước ngoài?
- [ ] Dữ liệu dự kiến chia sẻ gồm những field nào?
- [ ] Dữ liệu có liên quan khách hàng/người dùng không?
- [ ] Đối tác dùng dữ liệu để làm gì?
- [ ] Dữ liệu gửi bằng cách nào: API, file Excel, SFTP hay email?
- [ ] Đối tác lưu dữ liệu bao lâu?
- [ ] Đã có hợp đồng/DPA với đối tác chưa?

---

## D. Checklist Hồ Sơ Cần Chuẩn Bị

**Đối với case TRONG NƯỚC (Domestic):**

| Nhóm hồ sơ | Cần chuẩn bị |
|------------|--------------|
| Thông tin đối tác | Tên pháp nhân, địa chỉ, GPKD |
| Mục đích xử lý | Đối tác nhận dữ liệu để làm gì |
| Danh sách dữ liệu | Field list + ý nghĩa từng field |
| Cách truyền dữ liệu | API/file/SFTP/email |
| Thời gian lưu trữ | Retention period |
| Biện pháp bảo mật | Mã hóa, phân quyền, log truy cập |
| Hợp đồng/DPA | Điều khoản bảo vệ dữ liệu cá nhân |

**Đối với case NƯỚC NGOÀI (Cross-Border):**

| Nhóm hồ sơ | Cần chuẩn bị |
|------------|--------------|
| Thông tin đối tác | Tên pháp nhân, quốc gia, company registration |
| Mục đích xử lý | Đối tác nhận dữ liệu để làm gì |
| Danh sách dữ liệu | Field list + ý nghĩa từng field |
| Server location | Dữ liệu được lưu/xử lý ở đâu |
| OTIA | Hồ sơ chuyển dữ liệu ra nước ngoài |

---

## E. Link Form Cần Điền

**Đối với case TRONG NƯỚC:**
Vui lòng điền **Form A – Domestic Data Sharing Intake Form** tại link:
👉 {form_a_link}

**Đối với case NƯỚC NGOÀI:**
Vui lòng điền **Form B – Cross-border Data Sharing Intake Form** tại link:
👉 {form_b_link}

---

## F. Data Flow Diagram

```mermaid
flowchart LR
    Customer[Khách hàng] -->|Dữ liệu cá nhân| App[Company App]
    App -->|API| Backend[Backend Vietnam]
    Backend -->|Chia sẻ| Partner[Đối tác]
    Partner -->|Lưu trữ| Server[Cần xác nhận]
```

---

## G. Tóm Tắt Request Gửi Data Privacy

**Tóm tắt request gửi Data Privacy:**

Team Biz/PO dự kiến chia sẻ dữ liệu cho [đối tác] để phục vụ mục đích [cần bổ sung]. Agent cần thêm thông tin về vị trí đối tác và loại dữ liệu cụ thể để phân loại chính xác đây là hoạt động chia sẻ dữ liệu cá nhân trong nước hay ra nước ngoài.

---

## H. Lưu Ý Quan Trọng

⚠️ **Lưu ý:** Đây là phân loại sơ bộ từ Agent. Kết luận cuối cùng cần được Data Privacy team xác nhận chính thức sau khi review đầy đủ hồ sơ.

**Giải thích thuật ngữ:**
- **API**: Kênh kỹ thuật để hai hệ thống gửi dữ liệu cho nhau
- **SFTP**: Cách gửi file qua kênh bảo mật
- **DPA**: Data Processing Agreement - thỏa thuận xử lý/bảo vệ dữ liệu cá nhân
- **OTIA**: Offshore Transfer Impact Assessment - đánh giá tác động chuyển dữ liệu ra nước ngoài
"""
    
    async def analyze_case(self, message: str, config: Optional[dict] = None, conversation_history: Optional[list] = None) -> str:
        """Main entry point for case analysis with conversation history support"""
        return await self.call_llm(message, config, conversation_history)
