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
        return f"""# Data Privacy Case Analysis (MOCK RESPONSE)

**Note: This is a mock response. Configure LLM_API_KEY to get real AI analysis.**

---

## A. Case Classification

**Personal Data Involved:** Likely Yes  
**Sensitive Personal Data:** Potentially Yes  
**Transfer Type:** Need Confirmation  
**Human Review Required:** Yes

---

## B. Reasoning

Based on the limited information provided in your request:

```
{user_message[:200]}...
```

Without complete API integration, this is a template response. The actual agent would:
- Analyze the business purpose
- Identify data categories
- Classify transfer type (domestic/cross-border)
- Assess risk level

---

## C. Missing Information

Please provide the following information:
- [ ] Clear business purpose and use case
- [ ] Specific data categories being processed/shared
- [ ] Recipient/vendor name and location
- [ ] Data subjects affected (customers, users, etc.)
- [ ] Data transfer mechanism (API, file transfer, database access, etc.)
- [ ] Data retention period
- [ ] Security measures in place
- [ ] Existing contracts or agreements

---

## D. Required Document Checklist

**For Domestic Data Sharing:**
- [ ] Contract/MSA with partner
- [ ] Data Processing Agreement (DPA)
- [ ] Purpose of processing
- [ ] List of personal data categories
- [ ] Roles of parties
- [ ] Data retention period
- [ ] Security measures
- [ ] Sub-processor list (if any)
- [ ] Incident response obligations
- [ ] Evidence of user notice/consent

**For Cross-Border Transfer:**
- [ ] Recipient name and country
- [ ] Cross-border transfer purpose
- [ ] Data categories for transfer
- [ ] Data subject groups
- [ ] Transfer mechanism
- [ ] DPA with cross-border clauses
- [ ] Security assessment
- [ ] Data protection level assessment

---

## E. Draft Data Flow

```mermaid
flowchart LR
    Customer[Customer/User] -->|Personal Data| App[Company App]
    App -->|Processing| Backend[Internal System]
    Backend -->|Data Sharing| Partner[Partner/Vendor]
    Partner -.->|Location TBD| Country[Country TBD]
    
    style Customer fill:#e1f5ff
    style App fill:#fff4e1
    style Backend fill:#ffe1f5
    style Partner fill:#f5e1ff
    style Country fill:#ff0000
```

---

## F. Summary for Data Privacy Team

**Case Type:** TBD (need more information)  
**Risk Level:** Medium to High  
**Transfer Type:** TBD  
**Next Steps:**  
1. Request complete information from Biz team
2. Review contracts and DPA
3. Conduct risk assessment
4. Determine if OTIA/cross-border assessment needed

**Reviewer Notes:**  
This case requires human review due to insufficient information. Please coordinate with Biz team to gather complete documentation.

---

## G. Suggested Email to Biz

**Subject:** Data Privacy Review - Additional Information Required

Dear Team,

Thank you for submitting your data privacy review request. To proceed with the assessment, we need the following information:

**Required Information:**
- Business purpose and detailed use case
- Complete list of personal data categories
- Recipient/vendor details (name, location, country)
- Data transfer mechanism
- Data retention period
- Security measures

**Required Documents:**
- Draft contract or MSA
- DPA or data protection clauses
- Evidence of user consent/notice (if applicable)

Please provide the above information at your earliest convenience so we can complete the privacy assessment.

If you have any questions, please don't hesitate to reach out.

Best regards,  
Data Privacy Team

---

**Important:** This analysis is preliminary. Final approval requires human review by the Data Privacy legal team.
"""
    
    async def analyze_case(self, message: str) -> str:
        """Main entry point for case analysis"""
        return await self.call_llm(message)
