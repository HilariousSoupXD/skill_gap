# Skill Sketch - Campus Skill Gap Analyzer

A skill gap analysis tool that helps students visualize their proficiency levels, identify missing skills, and get personalized learning plans with curated resources for target tech roles.

🌐 **Live Demo**: [https://skillsketch.vercel.app/](https://skillsketch.vercel.app/)

## ✨ Features

- **📊 Visual Skill Assessment**: Interactive radar charts showing your strengths and gaps
- **🎯 Role-Based Analysis**: Evaluate your skills against industry roles (SDE, Data Scientist, etc.)
- **📚 Personalized Learning Plans**: Automatic week-by-week schedules with prioritized resources
- **🔍 Gap Identification**: Detailed breakdown of skill gaps with explanations
- **📖 Curated Resources**: Hand-picked courses, tutorials, and practice materials
- **💾 Evaluation History**: Track your progress over time

## 🛠️ Tech Stack

### Frontend
- **React 19** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons

### Backend
- **Flask** - Python web framework
- **SQLite** - Database
- **NumPy** - Numerical computations
- **Gunicorn** - Production server

### Deployment
- **Vercel** - Frontend hosting
- **Render** - Backend hosting

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/HilariousSoupXD/skill_gap.git
cd skill_gap
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will be available at `http://127.0.0.1:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional, for local development):
```env
VITE_API_BASE_URL=http://127.0.0.1:5000
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📡 API Endpoints

### `POST /evaluate`
Evaluate a student's skill profile against a target role.

**Request Body:**
```json
{
  "role": "SDE",
  "student_profile": {
    "DSA": 0.6,
    "OS": "beginner",
    "Python": 0.8
  },
  "weekly_hours": 10,
  "weeks": 4
}
```

**Response:**
```json
{
  "evaluation_id": 123,
  "alignment_score": 0.75,
  "readiness_score": 0.56,
  "top_gaps": [["DSA", 0.12], ...],
  "plan": { ... }
}
```

### `GET /roles`
Get all available roles and their required skills.

**Response:**
```json
[
  {
    "id": "SDE",
    "label": "SDE",
    "description": "Core CS & Systems",
    "icon": "code",
    "skills": ["DSA", "OS", "Python", ...]
  }
]
```

## 📁 Project Structure

```
skill_gap/
├── app.py                 # Flask backend application
├── module1_vectors.py     # Skill vector representations
├── module2_models.py       # Role definitions and requirements
├── module3_evaluator.py   # Skill gap evaluation engine
├── module4_recommender.py # Learning plan generator
├── requirements.txt       # Python dependencies
├── evaluations.db        # SQLite database
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.jsx       # Main app component
│   │   └── config.js    # API configuration
│   └── package.json      # Node dependencies
├── DEPLOYMENT.md         # Detailed deployment guide
└── QUICK_DEPLOY.md       # Quick deployment checklist
```

## 🚢 Deployment

This project is configured for free-tier deployment:

- **Backend**: Deploy to [Render](https://render.com) (free tier)
- **Frontend**: Deploy to [Vercel](https://vercel.com) (free tier)

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions or [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) for a quick checklist.

### Environment Variables

**Frontend (Vercel):**
- `VITE_API_BASE_URL` - Your Render backend URL (e.g., `https://your-backend.onrender.com`)

**Backend (Render):**
- `PYTHON_VERSION` - Python version (default: 3.12.0)

## 🎯 How It Works

1. **Select Role**: Choose your target role (SDE, Data Scientist, etc.)
2. **Input Skills**: Enter your proficiency levels for each skill
3. **Get Analysis**: View your alignment score, readiness score, and skill gaps
4. **Receive Plan**: Get a personalized week-by-week learning plan with resources

## 📝 Development

### Running Tests
```bash
# Backend tests (if available)
python -m pytest

# Frontend tests (if available)
cd frontend
npm test
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Built with ❤️ for the hackathon
- Uses curated educational resources from various platforms
- Inspired by the need for better skill gap analysis in education

---

**Note**: This is a hackathon project. For production use, consider adding authentication, more robust error handling, and additional features.

