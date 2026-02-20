# Trimgram - Instagram Follower Analyzer

**Clean up who you follow. One tap at a time.**

Trimgram is a web application that helps you identify and unfollow Instagram accounts that don't follow you back. It ranks non-followers by your interaction with their content, showing you the accounts you engage with least first.

## Features

- **Smart Analysis**: Identifies accounts that don't follow you back
- **Interaction-Based Ranking**: Ranks non-followers by how much you've engaged with their content (least interaction first)
- **One-Tap Unfollow**: Unfollow accounts directly from the app with confirmation
- **Privacy-First**: No database, no persistent storage, open source code
- **Mobile-Ready**: Works perfectly on iPhone Safari and all modern browsers

## Important Disclaimers

⚠️ **Unofficial API**: This app uses Instagram's unofficial private API via the `instagrapi` library. This is not affiliated with or endorsed by Instagram or Meta. Using this tool carries a small risk of your account being temporarily rate-limited or flagged by Instagram.

🔒 **Security**: Your Instagram password is NEVER stored. It's used only to create a temporary session (30 minutes max) and then discarded. All code is open source for verification.

## Architecture

Trimgram follows **Clean Architecture** and **SOLID principles** throughout. The codebase is designed to be readable, testable, and maintainable.

### Backend Architecture

The backend is built with **Python FastAPI** and structured in clearly separated layers:

```
backend/
├── routers/          # API Layer - HTTP handlers only, zero business logic
│   ├── auth.py       # Login and 2FA endpoints
│   ├── analysis.py   # Follower analysis endpoint
│   └── unfollow.py   # Unfollow endpoint
├── services/         # Service Layer - ALL business logic lives here
│   ├── auth_service.py       # Authentication logic
│   ├── analysis_service.py   # Follower comparison and interaction scoring
│   └── unfollow_service.py   # Unfollow logic with rate limiting
├── integrations/     # Integration Layer - External API calls isolated here
│   ├── interfaces.py         # Abstract interfaces (ISP)
│   └── instagram_client.py   # Concrete instagrapi implementation
├── models/           # Domain Layer - Pure Pydantic models
│   ├── domain.py     # Core entities: User, Session, InteractionScore, etc.
│   ├── api.py        # Request/Response models for HTTP endpoints
│   └── exceptions.py # Custom exception types
├── infrastructure/   # Infrastructure Layer - Config, session storage
│   ├── config.py     # Environment variable configuration
│   └── session_store.py  # In-memory session storage
├── dependencies.py   # Dependency injection container
└── main.py          # FastAPI application entry point
```

#### SOLID Principles Implementation

**Single Responsibility Principle (S)**
- `AuthService` only handles authentication
- `AnalysisService` only handles follower analysis and scoring
- `UnfollowService` only handles unfollowing
- Each router handles only HTTP concerns for its domain

**Open/Closed Principle (O)**
- All Instagram operations are behind abstract interfaces
- You can swap `InstagrapiClient` for a different implementation without touching any service code

**Liskov Substitution Principle (L)**
- Any implementation of `InstagramAuthInterface`, `InstagramFollowerInterface`, or `InstagramUnfollowInterface` is a safe drop-in replacement
- Enables unit testing with mocks

**Interface Segregation Principle (I)**
- Narrow, focused interfaces: `InstagramAuthInterface`, `InstagramFollowerInterface`, `InstagramUnfollowInterface`
- Services only depend on what they actually use

**Dependency Inversion Principle (D)**
- Services depend on abstractions (interfaces), not concrete implementations
- All dependencies are injected via FastAPI's `Depends()` system
- No service ever instantiates its own dependencies

### Frontend Architecture

The frontend is built with **React + Vite + Tailwind CSS**:

```
frontend/
├── src/
│   ├── components/
│   │   ├── LoginForm.jsx      # Login screen with disclaimer
│   │   ├── LoadingScreen.jsx  # Analysis loading screen
│   │   ├── ResultsList.jsx    # Ranked non-followers list
│   │   ├── ResultRow.jsx      # Single non-follower row with unfollow button
│   │   └── PrivacyPolicy.jsx  # Privacy policy page
│   ├── services/
│   │   └── api.js             # API service module - ALL API calls here
│   ├── App.jsx                # Main app component
│   └── index.css              # Tailwind + global styles
```

**Frontend Principles**
- **Single-purpose components**: Each component does one thing
- **No business logic in components**: API calls go through `api.js`
- **Error handling everywhere**: No silent failures
- **No hardcoded URLs**: Environment variables for API configuration

## How It Works

### 1. Authentication
- User logs in with Instagram username and password
- `instagrapi` creates a session with Instagram's private API
- Session token is generated and stored in memory (30-minute TTL)

### 2. Follower Analysis
- Fetches user's followers and following lists
- Identifies accounts that don't follow back
- For each non-follower:
  - Fetches their last 12 posts
  - Checks if YOU liked or commented on those posts
  - Calculates interaction score = your likes + your comments on their posts

### 3. Ranking
- Non-followers are sorted **ascending** by interaction score
- Accounts with 0 interaction appear first
- Top 100 least-interacted accounts are shown

### 4. Unfollowing
- Tap "Unfollow" on any account
- Confirmation dialog appears
- On confirm, unfollow API is called with rate limiting (15-second delay between unfollows)
- Row is removed from UI on success

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
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

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Run the server:
```bash
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Run the development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## Deployment

### Backend (Railway)
1. Push code to GitHub
2. Connect your GitHub repo to Railway
3. Set environment variables in Railway dashboard
4. Deploy

### Frontend (Vercel)
1. Push code to GitHub
2. Import project in Vercel
3. Set `VITE_API_URL` to your Railway backend URL
4. Deploy

## Security & Privacy

### What We DON'T Do
- ❌ Store your password (ever, anywhere)
- ❌ Use a database
- ❌ Track analytics
- ❌ Share data with third parties
- ❌ Log credentials

### What We DO
- ✅ Use HTTPS for all communication
- ✅ Store sessions in memory only (30-minute TTL)
- ✅ Open source all code for verification
- ✅ Implement rate limiting to protect your account
- ✅ Never commit secrets to GitHub

### Session Flow
1. Login creates temporary session in server memory
2. Session token is a random UUID
3. Session expires after 30 minutes
4. Only ONE session can exist at a time
5. All session data is deleted on expiration

## Configuration

### Backend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `False` | Enable debug mode |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:5173` | Allowed frontend origins |
| `SESSION_TTL_SECONDS` | `1800` | Session lifetime (30 minutes) |
| `INSTAGRAM_REQUEST_DELAY` | `2.0` | Delay between Instagram API requests (seconds) |
| `MAX_NON_FOLLOWERS_SHOWN` | `100` | Maximum results to return |
| `POSTS_TO_ANALYZE` | `12` | Number of posts to analyze per account |
| `UNFOLLOW_DELAY_SECONDS` | `15.0` | Delay between unfollows (seconds) |

### Frontend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | Backend API URL |

## Development

### Running Tests (Backend)
```bash
cd backend
pytest tests/
```

### Code Quality
- All functions have type hints
- All functions have docstrings
- Pydantic models for all API I/O
- No hardcoded values (all env vars)

## Limitations & Future Enhancements

### Current Limitations
- 2FA support is basic (shows error message)
- No bulk unfollow (intentional - prevents aggressive unfollowing)
- No whitelist feature
- No persistent login (session expires after 30 minutes)

### Planned Enhancements
- Full 2FA flow with code input
- Account age display (how long you've been following them)
- CSV export
- Better progress indicators during analysis

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow the existing code style and architecture
4. Add tests for new features
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgements

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Instagram integration via [instagrapi](https://github.com/subzeroid/instagrapi)
- Frontend powered by [React](https://react.dev/), [Vite](https://vite.dev/), and [Tailwind CSS](https://tailwindcss.com/)

## Disclaimer

This project is not affiliated with, endorsed by, or connected to Instagram or Meta Platforms, Inc. Use at your own risk. The developers are not responsible for any consequences resulting from the use of this tool, including but not limited to account suspension, rate limiting, or data loss.

---

**Made with ❤️ by the open source community**

For questions, issues, or feature requests, please open an issue on GitHub.
