# 🤖 Self-Healing DevOps Agent

An **agentic AI system** built with LangGraph that autonomously monitors Kubernetes workloads, diagnoses failures using an LLM, and either auto-remediates the issue or escalates it to a human — complete with observability, memory, and safety guardrails.

---

## 📌 Why this project

Traditional monitoring tools tell you *something is wrong*. This agent goes a step further: it **investigates**, **decides**, and **acts** — restarting pods, scaling deployments, or rolling back bad releases — while keeping humans in the loop for anything it isn't confident about.

It was built to explore how agentic AI (LangGraph + an LLM) can be applied to real DevOps/SRE workflows, not just chatbots.

---

## 🧠 How it works — Agent Flow

```
Observe → Diagnose → Decide → Act → Verify → Log
```

| Node | Responsibility |
|------|-----------------|
| **Observe** | Collects logs and live metrics from the cluster (Prometheus) |
| **Diagnose** | Sends logs/metrics to an LLM (Groq — Llama 3.3 70B), enriched with similar past incidents via RAG, to produce a diagnosis + confidence score |
| **Decide** | If confidence ≥ threshold (0.75) → auto-fix path. Otherwise → escalate for manual review |
| **Act** | Auto-fix: restarts/scales/rolls back the pod or deployment. Escalate: opens a GitHub issue |
| **Verify** | Confirms the outcome and sets the final status |
| **Log** | Persists the incident to SQLite, sends Slack/Email alerts, and updates Prometheus metrics for the agent itself |

Each incident is treated as a stateful run, tracked end-to-end and checkpointed via LangGraph's memory layer.

---

## ✨ Key Features

- **🔍 RAG-Enhanced Diagnosis** — retrieves similar past incidents (via FAISS + sentence-transformers embeddings) and feeds them to the LLM for better, pattern-aware diagnoses
- **🧵 Agent Memory** — LangGraph `MemorySaver` checkpoints state per-incident thread
- **🔧 Kubernetes Remediation** — pod restarts, deployment scaling, and rollbacks via the Kubernetes Python client + `kubectl`
- **📊 Real-Time Metrics** — pulls live CPU/memory data from Prometheus instead of relying on static values
- **🔁 CI/CD Awareness** — detects failed GitHub Actions workflow runs as a source of incidents
- **🚨 Multi-Channel Alerting** — Slack and Email notifications for every incident
- **📄 PDF Incident Reports** — auto-generated, downloadable reports per incident
- **📈 Agent Self-Observability** — the agent exposes its own Prometheus metrics (incidents handled, confidence distribution) visualized in Grafana
- **🔒 Least-Privilege Security** — dedicated Kubernetes ServiceAccount/Role/RoleBinding scoped to only the permissions the agent needs
- **✅ Full Test Coverage** — unit tests (with mocking), integration tests (against a live Minikube cluster), and end-to-end tests covering both the auto-fix and escalation paths

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Orchestration | LangGraph |
| LLM | Groq API (Llama 3.3 70B Versatile) |
| RAG | sentence-transformers (`all-MiniLM-L6-v2`) + FAISS |
| Backend / Dashboard | FastAPI, Streamlit |
| Storage | SQLite |
| Container Orchestration | Kubernetes (Minikube) |
| Observability | Prometheus, Grafana, LangSmith |
| Alerting | Slack, Gmail SMTP |
| Testing | pytest, unittest.mock |
| CI/CD Integration | GitHub Actions API, PyGithub |
| Reporting | fpdf2 |
| Containerization | Docker |

---

## 📂 Project Structure

```
self-healing-devops-agent/
├── app/
│   └── main.py                # Target FastAPI app (/health, /process, /risky, /metrics)
├── agent/
│   ├── state.py                # AgentState schema
│   ├── nodes.py                 # observe, diagnose, decide, act, verify, log
│   ├── graph.py                  # LangGraph graph + MemorySaver
│   ├── rag_tool.py                # Embedding + FAISS similarity search
│   └── metrics.py                  # Agent's own Prometheus metrics
├── tools/
│   ├── k8s_tool.py               # restart_pod, scale_deployment, rollback_deployment
│   ├── github_tool.py             # create_issue, check_ci_failures
│   ├── slack_tool.py               # send_slack_alert
│   ├── prometheus_tool.py           # query_prometheus
│   ├── email_tool.py                 # send_email_alert
│   └── pdf_tool.py                    # generate_incident_report
├── api/
│   ├── database.py                # SQLite persistence layer
│   └── main.py                      # FastAPI: /status, /incidents
├── dashboard/
│   └── app.py                    # Streamlit incident dashboard
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── servicemonitor.yaml
│   ├── alert-rules.yaml
│   └── rbac.yaml                 # ServiceAccount / Role / RoleBinding
├── tests/
│   ├── test_nodes.py             # Unit tests (with mocking)
│   ├── test_integration.py        # Integration tests (live cluster)
│   └── test_e2e.py                 # End-to-end tests (full graph)
├── reports/                     # Generated PDF incident reports
├── .env                         # API keys & config (not committed)
├── Dockerfile
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Docker
- Minikube
- Helm

### 1. Clone and set up the environment

```bash
git clone https://github.com/malikuzair22/self-healing-devops-agent.git
cd self-healing-devops-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_key
LANGSMITH_API_KEY=your_langsmith_key
GITHUB_TOKEN=your_github_token
GITHUB_REPO=your_username/your_repo
SLACK_WEBHOOK_URL=your_slack_webhook
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=where_to_send@example.com
CONFIDENCE_THRESHOLD=0.75
```

### 3. Start the Kubernetes cluster

```bash
minikube start --driver=docker --memory=1800 --cpus=2
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/servicemonitor.yaml
kubectl apply -f k8s/alert-rules.yaml
kubectl apply -f k8s/rbac.yaml
```

### 4. Install monitoring stack

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set grafana.adminPassword=admin123
```

### 5. Run the components

```bash
# Terminal 1 — API
uvicorn api.main:app --reload --port 8080

# Terminal 2 — Dashboard
streamlit run dashboard/app.py

# Terminal 3 — Run the agent
python3 -m agent.graph
```

### 6. Run the tests

```bash
python3 -m pytest tests/test_nodes.py -v         # Unit tests
python3 -m pytest tests/test_integration.py -v   # Integration tests (needs live cluster)
python3 -m pytest tests/test_e2e.py -v            # End-to-end tests
```

---

## 🗺️ Roadmap

- [x] Core agent graph (Observe → Diagnose → Decide → Act → Verify → Log)
- [x] RAG-based diagnosis
- [x] Agent memory
- [x] K8s rollback + scale
- [x] Real-time Prometheus metrics
- [x] CI/CD failure detection
- [x] Slack + Email alerting
- [x] PDF incident reports
- [x] Agent self-metrics + Grafana dashboard
- [x] RBAC least-privilege setup
- [x] Unit, integration, and E2E test suites
- [ ] Voice call alerts (Twilio)
- [ ] Docker Compose one-command setup
- [ ] Helm chart packaging
- [ ] GitHub Actions CI/CD pipeline
- [ ] Multi-agent architecture (dedicated Monitor / Diagnose / Fix agents)

---

## 👤 Author

**Uzair Arif** — Final-year BSE student, COMSATS University Islamabad (Wah Campus)
[GitHub: malikuzair22](https://github.com/malikuzair22)