# Slipstream System Architecture

This document provides a high-level overview of the architecture, workflow orchestration model, access control system, and AI integration patterns used in the Slipstream onboarding platform.

The system was designed as a multi-tenant onboarding platform that combines workflow automation, role-based coordination, and AI-assisted onboarding experiences.

---

# Architecture Overview

The platform is built around four primary architectural layers:

1. Frontend Dashboard Layer  
2. Workflow Orchestration Layer  
3. AI Agent Interaction Layer  
4. Backend Infrastructure Layer  

```text
                    ┌────────────────────┐
                    │  Admin Dashboard   │
                    └────────────────────┘
                              │
                              │
┌────────────────────┐        │        ┌────────────────────┐
│ Employee Dashboard │────Workflow────│ Stakeholder Portal │
└────────────────────┘      Engine    └────────────────────┘
                              │
                              │
                    ┌────────────────────┐
                    │ Supabase Backend   │
                    └────────────────────┘
```

The onboarding system coordinates onboarding workflows across employees, HR/admins, stakeholders, and platform administrators.

---

# Frontend Dashboard Layer

The frontend layer is built with Next.js, React, and TypeScript and provides separate onboarding experiences depending on user access group.

## Employee Dashboard

The employee-facing experience combines:

- AI-guided onboarding chat
- Task progression tracking
- Workflow completion visibility
- Document access
- Escalation support
- Real-time onboarding updates

The employee dashboard focuses on onboarding execution and guided task completion.

---

## HR/Admin Dashboard

The HR dashboard supports onboarding operations including:

- Workflow assignment
- Employee onboarding management
- Task library management
- Workflow template creation
- Analytics dashboards
- Audit log visibility
- Document and form management

The HR dashboard is designed around onboarding coordination and operational visibility.

---

## Stakeholder Dashboard

Stakeholders such as managers, IT, finance, legal, and hiring managers interact through a simplified dashboard focused on:

- Assigned onboarding steps
- Action-item completion
- Workflow visibility for assigned employees

---

## Platform Admin Dashboard

Platform administrators have access to cross-company operational tooling including:

- Multi-company management
- Platform analytics
- Company snapshots
- Administrative controls
- User management

---

# Workflow Orchestration Layer

The core onboarding engine is built around reusable workflow templates and task sequencing logic.

The workflow hierarchy follows the structure:

```text
Workflow → Tasks → Steps
```

Each workflow may contain multiple tasks, and each task may contain multiple ordered onboarding steps.

---

## Workflow Assignment Lifecycle

When an HR/Admin assigns a workflow to an employee, the system performs a multi-step orchestration process:

1. Authenticates the requesting user
2. Verifies workflow assignment permissions
3. Validates company-scoped access
4. Prevents duplicate workflow assignments
5. Creates workflow assignment records
6. Materializes workflow tasks into employee-specific task instances
7. Materializes onboarding steps into employee-specific step instances
8. Calculates due dates using employee start dates
9. Writes onboarding audit log events

This architecture separates reusable workflow templates from employee-specific onboarding execution records.

---

## Task Dependency and Sequencing Logic

The onboarding system supports both explicit and inferred task dependencies.

Tasks can:

- Explicitly depend on other tasks
- Automatically inherit sequential dependencies through task ordering
- Be blocked until prerequisite tasks are completed

The sequencing engine builds dependency maps across workflows and determines onboarding availability based on completion state.

A task is considered blocked until all prerequisite tasks are marked as:

- completed
- skipped

The platform also supports sequential onboarding steps inside a task.

If the next incomplete step belongs to another stakeholder, the employee dashboard displays a waiting state indicating that onboarding progression is blocked pending another user’s action.

---

## Escalation and Coordination

The onboarding system supports escalation flows for blocked onboarding steps and incomplete onboarding actions.

Escalation logic allows onboarding issues to be surfaced to:

- HR/Admin users
- Assigned stakeholders
- Relevant user groups

This helps support cross-functional onboarding coordination across departments.

---

# Access Control and Permission Model

The platform uses a centralized role-based access and permission system.

The onboarding platform separates:

- Access Groups
- Department-Specific Roles
- System Groups
- Action-Level Permissions

---

## Access Groups

The system defines four primary access groups:

| Access Group | Purpose |
|---|---|
| Employee | Employee onboarding experience |
| Manager | Stakeholder onboarding participation |
| Admin | Company-scoped onboarding administration |
| Super_Admin | Platform-level administration |

---

## Department-Specific Roles

Department-specific onboarding roles include:

- HR
- IT
- Legal
- Finance
- Hiring Manager

These roles are mapped into broader access groups to simplify permission routing while still supporting department-specific onboarding responsibilities.

---

## Permission Model

Permissions are defined at the action level.

Examples include:

- Workflow assignment
- Employee management
- Analytics visibility
- Audit log access
- Workflow management
- Form management
- Knowledge management

This design allows onboarding functionality to be scoped independently from organizational department naming.

---

## Group-Based Step Assignment

Onboarding steps can be assigned:

- Directly to users
- To onboarding stakeholder groups

User group membership is fetched dynamically from Supabase and used to determine which onboarding action items should appear for each stakeholder.

This design supports scalable onboarding coordination across multiple departments and onboarding participants.

---

# AI Agent Interaction Layer

The employee-facing onboarding assistant communicates with the AI backend through secure server-side proxy routes.

The proxy layer:

- Authenticates users through Supabase Auth
- Overrides client-provided user identifiers with authenticated IDs
- Updates onboarding chat session metadata
- Securely forwards requests to the AI backend
- Streams responses back through Server-Sent Events (SSE)

This architecture allows the onboarding assistant to support real-time conversational onboarding experiences while keeping API credentials server-side.

---

## Streaming Chat Architecture

The onboarding assistant uses SSE streaming to provide:

- Real-time onboarding responses
- Interactive onboarding guidance
- Incremental AI-generated onboarding instructions
- Persistent onboarding sessions

Chat sessions are tracked through a dedicated session metadata table.

---

# Backend Infrastructure Layer

The backend infrastructure is built on Supabase and PostgreSQL.

The platform uses Supabase for:

- Authentication
- PostgreSQL storage
- Real-time subscriptions
- File storage
- Audit logging
- User and workflow management

---

## Real-Time Synchronization

The platform uses Supabase real-time subscriptions to synchronize onboarding state changes including:

- Task status updates
- Workflow progression
- Dashboard refreshes
- Onboarding completion tracking

---

# Multi-Tenant Architecture

The onboarding platform is designed as a multi-tenant SaaS system.

Company data is scoped by company identifiers and validated throughout onboarding operations.

Examples include:

- Workflow assignment validation
- Company-specific workflow access
- Group membership filtering
- Dashboard scoping
- Audit logging

This architecture helps isolate onboarding operations across organizations while supporting centralized platform administration.

---

# Design Goals

The onboarding platform was designed around several operational goals:

- Standardized onboarding workflows
- Reusable onboarding templates
- Cross-functional onboarding coordination
- Real-time onboarding visibility
- AI-assisted onboarding guidance
- Role-scoped onboarding access
- Enterprise onboarding scalability
- Operational auditability

---

# Technical Stack

| Layer | Technologies |
|---|---|
| Frontend | Next.js, React, TypeScript |
| Styling | Tailwind CSS, shadcn/ui |
| Backend Services | Supabase |
| Database | PostgreSQL |
| Authentication | Supabase Auth |
| Real-Time | Supabase Realtime |
| AI Integration | SSE-based agent communication |
| Deployment | Vercel |

---

# Notes

This document describes a sanitized portfolio version of the system architecture. Sensitive production infrastructure details, credentials, internal business logic, and proprietary implementation details have been intentionally omitted or generalized.
