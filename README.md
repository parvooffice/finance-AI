# Finance One · Taxometer

A responsive full-stack MVP for the Taxometer tax-planning journey. The project includes a React + TypeScript frontend, an Express API backed by MongoDB, and a separate FastAPI tax-estimate service.

> **Estimate notice:** The tax amounts in this MVP are illustrative estimates, not tax advice. The slab calculation is intentionally simple and must be replaced with reviewed rules for the relevant financial year before real-world use.

## Requirements

- Node.js 20 or newer and npm
- Python 3.10 or newer and pip
- MongoDB Community Server running locally, or a MongoDB Atlas connection string (optional for trying the UI; without MongoDB, the API uses temporary in-memory storage)

## Project layout

```text
frontend/    React + TypeScript + Vite user interface
backend/     Express API, MongoDB persistence, FastAPI proxy
fastapi/     FastAPI estimate service
```

The Finance One landing dashboard shows demo scores for Taxometer, Investometer, Insurometer, HealthMeter, EMI Meter, Protectometer, and Masterometer. Taxometer is the only connected feature; selecting it opens the tax journey backed by Express, MongoDB, and FastAPI. The other meters are display-only placeholders for now.

## Start the app locally

Open three terminals in the project root.

### 1. Start the FastAPI service

```powershell
cd fastapi
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

FastAPI health check: <http://localhost:8001/health>. Interactive API docs: <http://localhost:8001/docs>.

### 2. Start the Express API

```powershell
cd backend
npm install
Copy-Item .env.example .env
npm run dev
```

The API listens at <http://localhost:4001>. Its health check is <http://localhost:4001/api/health>. Set `MONGODB_URI` in `backend/.env` to your MongoDB URL. If MongoDB is not running, the API logs a warning and stores the current journey in memory until the server stops. `FASTAPI_URL` defaults to `http://localhost:8001`.

### 3. Start the React app

```powershell
cd frontend
npm install
npm run dev -- --port 5174
```

Open <http://localhost:5174>. To point the browser at a different API, create `frontend/.env` with:

```dotenv
VITE_API_URL=http://localhost:4001/api
```

## API endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Express and database status |
| `GET` | `/api/journey` | Load the saved demo journey |
| `PUT` | `/api/journey` | Save income details and deduction amounts |
| `POST` | `/api/calculate` | Forward an estimate request to FastAPI |
| `GET` | `http://localhost:8000/health` | FastAPI service status |
| `POST` | `http://localhost:8000/calculate` | Calculate placeholder regime estimates |

Example calculation request to Express:

```json
{"income":1550000,"deductions":500000}
```

## Build the frontend

```powershell
cd frontend
npm run build
```

The production bundle is written to `frontend/dist`. The **Download report** button opens the browser print dialog; choose **Save as PDF** to create a PDF report.

## Deploy to Render

The root `render.yaml` Blueprint creates the React static site, Express API, and FastAPI calculation service. To deploy:

1. Push the project to a GitHub repository and connect that repository to Render.
2. In Render, create a new **Blueprint** and select the repository. Render will read `render.yaml` and create the three services.
3. Add a MongoDB connection string as `MONGODB_URI` for the API service. Without it, the API falls back to temporary in-memory storage and saved journeys can be lost when the service restarts.
4. Wait for the frontend and both API services to finish deploying, then open the frontend's `onrender.com` URL.

The frontend build reads the deployed API hostname from Render and configures the API URL automatically. The services use Render's private network for API-to-calculator requests.

## MVP behavior

- The journey includes income entry, editable deduction cards, and side-by-side regime estimates.
- Income and deduction amounts can be changed; the comparison updates immediately.
- The Express API persists the current journey in MongoDB if configured, with a memory fallback for a quick local demo.
- Express exposes a calculation proxy to FastAPI. The current screen uses an intentionally lightweight local estimate for instant feedback.
- Values are demo data and are not connected to tax filing, identity, or financial accounts.
