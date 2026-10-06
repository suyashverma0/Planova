# ML_PIPELINE.md — Planova Machine Learning Architecture

Planova incorporates a dedicated machine learning pipeline for **Goal Completion Prediction**. The model predicts the probability that a user will successfully complete a goal by its target deadline, classifies the goal into a risk category (Low, Medium, High), and outputs interpretable risk factors.

---

## 1. Problem Formulation & Label Definition

### Target Variable (`goal_completed`)
- **Binary Label**: `goal_completed = 1` if $\ge 95\%$ of required tasks associated with the goal are marked completed by the deadline date; `0` otherwise.

### Snapshot Time Concept
To prevent target leakage, all features are calculated strictly at a snapshot prediction time $t_{\text{snap}}$ prior to the deadline:
$$t_{\text{start}} < t_{\text{snap}} < t_{\text{deadline}}$$
Features consume only historical information available up to $t_{\text{snap}}$.

---

## 2. Feature Specification

The feature store (`ml/src/features.py`) extracts 17 tabular features:

| Feature Name | Type | Description |
| :--- | :--- | :--- |
| `goal_type` | Categorical | Category of the goal ('career', 'academic', 'exam') |
| `goal_complexity` | Numeric | Total estimated required study hours for the goal |
| `deadline_days` | Numeric | Total calendar days from start date to deadline |
| `available_hours_per_day` | Numeric | User's daily allocated time budget (hours/day) |
| `current_skill` | Categorical | User's self-assessed initial skill level |
| `required_hours` | Numeric | Total effort remaining for incomplete tasks |
| `planned_hours` | Numeric | Scheduled hours up to $t_{\text{snap}}$ |
| `completed_hours` | Numeric | Actual logged study hours up to $t_{\text{snap}}$ |
| `completion_ratio` | Numeric | Ratio of completed hours to planned hours ($\frac{\text{completed}}{\text{planned}}$) |
| `tasks_completed` | Numeric | Count of completed tasks |
| `tasks_missed` | Numeric | Count of scheduled tasks missed or unattempted |
| `consistency_rate` | Numeric | Percentage of active days where study hours $>0$ |
| `average_daily_hours` | Numeric | Mean logged hours per day over active window |
| `previous_goal_completion_rate` | Numeric | Historical completion rate of past goals for this user |
| `days_since_start` | Numeric | Elapsed calendar days since goal creation |
| `deadline_pressure` | Numeric | Workload ratio: $\frac{\text{Remaining Hours}}{\text{Remaining Days} \times \text{Daily Available Hours}}$ |
| `milestone_completion_ratio` | Numeric | Fraction of milestones completed ($0.0$ to $1.0$) |

---

## 3. Data Strategy & Synthetic Generation

Since real user telemetry is absent at initial platform launch:
1. **Synthetic Generator (`ml/data_generation/generate_synthetic_data.py`)**:
   - Seeded (`seed=42`) and deterministic for reproducibility.
   - Embeds realistic causal dependencies (e.g., higher `consistency_rate` and `completion_ratio` causally raise completion probability).
   - Generates user behavioral archetypes:
     - *Consistent High Performers*: Steady daily hours, low miss rate.
     - *Burst Workers*: Clustered activity near milestones, high variance.
     - *Overcommitted Users*: High initial goals, low daily availability, declining activity.
     - *Late Starters*: Low initial progress, sharp rise late in timeline.
   - Adds realistic measurement noise and missing data anomalies.
2. **Synthetic Data Labeling**:
   - Every dataset artifact generated is strictly labeled with metadata attribute `is_synthetic: true` in MLflow, DVC, and README files. Synthetic performance metrics are NEVER represented as production user benchmark results.
3. **Real User Ingestion Consent**:
   - Schema and database include `data_consent_given` flags for seamless future ingestion of anonymized, consented real user trajectory data.

---

## 4. Train / Validation / Test Splitting Protocol

- **Grouped Splitting**: To avoid data leakage across multiple snapshot rows from the same user or goal, splitting is performed strictly using `GroupKFold` or `GroupShuffleSplit` grouped by `user_id`.
- **Split Ratio**: 70% Train, 15% Validation, 15% Hold-out Test.
- **Preprocessing Pipeline**: Missing value imputation, standard scaling for numeric features, and one-hot encoding for categorical features fitted ONLY on the training split.

---

## 5. Candidate Models & Evaluation Metric Suite

### Evaluated Models
1. **Baseline**: Rule-based heuristic + Logistic Regression.
2. **Tree Ensembles**: Random Forest, HistGradientBoosting, XGBoost, LightGBM.

### Metric Suite
- **PR-AUC (Precision-Recall Area Under Curve)**: Primary metric due to class imbalance optimization.
- **ROC-AUC**: Secondary discrimination metric.
- **Calibration (Brier Score & Reliability Curves)**: Essential for converting probabilities into trusted UI risk categories (Low: $<30\%$, Medium: $30-65\%$, High: $>65\%$ failure risk).
- **Classification Metrics**: Accuracy, Precision, Recall, F1-Score, Confusion Matrix.

---

## 6. Cold-Start Fallback Heuristic (`heuristic-v1`)

Until a trained ML model is registered in MLflow, the backend prediction service (`app/services/prediction_service.py`) uses a transparent rule-based heuristic:

$$\text{RiskScore} = 0.45 \times (1 - \text{completion\_ratio}) + 0.35 \times \text{deadline\_pressure} + 0.20 \times (1 - \text{consistency\_rate})$$

- If $\text{RiskScore} > 0.65 \rightarrow$ High Risk
- If $0.35 \le \text{RiskScore} \le 0.65 \rightarrow$ Medium Risk
- If $\text{RiskScore} < 0.35 \rightarrow$ Low Risk
- API outputs metadata tag: `"model_version": "heuristic-v1"`.

---

## 7. MLOps Pipeline Architecture (DVC & MLflow)

```
[generate_synthetic_data.py] 
           │
           ▼
     [data/synthetic.csv] (Tracked by DVC)
           │
           ▼
      [dvc.yaml] ────► Stage 1: Validate Data
                     ► Stage 2: Featurize & Split
                     ► Stage 3: Train & Tune (MLflow Tracking)
                     ► Stage 4: Evaluate & Log Artifacts
           │
           ▼
[MLflow Model Registry] ────► [FastAPI Prediction Endpoint]
```
