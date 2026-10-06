# DEVELOPMENT_PLAN.md — Planova Phase-by-Phase Execution Plan

Planova is built across 11 distinct, sequential phases (Phase 0 to Phase 10). Every phase must meet its exact Acceptance Criteria and pass all tests before receiving approval to proceed to the next phase.

---

## Overview of Phases

| Phase | Phase Name | Focus Area | Status |
| :--- | :--- | :--- | :--- |
| **Phase 0** | Scaffold, Docs, & Configs | Folder layout, documentation, tool configs, notebook stubs | 🔄 **In Progress (This Task)** |
| **Phase 1** | DB Models & Infrastructure | Database schema, Alembic migrations, settings, health checks | ⏳ Pending Approval |
| **Phase 2** | Auth, Users, & Core Goals | Authentication, JWT cookies, User & Goal CRUD endpoints | ⏳ Pending |
| **Phase 3** | Knowledge Base & Decomposition | Skill graph, DAG verification, LLM goal decomposition | ⏳ Pending |
| **Phase 4** | Planning Engine (CP-SAT) | OR-Tools CP-SAT scheduler, constraint solver, infeasibility reports | ⏳ Pending |
| **Phase 5** | Frontend Application | React 18, TypeScript, Tailwind CSS UI components & views | ⏳ Pending |
| **Phase 6** | LLM Integration & NL Progress | LLMClient protocol, NL parser, assistant tool calling, YouTube API | ⏳ Pending |
| **Phase 7** | Synthetic Data & ML Pipeline | Synthetic data generator, notebooks 01–07, model comparison | ⏳ Pending |
| **Phase 8** | MLflow, DVC, & Inference Service | MLflow experiment tracking, DVC pipeline, FastAPI prediction service | ⏳ Pending |
| **Phase 9** | Replanning Engine & Risk UI | Event-driven diff replanning engine, UI risk badges & explanations | ⏳ Pending |
| **Phase 10**| Docker, Telemetry, CI/CD, Hardening | Containerization, Prometheus, Grafana, GitHub Actions, E2E tests | ⏳ Pending |

---

## Detailed Phase Breakdown

### Phase 0: Scaffold, Docs, & Configs (Current)
- **Deliverables**:
  - Root directory structure (`frontend/`, `backend/`, `ml/`, `data/`, `docker/`, `monitoring/`, `scripts/`, `tests/`, `docs/`, `.github/`).
  - Core documentation (`README.md`, `AGENTS.md`, `DEVELOPMENT_PLAN.md`, `docs/DATABASE.md`, `docs/API.md`, `docs/ML_PIPELINE.md`, `docs/ARCHITECTURE.md`).
  - Configuration files (`backend/pyproject.toml`, `frontend/package.json`, `tsconfig.json`, `tailwind.config.js`, `vite.config.ts`, `ml/pyproject.toml`, `dvc.yaml`, `ruff`, `mypy`, `eslint`, `prettier`).
  - ML Jupyter notebooks 01–07 stubbed with valid JSON and section headers.
  - ML python module stubs in `ml/src/` raising `NotImplementedError`.
- **Acceptance Criteria**:
  - File structure intact.
  - All markdown docs complete with technical detail, diagrams, and schemas.
  - Config files valid syntactically.
  - No functional feature code written yet.
- **Risks & Mitigation**:
  - *Risk*: Misaligned database schema or API routes later.
  - *Mitigation*: Comprehensive verification of ERD and API specifications in `docs/` during Phase 0 gate review.

---

### Phase 1: DB Models, Alembic, Settings, Health Checks
- **Deliverables**:
  - PostgreSQL 16 schema setup in SQLAlchemy 2.x models (`app/models/`).
  - Initial Alembic migration scripts (`backend/alembic/`).
  - Environment settings module (`app/core/config.py`) using Pydantic Settings v2.
  - Health check endpoints (`GET /api/v1/health`, `/ready`).
  - Database connection pool tests and session management fixtures.
- **Acceptance Criteria**:
  - Alembic migrations upgrade/downgrade cleanly against PostgreSQL 16.
  - Health endpoint checks PostgreSQL and Redis connections accurately.
  - Unit tests in `backend/tests/test_health.py` pass 100%.
- **Risks & Mitigation**:
  - *Risk*: Async database driver incompatibilities.
  - *Mitigation*: Standardize on `asyncpg` with explicit connection pool parameters.

---

### Phase 2: Auth, Users, Goals, Milestones, Tasks
- **Deliverables**:
  - User registration, login, logout, token refresh endpoints (`/api/v1/auth/*`).
  - Argon2id password hashing + JWT token cookies (`httpOnly`, `Secure`, `SameSite=Strict`).
  - CRUD services & endpoints for Goals, Milestones, and Tasks (`/api/v1/goals/*`).
  - Authorization middleware ensuring multi-tenant user data isolation.
  - Pytest suite covering auth flows and goal validation.
- **Acceptance Criteria**:
  - Complete security test coverage: unauthenticated users cannot access goal resources.
  - JWT rotation works cleanly without leaking tokens into localStorage.
  - All test cases pass with clean code linting (`ruff` & `mypy`).
- **Risks & Mitigation**:
  - *Risk*: Security holes in cookie handling.
  - *Mitigation*: Test CSRF protection and strict cookie options in isolation.

---

### Phase 3: Knowledge Base, Skill Graph, Goal Decomposition
- **Deliverables**:
  - Structured skill graph seed data (`data/knowledge_base/*.yaml`) for ML Engineer, Data Scientist, Web Developer, NIMCET.
  - Database seed script populating `skills` and `skill_edges` tables.
  - Graph verification module (`app/services/skill_graph.py`) enforcing Directed Acyclic Graph (DAG) for prerequisite edges.
  - LLM goal decomposition service parsing input goals into candidate milestones, skills, topics, and tasks.
- **Acceptance Criteria**:
  - Skill graph validation detects cycle insertion and raises validation errors.
  - Goal decomposition falls back to knowledge base standards if LLM parsing fails or produces invalid dependencies.
  - Unit tests for DAG verification and skill lookups pass.
- **Risks & Mitigation**:
  - *Risk*: LLM producing hallucinated or cyclic skill dependencies.
  - *Mitigation*: Knowledge base acts as the hard constraint layer; LLM output is strictly mapped onto KB nodes.

---

### Phase 4: Planning Engine (CP-SAT Scheduling & Allocation)
- **Deliverables**:
  - Google OR-Tools CP-SAT scheduler (`app/planning/scheduler.py`).
  - Hard constraint formulation (daily capacity, prerequisite ordering, blocked times, max task duration).
  - Soft constraint optimization objective (maximizing priority, urgency, milestone momentum, work consistency).
  - Infeasibility diagnostic report generator returning actionable feedback (e.g., extend deadline, add daily hours).
  - Test suite with complex schedule scenarios (e.g., exam crunch, multi-goal collision).
- **Acceptance Criteria**:
  - Scheduler runs deterministically (fixed random seed, fixed solver time limit).
  - Valid schedules violate zero hard constraints.
  - Infeasible requests return explicit diagnostic reports with actionable options instead of invalid schedules.
- **Risks & Mitigation**:
  - *Risk*: CP-SAT solver timeout on large multi-month schedules.
  - *Mitigation*: Horizon sliding window approach combined with hard solver timeout limits (e.g., 5 seconds).

---

### Phase 5: Frontend Application (Design System & Core Screens)
- **Deliverables**:
  - Planova original design system (Tailwind tokens, typography scale, color palette, accessible components).
  - Core views: Landing, Auth (Login/Signup), Multi-goal Onboarding wizard, Dashboard, Goal Detail + Roadmap view, Planner (Daily/Weekly view), Progress tracker, Settings.
  - State management & API integration via TanStack Query and Axios/Fetch client.
  - Vitest + React Testing Library component tests.
- **Acceptance Criteria**:
  - Keyboard accessible (WCAG AA compliant contrast ratios).
  - Zero placeholder UI copy or generic AI styling.
  - Dashboard accurately renders today's plan, streaks, active goals, and upcoming deadlines.
  - All frontend unit tests pass.
- **Risks & Mitigation**:
  - *Risk*: Complex roadmap visualization breaking layout.
  - *Mitigation*: Modular SVG/Tailwind tree rendering with fallback linear views.

---

### Phase 6: LLM Integration, NL Progress Updates, Resource Engine
- **Deliverables**:
  - Production `LLMClient` protocol with provider adapters (e.g., OpenAI / generic LLM) and Pydantic response validation.
  - Natural Language update parser handling English & Hinglish ("Aaj sirf 2 hours hain", "SQL completed").
  - AI Assistant tool calling over Planova service layer (`get_today_plan`, `replan`, `set_availability`, etc.).
  - Resource recommendation pipeline with YouTube Data API candidate fetching, caching in Redis, and multi-factor ranking.
- **Acceptance Criteria**:
  - All natural language updates require user confirmation before applying destructive state changes.
  - Assistant calls service actions exclusively (zero direct DB mutations or hallucinations).
  - YouTube API quota limits respected with Redis caching and graceful fallback if API keys are missing.
- **Risks & Mitigation**:
  - *Risk*: Hinglish parsing ambiguity leading to corrupted availability state.
  - *Mitigation*: User confirmation modal displays parsed intent before committing updates.

---

### Phase 7: Synthetic Data, Notebooks 01–07, Model Comparison
- **Deliverables**:
  - `ml/data_generation/generate_synthetic_data.py` producing realistic multi-goal student trajectories with causal relationships, noise, and archetypes.
  - Fully executed Jupyter notebooks (`ml/notebooks/01_exploration.ipynb` through `07_explainability.ipynb`).
  - Model evaluation comparing Logistic Regression, Random Forest, HistGradientBoosting, XGBoost, and LightGBM.
  - Feature importance, permutation importance, and SHAP explainability analyses.
- **Acceptance Criteria**:
  - Datasets labeled explicitly as **synthetic** in metadata and notebooks.
  - Stratified user/goal grouped split preventing row leakage.
  - Model selection based on PR-AUC, Brier calibration score, and complexity tie-breaker.
- **Risks & Mitigation**:
  - *Risk*: Overfitting to synthetic artifacts.
  - *Mitigation*: Introduce realistic noise, non-linear interactions, edge cases (burst workers, late starters), and drop trivial identifiers.

---

### Phase 8: MLflow, DVC, Production Inference, Cold-Start Switch
- **Deliverables**:
  - DVC pipeline (`ml/dvc.yaml`) reproducing generation, featurization, training, and evaluation steps.
  - MLflow tracking integration logging params, metrics, ROC/PR curves, and registering the best model artifact.
  - Modular ML package (`ml/src/features.py`, `preprocessing.py`, `train.py`, `evaluate.py`, `predict.py`).
  - Prediction service in backend (`app/services/prediction_service.py`) loading MLflow model for `/api/v1/predictions`.
  - Transparent fallback heuristic (`model_version: "heuristic-v1"`) when registered ML model is absent.
- **Acceptance Criteria**:
  - `dvc repro` executes cleanly end-to-end.
  - FastAPI prediction endpoint responds with calibrated completion probability, risk category (Low/Med/High), top risk factors, and active model version.
  - Cold-start heuristic activates seamlessly if no model is loaded.
- **Risks & Mitigation**:
  - *Risk*: Latency spike on model load during API requests.
  - *Mitigation*: Singleton pattern for model loading on application startup with warm-up prediction.

---

### Phase 9: Dynamic Replanning Engine & Risk UI Integration
- **Deliverables**:
  - Event-driven replanning engine (`app/planning/replanning_engine.py`) triggered by missed tasks, reduced time, or priority changes.
  - Replanning diff generator producing structured output (moved, delayed, or added tasks with explicit explanations).
  - Risk notification banner & explanation panel in Frontend dashboard.
- **Acceptance Criteria**:
  - Replanning logic is 100% deterministic (no LLM invocation for schedule calculation).
  - Replanning outputs clear visual diff showing *what changed* and *why*.
  - User can review and accept/reject proposed schedule adjustments.
- **Risks & Mitigation**:
  - *Risk*: Replanning cascade creating daily overload.
  - *Mitigation*: Cap maximum daily capacity and trigger goal deadline extension warnings if overload threshold is breached.

---

### Phase 10: Docker, Telemetry, CI/CD, Production Hardening
- **Deliverables**:
  - Production Dockerfiles & `docker-compose.yml` orchestrating PostgreSQL, Redis, FastAPI, Celery, React/Nginx, Prometheus, Grafana, MLflow.
  - Prometheus metrics exporter collecting HTTP request counts, CP-SAT solve duration, prediction latency, and Celery job queue depth.
  - Grafana dashboard JSON configurations (`monitoring/dashboards/`).
  - GitHub Actions CI workflow (`.github/workflows/ci.yml`) executing ruff, mypy, pytest, pnpm lint, pnpm test, and docker build.
  - End-to-end test suite (`tests/e2e/`).
- **Acceptance Criteria**:
  - `docker-compose up` boots entire stack cleanly with healthy status.
  - GitHub Actions CI pipeline passes all linting, type-checking, unit, and E2E tests.
  - Comprehensive documentation finalized across `docs/` and `README.md`.
- **Risks & Mitigation**:
  - *Risk*: Flaky E2E tests in CI environment.
  - *Mitigation*: Seed database deterministically and use explicit wait-for-health checks before running tests.
