# API.md — Planova REST API Specification

Planova exposes a fully versioned RESTful API under the base path `/api/v1`.

---

## Architecture & Conventions

- **Base URL**: `http://localhost:8000/api/v1` (Development) / `https://api.planova.io/api/v1` (Production)
- **Content Type**: `application/json`
- **Authentication**: JWT tokens stored in `httpOnly`, `Secure`, `SameSite=Strict` cookies (`access_token` and `refresh_token`).
- **Rate Limiting**: Enforced via Redis middleware. Default limit: 60 requests/minute per authenticated user, 20 requests/minute for auth endpoints.

---

## Unified Error Schema

All API error responses follow a strict Pydantic-validated JSON structure:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Goal with ID '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d' was not found.",
    "status": 404,
    "timestamp": "2026-10-07T10:00:00Z",
    "trace_id": "req-8f921a-4c21",
    "details": [
      {
        "field": "goal_id",
        "issue": "Invalid UUID or non-existent entity"
      }
    ]
  }
}
```

Common Error Codes:
- `UNAUTHORIZED` (401): Missing or expired access token.
- `FORBIDDEN` (403): User lacks permission for the requested resource.
- `NOT_FOUND` (404): Entity does not exist.
- `VALIDATION_ERROR` (422): Request body or parameter validation failed.
- `INFEASIBLE_SCHEDULE` (422): CP-SAT solver failed to find a valid schedule.
- `RATE_LIMIT_EXCEEDED` (429): Quota exceeded.
- `INTERNAL_SERVER_ERROR` (500): Unexpected system error.

---

## Endpoint Modules Overview

### 1. `/auth` — Authentication & Session Management
- `POST /api/v1/auth/register` — Register a new account.
- `POST /api/v1/auth/login` — Authenticate credentials, set httpOnly JWT cookies.
- `POST /api/v1/auth/logout` — Clear token cookies and invalidate session in Redis.
- `POST /api/v1/auth/refresh` — Rotate refresh token and issue new access token cookie.
- `GET  /api/v1/auth/me` — Retrieve current authenticated user profile.

### 2. `/goals` — Goal & Milestone Lifecycle
- `POST /api/v1/goals` — Create a new goal.
- `GET  /api/v1/goals` — List user's active/paused/completed goals (paginated).
- `GET  /api/v1/goals/{id}` — Get single goal details with milestones and tasks.
- `PATCH /api/v1/goals/{id}` — Edit goal title, deadline, priority, daily hours, or status.
- `DELETE /api/v1/goals/{id}` — Soft delete goal and associated schedule items.
- `POST /api/v1/goals/decompose` — LLM-assisted goal decomposition into validated milestones and tasks.

### 3. `/planner` — Constraint Optimization & Scheduling
- `POST /api/v1/planner/generate` — Trigger CP-SAT optimization engine to build schedule.
- `GET  /api/v1/planner/today` — Retrieve today's scheduled tasks and time slots.
- `GET  /api/v1/planner/weekly` — Retrieve 7-day schedule view.
- `POST /api/v1/planner/replan` — Trigger event-driven deterministic replanning diff engine.

### 4. `/progress` — Progress Tracking & Natural Language Updates
- `POST /api/v1/progress/log` — Record task completion or manual study hours.
- `POST /api/v1/progress/natural-language` — Process English/Hinglish update (e.g. "Aaj 2 hrs hain"). Returns parsed intent for user confirmation.
- `POST /api/v1/progress/confirm-intent` — Apply confirmed natural language intent changes.
- `GET  /api/v1/progress/stats` — Retrieve completion ratios, streaks, and study time analytics.

### 5. `/resources` — Resource Recommendation Engine
- `GET  /api/v1/resources/task/{task_id}` — Get ranked recommendations for a specific task.
- `GET  /api/v1/resources/skill/{skill_id}` — Get top-ranked videos/docs for a skill node.

### 6. `/assessment` — Diagnostic & Initial Skill Assessment
- `GET  /api/v1/assessment/questions` — Fetch initial question set for a domain/category.
- `POST /api/v1/assessment/submit` — Submit answers, calculate initial skill scores, and update user profile.

### 7. `/predictions` — Goal Completion ML Risk Prediction
- `GET  /api/v1/predictions/goal/{goal_id}` — Get ML completion probability, risk category (Low/Med/High), SHAP risk factors, and active model version.
- `GET  /api/v1/predictions/dashboard` — Get aggregated risk predictions across all user goals.

### 8. `/assistant` — AI Assistant (Tool Calling Interface)
- `POST /api/v1/assistant/chat` — Send message to assistant. Assistant uses strict tool-calling over Planova services (e.g., `get_today_plan`, `set_availability`, `explain_risk`). Returns message response and confirmable actions.
