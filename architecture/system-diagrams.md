# System Architecture Diagrams

This file contains simplified system diagrams for the AI Onboarding Workflow System.

---

# High-Level System Architecture

```mermaid
flowchart TD
    Employee[Employee Dashboard] --> Frontend[Next.js Frontend]
    HR[HR / Admin Dashboard] --> Frontend
    Manager[Stakeholder / Manager Dashboard] --> Frontend
    SuperAdmin[Platform Admin Dashboard] --> Frontend

    Frontend --> APIRoutes[Next.js API Routes]
    APIRoutes --> Supabase[Supabase Backend]
    APIRoutes --> Agent[AI Agent Backend]

    Supabase --> Auth[Authentication]
    Supabase --> DB[(PostgreSQL Database)]
    Supabase --> Storage[Document Storage]
    Supabase --> Realtime[Realtime Updates]

    Agent --> SSE[Streaming Responses via SSE]
    SSE --> Frontend
```

---

# Workflow Assignment Flow

```mermaid
flowchart TD
    HR[HR / Admin assigns workflow] --> Auth[Authenticate user]
    Auth --> Permission[Check assign_workflows permission]
    Permission --> CompanyCheck[Validate employee and workflow belong to same company]
    CompanyCheck --> DuplicateCheck[Check duplicate assignment]
    DuplicateCheck --> UserWorkflow[Create user_workflow record]
    UserWorkflow --> UserTasks[Generate user_tasks from workflow template]
    UserTasks --> UserSteps[Generate user_task_steps from task template]
    UserSteps --> DueDates[Calculate due dates from employee start date]
    DueDates --> Audit[Write audit log]
    Audit --> Dashboard[Update workflow status dashboards]
```

---

# Workflow Sequencing Logic

```mermaid
flowchart TD
    Workflow[Workflow Template] --> Tasks[Ordered Tasks]
    Tasks --> Dependencies[Dependency Map]

    Dependencies --> Check{Are prerequisites complete?}

    Check -->|Yes| Available[Task becomes available]
    Check -->|No| Blocked[Task remains blocked]

    Blocked --> Waiting[Show waiting / blocked state]
    Available --> StepCheck{Next step owner?}

    StepCheck -->|Employee| EmployeeAction[Employee completes step]
    StepCheck -->|Stakeholder| StakeholderAction[Wait for stakeholder action]

    EmployeeAction --> Progress[Update workflow progress]
    StakeholderAction --> Progress
```

---

# Role-Based Access Model

```mermaid
flowchart TD
    User[User] --> AccessGroup{Access Group}

    AccessGroup --> Employee[Employee]
    AccessGroup --> Manager[Manager / Stakeholder]
    AccessGroup --> Admin[HR / Admin]
    AccessGroup --> SuperAdmin[Super Admin]

    Employee --> EmployeePerms[Own tasks and onboarding chat]
    Manager --> ManagerPerms[Assigned workflows and action items]
    Admin --> AdminPerms[Workflow, employee, task, form, analytics management]
    SuperAdmin --> SuperPerms[Platform-level company and user management]
```

---

# Agent Streaming Flow

```mermaid
flowchart TD
    Employee[Employee sends message] --> Frontend[Chat UI]
    Frontend --> Proxy[Next.js API Proxy]

    Proxy --> Auth[Supabase Auth Check]
    Auth --> SafeUser[Replace client userId with authenticated userId]
    SafeUser --> Session[Update chat session metadata]
    Session --> AgentBackend[AI Agent Backend]
    AgentBackend --> SSE[Server-Sent Events Stream]
    SSE --> Frontend
    Frontend --> EmployeeResponse[Real-time assistant response]
```

---

# Data Flow Overview

```mermaid
flowchart LR
    HR[HR/Admin] --> WorkflowTemplate[Workflow Template]
    WorkflowTemplate --> Assignment[Workflow Assignment]
    Assignment --> UserWorkflow[User Workflow]
    UserWorkflow --> UserTasks[User Tasks]
    UserTasks --> UserSteps[User Task Steps]

    UserSteps --> Status[Task Status Updates]
    Status --> Analytics[Analytics Dashboard]
    Status --> EmployeeView[Employee Task View]
    Status --> AdminView[HR/Admin Status View]
```
