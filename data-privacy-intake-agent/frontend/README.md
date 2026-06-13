# Data Privacy Intake Agent - Frontend

This is the Streamlit-based frontend for the Data Privacy Intake Agent MVP.

## Features

- Simple, clean web interface
- Text area for case description input
- Three sample case buttons for quick testing
- Real-time analysis with loading indicator
- Formatted output display with markdown support
- Download analysis results as markdown file
- Responsive design

## Sample Cases

The frontend includes three pre-loaded sample cases:

1. **No Personal Data** - Aggregated reporting case (low risk)
2. **Domestic Sharing** - Customer support with domestic vendor (medium risk)
3. **Cross-Border Transfer** - Credit scoring with Singapore vendor (high risk)

## Running Locally

### Prerequisites

- Python 3.11+
- Backend running on `http://localhost:8000` (or configure `BACKEND_URL`)

### Setup

```bash
cd frontend
pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

The app will be available at http://localhost:8501

### Configuration

Set environment variable to point to backend:

```bash
export BACKEND_URL=http://localhost:8000
streamlit run app.py
```

## Running with Docker

Build the image:

```bash
docker build -t privacy-agent-frontend .
```

Run the container:

```bash
docker run -p 8501:8501 -e BACKEND_URL=http://backend:8000 privacy-agent-frontend
```

## UI Components

### Header Section
- Title and description
- Overview of agent capabilities

### Input Section
- Large text area for case description
- Analyze and Clear buttons

### Sidebar
- Sample case buttons
- About section with version info
- Important notices

### Results Section
- Formatted markdown output
- Mermaid diagram rendering (if supported)
- Download button for analysis

### Footer
- Important disclaimer
- Attribution

## Customization

### Changing Backend URL

Edit `app.py`:

```python
BACKEND_URL = os.getenv("BACKEND_URL", "http://your-backend:8000")
```

### Adding More Sample Cases

Edit the `SAMPLE_CASES` dictionary in `app.py`:

```python
SAMPLE_CASES = {
    "Your Case Name": "Your case description...",
    # ... more cases
}
```

### Styling

Streamlit uses its own theming system. To customize, create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## Tech Stack

- **Framework:** Streamlit 1.28.0
- **HTTP Client:** requests 2.31.0
- **Python:** 3.11

## Known Limitations

- Mermaid diagram rendering depends on Streamlit version
- Large responses may take time to render
- No authentication/authorization (MVP only)
- No session persistence across refreshes

## Future Enhancements

- Add authentication
- Save case history
- Export to PDF
- Real-time status updates
- Dark mode toggle
- Multiple language support
- Case templates management
