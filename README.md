# Website Content Search - Semantic Search Application

A full-stack semantic search application that allows users to search through website content using vector embeddings.

## Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note:** First run will download embedding models (~80MB). This happens automatically.

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start Backend Server

1. Navigate to backend directory:
```bash
cd backend
```

2. Activate virtual environment (if not already active):
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Start server:
```bash
uvicorn app.main:app --reload
```

Backend runs on: `http://127.0.0.1:8000`

### Start Frontend Server

1. Open new terminal and navigate to frontend directory:
```bash
cd frontend
```

2. Start development server:
```bash
npm run dev
```

Frontend runs on: `http://localhost:3000`

## Vector Database Configuration

- Uses **ChromaDB** (in-memory)
- No additional configuration required
- Fresh collection created for each search
- No external database setup needed

## Project Structure

```
Semantic Search App/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── scraper.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vectordb.py
│   │   └── models/
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── components/
    ├── package.json
    └── vite.config.js
```

## API Endpoint

**POST** `/search`

Request:
```json
{
  "url": "https://docs.python.org/3/tutorial/introduction.html",
  "query": "how to define functions"
}
```
