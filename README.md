# 🤖 Customer Support LangGraph Agent

A production-style **AI customer-support agent** built with **Python, FastAPI, LangGraph, Google Gemini, RAG, FAISS, SQLite, persistent session memory, dynamic tools, Docker, and Render**.

The system is designed to handle customer-support requests such as:

- 📦 Order-status lookup
- 🚚 Shipment/tracking information
- 💰 Refund information
- 📚 Policy-based questions using RAG
- 💬 Multi-turn conversations using persistent session memory
- 🔄 Response reflection and revision
- ⚡ API-based access through FastAPI
- 📊 Structured request logging
- 🐳 Dockerized deployment
- ☁️ Cloud deployment using Render

> **Note:** The shipping integration currently uses a simulated external shipping API. It is structured so that the simulated implementation can later be replaced by a real carrier/shipping API.

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       Customer      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      /chat          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Persistent Session  │
                         │      Memory         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Planner        │
                         │ Intent / Routing    │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┼──────────────┐
                     │              │              │
                     ▼              ▼              ▼
                  ┌──────┐      ┌──────┐      ┌────────┐
                  │ RAG  │      │ Tool │      │ Writer │
                  └──┬───┘      └──┬───┘      └────┬───┘
                     │             │               │
                     │        ┌────┴─────┐         │
                     │        │          │         │
                     │        ▼          ▼         │
                     │     SQLite   Shipping API   │
                     │        │          │         │
                     │        │      Tracking      │
                     │        │      Information   │
                     │        │                    │
                     └────────┴─────────┬──────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │     Reflect     │
                              │ Quality Check   │
                              └────────┬────────┘
                                       │
                              ┌────────┴────────┐
                              │                 │
                           Revise             End
                              │                 │
                              └────────┬────────┘
                                       ▼
                                   Response
```

---

# ✨ Key Features

## 1. LangGraph Agent Orchestration

The application uses **LangGraph** to model customer-support processing as a stateful workflow rather than a single LLM call.

The workflow contains dedicated nodes for:

- Memory
- Planning
- RAG
- Tool execution
- Response writing
- Reflection
- Revision

This allows the system to route different customer requests through different processing paths.

---

## 2. Persistent Session Memory

The application maintains customer conversation state using persistent SQLite-backed session memory.

A session is identified using:

```text
session_id
```

For example:

```json
{
  "session_id": "customer-001",
  "message": "Where is my order ORD-555?"
}
```

The agent can establish the current order context and use it in a later message:

```text
User:
Where is my order ORD-555?

Agent:
Order ORD-555 is currently Delivered...
```

Then:

```text
User:
What is the estimated delivery date?
```

The second message can use the previously established order context instead of requiring the customer to repeat:

```text
ORD-555
```

This provides a more natural multi-turn customer-support experience.

---

# 🧠 Agent Workflow

The LangGraph workflow follows this general process:

```text
START
  │
  ▼
Memory
  │
  ▼
Planner
  │
  ├──────────────► RAG
  │                 │
  │                 ▼
  │               Tool
  │                 │
  └──────────────► Writer
                    │
                    ▼
                 Reflect
                    │
             ┌──────┴──────┐
             │             │
           Revise         END
             │
             ▼
            END
```

### Memory

Loads previously stored session information.

### Planner

Determines whether the request requires:

- RAG
- A dynamic tool
- Direct response generation

### RAG

Retrieves relevant company-policy information from the FAISS vector store.

### Tool

Executes dynamic operations such as:

- Order lookup
- Refund lookup
- Shipment tracking

### Writer

Uses the available context and tool results to generate the customer-facing response.

### Reflect

Evaluates the generated response.

### Revise

If the response requires improvement, the workflow can revise it before returning the final answer.

---

# 📦 Dynamic SQLite Tools

The project contains a simulated customer database stored in SQLite.

The database contains information such as:

```text
Customers
Orders
Refunds
```

Example order data:

```text
Order ID     Status              Tracking
------------------------------------------------
ORD-111      Out for delivery    TRK-111
ORD-222      Processing          TRK-222
ORD-555      Delivered           TRK-555
```

The agent can dynamically retrieve information instead of relying on information embedded directly inside the prompt.

For example:

```text
User:
Where is my order ORD-555?
```

The system can perform:

```text
User query
    ↓
Planner
    ↓
Tool Node
    ↓
SQLite
    ↓
ORD-555
    ↓
Order information
```

---

# 🚚 Shipping API

The project includes a simulated shipping service located under:

```text
app/shipping/
```

The shipping service exposes a function conceptually similar to:

```python
track_shipment(tracking_number)
```

It returns information such as:

```text
Tracking number
Carrier
Current location
Status
Estimated delivery
Latest tracking event
```

Example:

```text
Tracking number: TRK123456
Carrier: FedEx
Current location: Hyderabad, India
Status: In Transit
Estimated delivery: 2026-08-20
Latest event: Package departed Hyderabad sorting facility
```

### Important architecture detail

The shipping service is intentionally separated from the SQLite order database.

The flow is:

```text
Customer asks about order
        │
        ▼
SQLite order lookup
        │
        ▼
Tracking number
        │
        ▼
Shipping service
        │
        ▼
Latest shipping information
        │
        ▼
LLM response
```

For example:

```text
ORD-555
   │
   ▼
TRK-555
   │
   ▼
Shipping API
   │
   ▼
Carrier / Location / Status / ETA
```

The current implementation is simulated. In a production system, the shipping service could be replaced with an HTTP integration with an actual carrier or shipping aggregator.

---

# 📚 RAG Pipeline

The application also supports retrieval-augmented generation.

The RAG pipeline uses:

```text
Company documents
       │
       ▼
Embeddings
       │
       ▼
FAISS vector index
       │
       ▼
Similarity search
       │
       ▼
Relevant policy context
       │
       ▼
Gemini
       │
       ▼
Answer
```

The project uses:

- Hugging Face embeddings
- FAISS
- LangChain
- Google Gemini

The embedding model currently used is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

FAISS is used to retrieve relevant document chunks before the response is generated.

This allows policy questions to be answered using the application's knowledge base rather than relying entirely on the model's general knowledge.

---

# 🔀 Planner-Based Routing

The planner determines which capabilities are needed for a request.

Conceptually:

```text
                    User Query
                        │
                        ▼
                     Planner
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
        RAG           Tool          Writer
          │             │
          │       ┌─────┴─────┐
          │       │           │
          │     SQLite     Shipping
          │
          └──────────┬──────────┘
                     ▼
                   Writer
```

Examples:

### Order query

```text
"Where is my order ORD-555?"
```

→ Dynamic tool

### Shipping query

```text
"What is the estimated delivery date?"
```

→ Shipping/order tool using session context

### Policy query

```text
"What is your refund policy?"
```

→ RAG

This allows the application to combine deterministic application logic with LLM-based reasoning.

---

# 💬 Example Multi-Turn Conversation

### Request 1

```text
Where is my order ORD-555?
```

The system retrieves:

```text
Order: ORD-555
Status: Delivered
Tracking: TRK-555
```

The tracking number is then passed to the shipping service.

The response can include:

```text
Order ORD-555 is currently Delivered.

Tracking number: TRK-555
Carrier: FedEx
Current location: Hyderabad, India
Status: Delivered
Estimated delivery: 2026-08-16
Latest tracking event: Package was delivered successfully.
```

### Request 2

Using the same session:

```text
What is the estimated delivery date?
```

The system can reuse the session's order context.

This demonstrates persistent multi-turn state.

---

# 🌐 FastAPI

The backend is exposed through FastAPI.

## Available endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/chat` | Main customer-support endpoint |
| POST | `/chat-stream` | Streaming response endpoint |
| GET | `/history/{session_id}` | Retrieve session history |

---

## `/health`

Used by deployment infrastructure and monitoring.

Example:

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

# `/chat`

Main customer-support endpoint.

Example request:

```json
{
  "session_id": "demo-001",
  "message": "Where is my order ORD-555?"
}
```

Example response:

```json
{
  "request_id": "example-request-id",
  "answer": "Order ORD-555 is currently Delivered...",
  "source": "langgraph-agent",
  "latency_ms": 25.65
}
```

The response contains a unique request ID and latency measurement to improve observability.

---

# `/chat-stream`

Provides a streaming-style response.

The endpoint processes the request and streams the generated answer progressively.

This provides a more conversational user experience similar to a typing interface.

---

# `/history/{session_id}`

Retrieves stored conversation history associated with a session.

Example:

```http
GET /history/demo-001
```

This is useful for inspecting persistent conversational state.

---

# 📖 Swagger / OpenAPI

FastAPI automatically generates OpenAPI documentation.

The application therefore provides an interactive API interface through Swagger UI.

When the deployed application is running, the API documentation is available through:

```text
/docs
```

The raw OpenAPI specification is available through:

```text
/openapi.json
```

Swagger UI makes it possible to:

- Inspect endpoints
- View request schemas
- View response schemas
- Enter request data
- Execute API requests
- Inspect responses

This is particularly useful during development and deployment testing.

---

# 📊 Structured Logging

The application includes structured application-level logging.

Example log information:

```text
Request received
Session state loaded
User message saved
LangGraph execution started
LangGraph execution completed
Session state updated
Request completed
```

Requests include information such as:

```text
request_id
session_id
latency_ms
```

This makes it easier to trace an individual request through the application.

Example:

```text
Request received |
request_id=... |
session_id=render-shipping-test-002
```

followed by:

```text
LangGraph execution started
```

and:

```text
Request completed |
request_id=... |
latency_ms=31.92
```

This provides basic production-style observability.

---

# 🐳 Docker

The application is containerized using Docker.

The Docker image:

1. Starts from Python
2. Sets the application working directory
3. Installs the Docker-specific dependencies
4. Copies application code
5. Copies runtime data
6. Exposes the application port
7. Starts FastAPI using Uvicorn

Conceptually:

```text
Docker Image
    │
    ├── Python runtime
    ├── Dependencies
    ├── FastAPI application
    ├── Models
    ├── Prompts
    ├── FAISS index
    └── Database
          │
          ▼
       Uvicorn
          │
          ▼
       FastAPI
```

---

# ☁️ Render Deployment

The application is deployed as a web service on Render.

Deployment flow:

```text
GitHub
   │
   ▼
Render
   │
   ▼
Docker Build
   │
   ▼
Container
   │
   ▼
FastAPI + Uvicorn
   │
   ▼
Public API
```

The application exposes a health endpoint that Render can use to verify that the service is running.

Production testing includes:

```text
/health
/chat
```

and the application logs can be inspected through Render's service logs.

---

# 🔐 Environment Variables

Sensitive credentials should not be committed to GitHub.

The application uses environment variables for configuration such as the Google API key.

Example:

```text
GOOGLE_API_KEY=<your-api-key>
```

Create a local `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

Do **not** commit `.env`.

The `.env` file should be included in `.gitignore`.

For Render, the API key should be configured using the service's environment-variable settings rather than hardcoded into the source code.

---

# 🗂️ Project Structure

A simplified project structure:

```text
Customer_Support_end_to_end/
│
├── app/
│   ├── api.py
│   │
│   ├── graph/
│   │   ├── final_state.py
│   │   ├── final_nodes.py
│   │   ├── final_workflow.py
│   │   └── db_tools.py
│   │
│   ├── memory/
│   │   ├── memory_store.py
│   │   └── session_memory.py
│   │
│   └── shipping/
│       └── shipping_api.py
│
├── data/
│   └── ...
│
├── models/
│   └── ...
│
├── prompts/
│   └── ...
│
├── faiss_index/
│   └── ...
│
├── database/
│   └── support.db
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── requirements.docker.txt
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangGraph | Agent orchestration |
| LangChain | LLM/RAG integration |
| Google Gemini | Language model |
| FastAPI | Backend API |
| Pydantic | Request/response validation |
| SQLite | Customer/order/refund data |
| FAISS | Vector similarity search |
| Sentence Transformers | Embeddings |
| Hugging Face | Embedding/model ecosystem |
| Docker | Containerization |
| Render | Cloud deployment |
| Uvicorn | ASGI application server |

---

# 🧪 Testing

The system has been tested across multiple layers.

## Database tools

Order lookup:

```text
ORD-111
ORD-222
ORD-555
```

Refund lookup:

```text
Valid refund
Missing refund
```

## Shipping API

Valid tracking:

```text
TRK123456
TRK987654
```

Invalid tracking numbers return an explicit failure response rather than silently producing fabricated tracking information.

## Agent

Tested customer-support requests including:

```text
Where is my order?
What is my order status?
What is my refund status?
What is the refund amount?
What is the refund policy?
Where is my package?
What is the estimated delivery date?
```

## Session memory

Tested multi-turn conversations using the same `session_id`.

## API

Tested:

```text
GET /health
POST /chat
POST /chat-stream
GET /history/{session_id}
```

## Deployment

The application has been deployed and tested on Render.

---

# 🚀 Running Locally

## 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Customer_Support_end_to_end
```

## 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

For the Docker-specific dependency set:

```powershell
pip install -r requirements.docker.txt
```

## 4. Configure environment variables

Create:

```text
.env
```

Add:

```env
GOOGLE_API_KEY=your_api_key_here
```

## 5. Start the API

```powershell
uvicorn app.api:app --reload
```

The API will be available locally through:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

---

# 🐳 Running with Docker

Build the image:

```powershell
docker build -t customer-support-agent .
```

Run:

```powershell
docker run --rm -p 8000:8000 --env-file .env customer-support-agent
```

Then open:

```text
http://localhost:8000/docs
```

---

# 🔄 End-to-End Request Example

Consider:

```text
Where is my order ORD-555?
```

The complete system flow is:

```text
1. FastAPI receives request
          ↓
2. Session memory loads existing state
          ↓
3. User message is saved
          ↓
4. LangGraph starts
          ↓
5. Memory node identifies ORD-555
          ↓
6. Planner determines a tool is required
          ↓
7. SQLite order tool retrieves ORD-555
          ↓
8. Tracking number TRK-555 is obtained
          ↓
9. Shipping service is queried
          ↓
10. Shipping information is added to state
          ↓
11. Writer generates customer response
          ↓
12. Reflection checks response
          ↓
13. Session state is updated
          ↓
14. Assistant response is saved
          ↓
15. FastAPI returns response
```

This demonstrates the project's main architectural idea:

> **LLM reasoning is combined with deterministic application tools and persistent state rather than relying on the LLM alone.**

---

# 🎯 Design Philosophy

The project intentionally separates responsibilities.

### LLM

Used for:

- Understanding natural-language requests
- Planning
- Generating responses
- Reflection/revision

### Application logic

Used for:

- Database queries
- Order lookup
- Refund lookup
- Tracking lookup
- Session persistence
- API handling
- Logging

This separation reduces the need for the LLM to invent factual customer/order information.

For example, the LLM should not invent:

```text
Order status
Refund amount
Tracking number
```

Instead, those values should come from application tools.

---

# ⚠️ Current Limitations

This project is designed as a production-style portfolio project, but it is not a complete enterprise customer-support platform.

Current limitations include:

- Shipping API is simulated rather than connected to a real carrier.
- SQLite is used instead of a production relational database.
- The planner uses application-level routing logic.
- Authentication and authorization are not implemented.
- Rate limiting is not implemented.
- The shipping dataset is static.
- The system does not actually place orders.
- The system does not actually cancel customer orders unless a dedicated transactional cancellation tool is implemented.
- Production-scale distributed state management is outside the current scope.

These limitations are intentional opportunities for future development.

---

# 🔮 Future Improvements

Potential extensions include:

### 1. Real Shipping API

Replace the simulated service with an actual HTTP integration such as:

```text
Carrier API
     ↓
Shipping Service Adapter
     ↓
LangGraph Tool
```

### 2. Real Production Database

Replace SQLite with:

```text
PostgreSQL
```

for a production-scale deployment.

### 3. Order Modification Tools

Add transactional tools for:

```text
Cancel order
Change shipping address
Request refund
Create return
Modify order
```

These should use explicit business rules and authorization rather than allowing the LLM to directly modify database records.

### 4. Authentication

Add:

```text
User authentication
JWT/session authorization
Customer identity verification
```

### 5. MCP

Expose customer-support tools through the Model Context Protocol.

Potential MCP tools:

```text
get_order
get_refund
track_shipment
get_policy
```

### 6. Better Observability

Potential additions:

```text
OpenTelemetry
Metrics
Distributed tracing
Error monitoring
Dashboarding
```

---

# 💡 What This Project Demonstrates

This project demonstrates experience with:

- Agentic workflow design
- LangGraph state machines
- LLM application development
- Tool-based agent architecture
- Retrieval-augmented generation
- Vector databases
- Persistent conversational memory
- Structured outputs
- FastAPI backend development
- API design
- SQLite data access
- External API abstraction
- Docker containerization
- Cloud deployment
- Structured logging
- Production-oriented debugging

---

# 📌 Resume Summary

**AI Customer Support Agent — LangGraph, Gemini, FastAPI, RAG, Docker**

Built and deployed a stateful AI customer-support agent using LangGraph and Google Gemini, combining planner-based routing, persistent session memory, FAISS-based RAG, SQLite tools, and a simulated external shipping API. Developed a FastAPI backend with structured logging, health monitoring, streaming responses, and Docker-based deployment on Render.

---

# 👩‍💻 Author

**Sai Deepika**

Built as an end-to-end AI/LLM engineering project demonstrating agent orchestration, retrieval, tool calling, persistent state, API development, and cloud deployment.

---

## ⭐ Project Highlights

```text
LangGraph Agent
      +
Persistent Memory
      +
RAG / FAISS
      +
SQLite Dynamic Tools
      +
Shipping API
      +
Gemini
      +
FastAPI
      +
Structured Logging
      +
Docker
      +
Render
      =
End-to-End AI Customer Support System
```