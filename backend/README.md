# AccessHire AI - Backend

FastAPI application providing authentication, document processing, and LangGraph multi-agent closed-loop interview orchestration.

## Structure
- `app/core/`: Configuration, database lifecycle, security, and Central Orchestrator
- `app/api/`: REST API route endpoints and auth dependencies
- `app/models/`: MongoDB document models
- `app/schemas/`: Pydantic request, response, and structured state schemas
- `app/agents/`: Modular AI Agents (Resume, Job, Planner, Decision, Question, Evaluation, Feedback, Skill Gap, Roadmap)
- `app/graph/`: LangGraph workflow nodes and state transitions
- `app/services/`: Document extractors (PDF/DOCX) and LLM client factory
- `app/utils/`: Logging and accessibility sanitation utilities

## Running Tests
```bash
$env:PYTHONPATH="backend"
.\backend\.venv\Scripts\pytest backend/tests
```
