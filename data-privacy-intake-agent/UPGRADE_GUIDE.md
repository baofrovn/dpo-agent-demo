# Upgrade Guide - Version 2.0.0

## 🎉 New Features

### 1. Chat Session Management
- **Lưu và quản lý nhiều chat sessions**
- **Tạo chat mới** và quay lại session cũ bất cứ lúc nào
- **Tự động lưu** mọi hội thoại vào backend
- **Xóa sessions** không cần thiết

### 2. Model Selection
- Hỗ trợ nhiều AI models:
  - **GPT-4o Mini** (OpenAI)
  - **GPT-4o** (OpenAI)
  - **GPT-4 Turbo** (OpenAI)
  - **Gemini 1.5 Pro** (Google)
  - **Gemini 1.5 Flash** (Google)
  - **Qwen Max** (Alibaba)
  - **Qwen Plus** (Alibaba)

### 3. Custom Instructions
- Setup instructions riêng cho agent của bạn
- Instructions sẽ được áp dụng cho **mọi message**
- Ví dụ: "Always respond in formal tone", "Focus on compliance"

### 4. Dark Mode Fix
- Cải thiện hiển thị trong dark mode
- Chat bubbles rõ ràng hơn
- Màu sắc tương thích với theme

---

## 🚀 How to Restart

### Option 1: Docker (Recommended)

```bash
cd E:\project\data-privacy-intake-agent

# Restart only frontend
docker-compose restart frontend

# Or rebuild everything
docker-compose down
docker-compose up --build -d
```

### Option 2: Local Development

**Terminal 1 - Backend:**
```bash
cd E:\project\data-privacy-intake-agent\backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd E:\project\data-privacy-intake-agent\frontend
streamlit run app.py
```

---

## 📖 How to Use New Features

### Chat Sessions

1. Click **"➕ New Chat"** trong sidebar để tạo chat mới
2. Click vào **tên session** để chuyển đổi giữa các chat
3. Click **🗑️** để xóa session không cần

### Model Selection

1. Mở **"⚙️ Settings"** trong sidebar
2. Chọn model từ dropdown
3. Click **"💾 Save Model"**
4. Model mới sẽ được sử dụng cho các message tiếp theo

### Custom Instructions

1. Mở **"⚙️ Settings"** trong sidebar
2. Nhập instructions vào text area
3. Click **"💾 Save Instructions"**
4. Instructions sẽ được áp dụng tự động

**Ví dụ instructions:**
```
- Always respond in Vietnamese
- Focus on legal compliance requirements
- Provide specific checklist items
- Be formal and professional
```

---

## 🔧 Configuration Files

Các file config được lưu tại:

```
backend/config/
├── agent_config.json      # Agent configuration
├── settings.json          # Model & custom instructions
└── sessions/              # Chat sessions
    ├── <uuid>.json        # Individual session files
    └── ...
```

---

## 🐛 Troubleshooting

### Frontend không load được sessions

1. Kiểm tra backend đang chạy: `http://localhost:8000/health`
2. Restart backend: `docker-compose restart backend`
3. Check logs: `docker-compose logs -f backend`

### Model không thay đổi

1. Đảm bảo click "Save Model"
2. Gửi message mới (không phải reload page)
3. Check settings API: `http://localhost:8000/settings`

### Custom instructions không work

1. Check backend logs
2. Verify API key còn valid
3. Test với message mới

---

## 📝 API Endpoints (New)

### Sessions

- `GET /sessions` - List all sessions
- `POST /sessions` - Create new session
- `GET /sessions/{id}` - Get session details
- `PUT /sessions/{id}` - Update session
- `DELETE /sessions/{id}` - Delete session

### Settings

- `GET /settings` - Get current settings
- `PUT /settings` - Update settings (model, custom_instructions)

---

## 🎯 Next Steps

1. **Restart** your frontend
2. **Refresh** browser tại `http://localhost:8501`
3. **Try** creating a new chat session
4. **Setup** your custom instructions
5. **Test** different models

---

## ⚠️ Notes

- Sessions được lưu dưới dạng JSON files (không dùng database)
- Mỗi session có unique ID (UUID)
- Custom instructions được merge vào system prompt
- Model selection không cần restart backend

---

**Version:** 2.0.0  
**Updated:** 2026-06-14  
**Status:** ✅ Ready to use
