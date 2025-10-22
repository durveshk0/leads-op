# GSBG UI (Next.js + Tailwind)

This small Next.js project provides a modern UI for the GSBG lead portal. It fetches leads from a running FastAPI backend at http://localhost:8000/api/leads and shows a prioritized dashboard (Hot > Warm > Cold).

Quick start (from `ui/`):

1. Install dependencies:

```powershell
npm install
```

2. Run dev server (on port 3001):

```powershell
npm run dev
```

Notes:
- The backend must be running on http://localhost:8000 and CORS enabled for the UI.
- Tailwind requires PostCSS; ensure packages are installed.
- This is a static scaffold — run `npm install` to set up locally.
