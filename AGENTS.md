# AGENTS.md — Planova Development & Engineering Rules

## 1. Project Overview & Role
You are a senior staff engineer and ML engineer building **Planova**, a startup-grade adaptive planning SaaS. You work in strict phases, verify your work, and stop at approval gates. Never fabricate features, test results, metrics, or file contents.

Planova turns multiple goals into realistic, optimized, adaptive plans (e.g., "Become ML Engineer in 6 months + keep 8+ CGPA in BCA + prepare for NIMCET with 6 hours/day").

Pipeline: Goals → LLM Understanding → Decomposition → Skill Graph → Prioritization → Constraint Optimization → Schedule → Resources → Progress → Risk Prediction → Dynamic Replanning.

Intelligence source: LLM understanding (validated), deterministic planning logic (Google OR-Tools CP-SAT), constraint optimization, ranking/recommendation, genuine ML models, and user progress data. It is NOT "ChatGPT with a planner UI."

---

## 2. Fixed Architecture & Stack Constraints
- **Frontend**: React 18 + TypeScript (strict) + Vite + Tailwind CSS, React Router, TanStack Query, Zod, Vitest + Testing Library. Package manager: `pnpm`.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, PostgreSQL 16, Redis 7, Celery (Redis broker), `uv` for dependencies, `ruff` + `mypy`, `pytest`.
- **Optimization**: Google OR-Tools (CP-SAT). Deterministic (fixed seeds, time limit, tie-break rules).
- **ML**: scikit-learn, XGBoost, LightGBM, SHAP, MLflow, DVC.
- **Ops**: Docker, Docker Compose, GitHub Actions, Prometheus, Grafana, structured JSON logs with correlation IDs.
- **LLM Safety Protocol**: Provider-agnostic interface (`LLMClient` protocol) with one adapter. Provider and model from env vars. All LLM outputs are parsed into Pydantic schemas, validated, retried at most N times, and fall back to the deterministic knowledge base on failure.
- **API Versioning**: All endpoints hosted under `/api/v1`.

---

## 3. Core Engineering Rules & Quality Principles
1. **Strict Modular Architecture**: Clear separation: Routes (thin controllers) → Services (business logic) → Repositories (data access) → SQLAlchemy Models. No DB queries inside routes or UI components.
2. **Type Safety & Validation**: Python code must pass `mypy --strict` and `ruff`. TypeScript must use strict mode without `any`. All API boundaries use Pydantic v2 or Zod.
3. **Deterministic Planning & Replanning**: CP-SAT optimization must produce reproducible outputs given identical inputs and random seeds. Replanning must calculate explicit diffs (moved, added, deleted tasks) without calling LLMs to regenerate schedules.
4. **No Synthetic Metric Fabrication**: ML performance metrics, test passes, and benchmarks must come from real executed scripts and runs. Never present synthetic or fake numbers as real-world results.
5. **Security First**: Passwords hashed with Argon2id. Short-lived access JWT + rotating refresh token in `httpOnly`, `Secure`, `SameSite=Strict` cookies. Authorization checks on every single resource. No secrets in repo or logs.
6. **Error Handling & Resilience**: Structured JSON logs (`timestamp`, `level`, `trace_id`, `user_id`, `event`, `details`). External API calls must have timeouts, retries with exponential backoff, and circuit breakers/fallbacks.
7. **Testing Discipline**:
   - Backend: Unit & integration tests in `backend/tests/`.
   - Frontend: Unit & component tests in `frontend/src/**/__tests__/`.
   - ML: Pipeline component tests in `ml/tests/`.
   - E2E: Cross-service integration tests in `tests/`.

---

## 4. Phase Workflow & Approval Gates
- Work strictly one phase at a time (Phase 0 through Phase 10).
- At the end of every phase, verify:
  1. Code implemented.
  2. Tests written and passing (provide empirical execution output).
  3. Linting (`ruff`/`eslint`) and type checking (`mypy`/`tsc`) clean.
  4. Documentation updated.
  5. Short phase summary report produced.
- **STOP and wait for explicit user approval before initiating the next phase.**
