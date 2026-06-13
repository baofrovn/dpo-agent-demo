import os
import httpx
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class AgentService:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        
        self.system_prompt = self._load_system_prompt()
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_file(self, filepath: str) -> str:
        """Load content from a file"""
        try:
            path = Path(__file__).parent / filepath
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")
            return ""
    
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
    
    async def call_llm(self, user_message: str) -> str:
        """Call LLM API with system prompt and user message"""
        if not self.api_key:
            return self._get_mock_response(user_message)
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                full_system_prompt = f"{self.system_prompt}\n\n{self.knowledge_base}"
                
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": full_system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 4000,
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            return self._get_mock_response(user_message)
    
    def _get_mock_response(self, user_message: str) -> str:
        """Return a mock response when API key is not available"""
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
👉 https://company.form/privacy-domestic-intake

**Đối với case NƯỚC NGOÀI:**
Vui lòng điền **Form B – Cross-border Data Sharing Intake Form** tại link:
👉 https://company.form/privacy-cross-border-intake

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
    
    async def analyze_case(self, message: str) -> str:
        """Main entry point for case analysis"""
        return await self.call_llm(message)
