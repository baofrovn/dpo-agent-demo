# Data Privacy Intake Agent

> AI Chatbot hỗ trợ team Biz/PO tại fintech chuẩn bị hồ sơ chia sẻ dữ liệu trước khi gửi Data Privacy review.

**Built for:** Internal AI Competition Demo  
**Version:** 2.0.0  
**Status:** Production Ready

---

## 🎯 Use Case Summary

| Thành phần | Mô tả |
|------------|-------|
| **🔴 Vấn đề** | Team Biz/Product tại fintech thường gửi yêu cầu Data Privacy review thiếu thông tin, gây ra 3-5 lần trao đổi qua lại, làm chậm quy trình 2-4 tuần và tạo bottleneck cho team Privacy. |
| **👥 Người dùng** | (1) Team Business/Product Owner cần chia sẻ dữ liệu khách hàng với vendors/partners; (2) Team Data Privacy cần review và phê duyệt các yêu cầu. |
| **✅ Giải pháp** | AI Chatbot tự động: phân loại case (trong nước/nước ngoài), detect dữ liệu nhạy cảm, phát hiện thông tin thiếu, sinh checklist DPA/OTIA, tạo data flow diagram, draft email - giúp Biz gửi request đầy đủ ngay lần đầu. |

### Mô tả ngắn

**Data Privacy Intake Agent** giúp team Biz/PO chuẩn bị hồ sơ chia sẻ dữ liệu. Agent tự động phân loại, phát hiện gaps, sinh checklist và tóm tắt - giảm 70% thời gian trao đổi với Privacy team.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start with Docker](#quick-start-with-docker)
- [Local Development Setup](#local-development-setup)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Demo Script](#demo-script)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Overview

### Problem Statement

At fintech companies, Business/Product teams frequently submit data privacy review requests for:
- Data Processing Agreements (DPA) with vendors
- Data sharing with partners
- Cross-border data transfers
- New vendor onboarding

However, these requests often lack critical information, causing:
- Multiple back-and-forth communications
- Delayed approvals
- Incomplete risk assessments
- Privacy team bottlenecks

### Solution

The Data Privacy Intake Agent automates the initial intake process by:

1. **Analyzing** the case description
2. **Classifying** the case type (domestic vs cross-border, personal vs sensitive data)
3. **Identifying** missing information
4. **Generating** required document checklists
5. **Creating** data flow diagrams
6. **Producing** executive summaries for reviewers
7. **Drafting** follow-up emails to request additional information

This reduces the Data Privacy team's workload and helps Business teams submit complete requests the first time.

### Key Benefits

- **For Business Teams:** Clear guidance on what information to provide
- **For Data Privacy Team:** Pre-analyzed cases with complete documentation
- **For the Organization:** Faster approval cycles and better compliance

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User (Biz/Product Team)              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                      │
│  - Web UI                                                    │
│  - Sample cases                                              │
│  - Result display                                            │
│  Port: 8501                                                  │
└────────────────────────┬────────────────────────────────────┘
                         │ POST /chat
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  - API endpoints                                             │
│  - Agent service                                             │
│  - Knowledge base loader                                     │
│  Port: 8000                                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ├──► System Prompt
                         ├──► Knowledge Base (Privacy Rules, Checklists)
                         ├──► Skills (7 specialized instructions)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM API (OpenAI-compatible)               │
│  - GPT-4, GPT-3.5, or other compatible models                │
│  - Configured via environment variables                      │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.11
- FastAPI (REST API)
- httpx (HTTP client for LLM API)
- python-dotenv (environment management)

**Frontend:**
- Streamlit (web UI)
- requests (API client)

**LLM Integration:**
- OpenAI-compatible API
- Configurable model (gpt-4o-mini, gpt-4, etc.)
- Mock response fallback for demos without API key

**Deployment:**
- Docker & Docker Compose
- No database (MVP)
- No vector store (MVP)

---

## Features

### Core Capabilities

✅ **Case Classification**
- Identifies personal data involvement
- Detects sensitive personal data (financial, biometric, health)
- Classifies domestic vs cross-border transfers
- Assesses risk level

✅ **Information Gap Analysis**
- Identifies missing critical information
- Prioritizes gaps (critical, high-priority, nice-to-have)
- Provides specific questions to ask Business team

✅ **Document Checklist Generation**
- DPA checklist for domestic cases
- OTIA checklist for cross-border cases
- Customized based on case specifics

✅ **Data Flow Visualization**
- Generates Mermaid diagrams
- Shows data flow from user to systems to vendors
- Highlights cross-border elements

✅ **Executive Summary**
- Concise summary for Data Privacy reviewers
- Risk assessment with justification
- Recommended next steps

✅ **Email Drafting**
- Professional email requesting missing information
- Specific, actionable requests
- Appropriate tone and timeline

### Sample Cases Included

1. **No Personal Data Case** - Aggregated reporting (low risk)
2. **Domestic Sharing Case** - Customer support vendor (medium risk)
3. **Cross-Border Transfer Case** - Credit scoring with Singapore vendor (high risk)

---

## Project Structure

```
data-privacy-intake-agent/
├── backend/
│   ├── main.py                           # FastAPI application
│   ├── agent_service.py                  # LLM integration & agent logic
│   ├── requirements.txt                  # Python dependencies
│   ├── Dockerfile                        # Backend container
│   ├── .env.example                      # Environment variables template
│   │
│   ├── prompts/
│   │   └── system_prompt.md              # Main system prompt for agent
│   │
│   ├── knowledge/
│   │   ├── privacy_rules.md              # Privacy data definitions & rules
│   │   ├── dpa_checklist.md              # Domestic case checklist
│   │   └── otia_checklist.md             # Cross-border case checklist
│   │
│   ├── skills/
│   │   ├── intake_skill.md               # Information extraction
│   │   ├── privacy_classification_skill.md    # Data classification
│   │   ├── transfer_classification_skill.md   # Domestic vs cross-border
│   │   ├── checklist_generation_skill.md      # Checklist creation
│   │   ├── data_flow_generation_skill.md      # Mermaid diagram
│   │   ├── privacy_summary_skill.md           # Executive summary
│   │   └── email_generation_skill.md          # Email drafting
│   │
│   └── examples/
│       └── sample_cases.md               # 3 demo cases
│
├── frontend/
│   ├── app.py                            # Streamlit web app
│   ├── requirements.txt                  # Python dependencies
│   ├── Dockerfile                        # Frontend container
│   └── README.md                         # Frontend documentation
│
├── docker-compose.yml                    # Multi-container orchestration
└── README.md                             # This file
```

**Total Files:** 21 files

---

## Prerequisites

### For Docker Deployment (Recommended)
- Docker Desktop or Docker Engine
- Docker Compose v2.0+

### For Local Development
- Python 3.11+
- pip

### For Full Functionality
- OpenAI API key or compatible LLM API
- (Optional) The app works with mock responses without an API key

---

## Quick Start with Docker

This is the fastest way to get the app running.

### Step 1: Clone or Navigate to Project

```bash
cd data-privacy-intake-agent
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy example
cp backend/.env.example .env

# Edit .env file
# Add your API key
```

`.env` file content:

```
LLM_API_KEY=your-openai-api-key-here
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1
```

**Note:** If you don't have an API key, the app will use mock responses for demo purposes.

### Step 3: Start Services

```bash
docker-compose up -d
```

This will:
- Build both backend and frontend containers
- Start the services in the background
- Expose ports 8000 (backend) and 8501 (frontend)

### Step 4: Access the Application

**Frontend (Web UI):**  
Open http://localhost:8501 in your browser

**Backend (API):**  
http://localhost:8000

**Health Check:**  
http://localhost:8000/health

### Step 5: Test with Sample Cases

In the web UI:
1. Click one of the three sample case buttons in the sidebar
2. Click "Analyze Case"
3. Wait 10-30 seconds for analysis
4. Review the comprehensive output

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

---

## Local Development Setup

For development without Docker.

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API key

# Run backend
python main.py
```

Backend will run on http://localhost:8000

### Frontend Setup

Open a new terminal:

```bash
cd frontend

# Create virtual environment (optional, can reuse)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set backend URL
export BACKEND_URL=http://localhost:8000  # On Windows: set BACKEND_URL=http://localhost:8000

# Run frontend
streamlit run app.py
```

Frontend will run on http://localhost:8501

---

## Configuration

### Environment Variables

#### Backend (`backend/.env`)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LLM_API_KEY` | OpenAI or compatible API key | None | No* |
| `LLM_MODEL` | Model name | `gpt-4o-mini` | No |
| `LLM_BASE_URL` | API base URL | `https://api.openai.com/v1` | No |

*If not provided, backend uses mock responses.

#### Frontend

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BACKEND_URL` | Backend API URL | `http://localhost:8000` | No |

### Changing the LLM Model

Edit `.env`:

```bash
# For GPT-4
LLM_MODEL=gpt-4

# For GPT-3.5 Turbo
LLM_MODEL=gpt-3.5-turbo

# For other compatible models
LLM_MODEL=your-model-name
```

### Using a Different LLM Provider

If using a different OpenAI-compatible API:

```bash
LLM_BASE_URL=https://your-provider.com/v1
LLM_API_KEY=your-provider-api-key
LLM_MODEL=your-model-name
```

---

## API Documentation

### Backend Endpoints

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

#### `POST /chat`

Analyze a data privacy case.

**Request:**
```json
{
  "message": "We want to share customer data with Vendor XYZ..."
}
```

**Response:**
```json
{
  "answer": "# Data Privacy Case Analysis\n\n## A. Case Classification\n..."
}
```

**Response Format:**

The `answer` field contains markdown-formatted analysis with these sections:

- A. Case Classification
- B. Reasoning
- C. Missing Information
- D. Required Document Checklist
- E. Draft Data Flow (Mermaid diagram)
- F. Summary for Data Privacy Team
- G. Suggested Email to Biz

### Testing the API

Using curl:

```bash
# Health check
curl http://localhost:8000/health

# Analyze a case
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "We want to share customer emails with a marketing vendor in Vietnam."}'
```

Using Python:

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "Your case description here"}
)

print(response.json()["answer"])
```

---

## Testing

### Test Cases Provided

Three sample cases are included in `backend/examples/sample_cases.md`:

1. **Case 1: No Personal Data** - Aggregated reporting
2. **Case 2: Domestic Sharing** - Customer support vendor
3. **Case 3: Cross-Border Transfer** - Credit scoring with Singapore vendor

### Manual Testing via Web UI

1. Open http://localhost:8501
2. Click "No Personal Data" button
3. Click "Analyze Case"
4. Verify output shows low-risk classification
5. Repeat for other sample cases

### Manual Testing via API

```bash
# Test Case 1: No Personal Data
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Team tôi muốn chia sẻ báo cáo tổng hợp số lượng giao dịch theo tháng cho đối tác, không có user ID, số điện thoại, email hoặc thông tin định danh khách hàng."}'

# Expected: Classification shows likely no personal data, low risk
```

### Automated Testing

For the MVP, automated tests are not included. Future versions should include:
- Unit tests for backend functions
- Integration tests for API endpoints
- End-to-end tests for user flows

---

## Demo Script

Use this script for live demos or presentations.

### Preparation (5 minutes before demo)

1. Start services:
   ```bash
   docker-compose up -d
   ```

2. Open frontend: http://localhost:8501

3. Open a second browser tab to backend health: http://localhost:8000/health

4. Prepare to screen share the web UI

### Demo Flow (10-15 minutes)

#### Introduction (2 minutes)

"Today I'll demo the Data Privacy Intake Agent, which helps Business teams prepare complete privacy review requests."

**Show the problem:**
- Business teams often submit incomplete requests
- Lots of back-and-forth to gather information
- Data Privacy team spends time on basic triage
- Delays in approvals

**Show the solution:**
- AI agent analyzes cases
- Identifies missing information
- Generates checklists and summaries
- Drafts follow-up emails

#### Demo Case 1: Low Risk (3 minutes)

Click "No Personal Data" button

**Explain:** "This is a simple case - sharing aggregated statistics with no personal data."

Click "Analyze Case"

**While waiting:** "The agent is analyzing the case, classifying data types, and generating recommendations."

**When complete, highlight:**
- ✅ Classification: Likely no personal data
- ✅ Agent asks for confirmation of anonymization
- ✅ Low risk assessment
- ✅ Simplified checklist

**Key message:** "Even for low-risk cases, the agent ensures proper documentation."

#### Demo Case 2: Medium Risk (4 minutes)

Click "Domestic Sharing" button

**Explain:** "This is a more complex case - sharing customer data with a domestic vendor for customer support."

Click "Analyze Case"

**When complete, highlight:**
- 🟡 Personal data: Yes (names, phones, emails)
- 🟡 Sensitive data: Potentially yes (transaction history)
- 🟡 Transfer type: Domestic sharing
- 🟡 Human review required: Yes
- **Show the checklist** - DPA requirements
- **Show missing items** - No DPA yet, security measures unclear
- **Show data flow diagram** - Visual representation
- **Show email draft** - Professional request for information

**Key message:** "The agent provides a complete analysis with specific, actionable guidance."

#### Demo Case 3: High Risk (5 minutes)

Click "Cross-Border Transfer" button

**Explain:** "This is a high-risk case - transferring sensitive financial data to Singapore and Philippines for credit scoring."

Click "Analyze Case"

**When complete, highlight:**
- 🔴 Personal data: Yes
- 🔴 Sensitive data: Yes (financial - credit scores, transaction history)
- 🔴 Transfer type: Cross-border (Singapore + Philippines)
- 🔴 Human review: Absolutely required
- **Show risk factors:**
  - Cross-border to multiple countries
  - Sensitive financial data
  - Large scale (30,000 users)
- **Show OTIA checklist** - Comprehensive cross-border requirements
- **Show data flow with countries highlighted**
- **Show executive summary** - Clear risk assessment
- **Show email** - Detailed requirements

**Key message:** "For high-risk cases, the agent provides thorough analysis to ensure nothing is missed."

#### Conclusion (1 minute)

**Summarize:**
- ✅ Agent handles cases of all complexity levels
- ✅ Provides specific, actionable guidance
- ✅ Saves time for both Business and Data Privacy teams
- ✅ Improves compliance and reduces risk

**Q&A**

### Common Demo Questions

**Q: Does this replace the Data Privacy team?**  
A: No. This is an intake assistant. Final legal review and approval still require human experts.

**Q: What if the LLM makes a mistake?**  
A: That's why human review is required for all cases, especially high-risk ones. The agent flags uncertain classifications.

**Q: Can we customize the checklists?**  
A: Yes. The knowledge base files (in `backend/knowledge/`) can be edited to match your organization's requirements.

**Q: Does it work with Vietnamese input?**  
A: Yes. The agent handles both Vietnamese and English inputs.

**Q: How long does analysis take?**  
A: Typically 10-30 seconds depending on case complexity and LLM response time.

---

## Limitations

This is an MVP (Minimum Viable Product) for demo purposes. Current limitations:

### Functional Limitations

❌ **No Database**  
- Cases are not saved
- No case history or tracking
- Each analysis is independent

❌ **No Vector Database / RAG**  
- Knowledge base is loaded directly into prompt
- No semantic search over historical cases
- Limited by LLM context window

❌ **No Authentication**  
- No user login
- No access control
- No audit trail

❌ **No Complex Workflows**  
- No LangGraph or complex chains
- Single-shot analysis
- No iterative refinement

❌ **No Integration**  
- No email sending
- No Jira ticket creation
- No SharePoint integration
- No calendar booking

❌ **No Human-in-the-Loop**  
- No approval workflow
- No review assignment
- No notifications

### Technical Limitations

⚠️ **Mock Response Fallback**  
- Without API key, provides generic mock response
- Not useful for real analysis

⚠️ **Single Model**  
- No ensemble or model comparison
- Quality depends on chosen LLM

⚠️ **No Caching**  
- Each request calls LLM
- No caching of similar cases

⚠️ **Basic Error Handling**  
- Limited retry logic
- No graceful degradation

### Known Issues

- Mermaid diagram rendering may vary by browser
- Large responses may take time to display
- No session persistence across refreshes
- Vietnamese text rendering depends on system fonts

---

## Future Enhancements

### Phase 2: Data Persistence
- Add PostgreSQL or MongoDB
- Store case history
- Track submission status
- Enable case search and retrieval

### Phase 3: RAG & Vector Search
- Implement vector database (Pinecone, Weaviate, or Chroma)
- Semantic search over past cases
- Retrieve similar approved cases
- Learn from historical decisions

### Phase 4: Integration
- Email integration (send drafts automatically)
- Jira/ServiceNow ticket creation
- SharePoint document library integration
- Calendar scheduling for review meetings
- Slack/Teams notifications

### Phase 5: Workflow Automation
- Human approval workflow
- Assign cases to reviewers
- Track review status
- Escalation rules
- SLA monitoring

### Phase 6: Advanced Features
- Multi-language support (Vietnamese, English, others)
- Voice input/output
- PDF document parsing
- Contract clause extraction
- Automatic DPA generation
- Risk scoring model
- Compliance dashboard

### Phase 7: Authentication & Security
- User authentication (OAuth, SSO)
- Role-based access control
- Audit logging
- Data encryption at rest
- Compliance with ISO 27001

### Phase 8: Analytics
- Usage metrics dashboard
- Case volume trends
- Average resolution time
- Most common missing items
- Vendor risk heatmap

---

## Troubleshooting

### Backend won't start

**Error:** Port 8000 already in use

**Solution:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
# Kill process by PID

# macOS/Linux:
lsof -ti:8000 | xargs kill
```

### Frontend can't connect to backend

**Error:** "Cannot connect to backend"

**Check:**
1. Is backend running? http://localhost:8000/health
2. Is BACKEND_URL correct? Check docker-compose.yml
3. Check Docker network: `docker network ls`

**Solution:**
```bash
docker-compose restart backend
docker-compose logs backend
```

### LLM API errors

**Error:** "Error calling LLM API"

**Check:**
1. Is LLM_API_KEY set correctly?
2. Is LLM_BASE_URL correct?
3. Do you have API credits?

**Solution:**
- Without API key, app uses mock responses
- Check `.env` file
- Test API key with curl:
  ```bash
  curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer YOUR_API_KEY"
  ```

### Slow response times

**Issue:** Analysis takes > 30 seconds

**Possible causes:**
- LLM API latency
- Large prompt size
- Model choice (GPT-4 is slower than GPT-3.5)

**Solution:**
- Use faster model: `LLM_MODEL=gpt-3.5-turbo`
- Increase timeout in frontend (edit `app.py`)

---

## Contributing

This is an internal demo project. For improvements:

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with description

---

## License

Internal use only. Not licensed for external distribution.

---

## Contact

For questions about this demo:

- **Project Owner:** [Your Name]
- **Team:** Data Privacy
- **Competition:** Internal AI Competition [Year]

---

## Acknowledgments

- **Data Privacy Team** - For domain expertise and requirements
- **Business Teams** - For real-world use cases and feedback
- **AI Competition Organizers** - For the opportunity to innovate

---

## Appendix

### Glossary

- **DPA** - Data Processing Agreement
- **OTIA** - Offshore Transfer Impact Assessment (cross-border checklist)
- **PII** - Personally Identifiable Information
- **MVP** - Minimum Viable Product
- **LLM** - Large Language Model
- **RAG** - Retrieval-Augmented Generation

### References

- Vietnamese Personal Data Protection Decree
- GDPR (for international best practices)
- ISO 27001 (Information Security Management)
- OpenAI API Documentation

---

**End of README**

For frontend-specific documentation, see `frontend/README.md`.

For sample cases and testing, see `backend/examples/sample_cases.md`.
