---
name: prd
description: Create Product Requirements Documents for new projects. Use when starting a new project or feature that needs a spec, implementation plan, and task breakdown. Guides a brainstorm session with the human, then generates spec.md, plan.md, Notion project page, and initial tickets.
---

# PRD — Product Requirements Document

Create structured project documentation following Spec-Driven Development. The PRD lives in the project repo and is mirrored to Notion for visibility.

## Artifacts

### 1. spec.md — What & Why

Lives in the project repo root. Defines the product, not the implementation.

Sections:
- **Project Overview** — What it is, in 2-3 sentences
- **Problem Statement** — What problem it solves
- **Proposed Solution** — How it solves it (approach, not implementation)
- **User Personas** — Who uses it, their goals and context
- **User Stories & Acceptance Criteria** — "As a [user], I want [feature] so that [benefit]" with testable conditions
- **Negative Requirements** — What NOT to do ("Do NOT add auth in this phase", "Do NOT use modals")
- **Design References** — Figma links, look & feel, brand guidelines
- **Success Metrics** — How to measure if it worked

### 2. plan.md — How

Lives in the project repo root. Technical strategy derived from the spec.

Sections:
- **Architecture Overview** — Stack, high-level structure
- **Data Model** — Entities, relationships, schemas
- **API Design / Data Contracts** — Endpoints, interfaces, component communication
- **Design Tokens** — Colors, fonts, spacing (from Figma or brand guidelines)
- **Infrastructure** — Hosting, deploy, CI/CD
- **Technical Constraints** — Limitations, research checklist, unknowns to verify

### 3. Notion Project Page

Mirror of spec + plan for visibility and reporting. Contains:
- Project overview and status
- Links to repo, Figma, deploy
- Embedded or linked spec and plan content
- Project-level metrics (time, tickets, PRs)

### 4. Tickets

Generated from plan.md phases, created in the Notion Tasks database. Follow the Notion skill workflow.

## Workflow

When starting a new project:

1. **Brainstorm with the human** — Use planning mode (one question at a time, planning header). Define scope, problem, solution, personas.
2. **Generate spec.md** — From brainstorm output. Human validates.
3. **Generate plan.md** — From spec. Architecture, data model, API, design tokens. Human validates.
4. **Create Notion project page** — Mirror spec + plan, add links.
5. **Generate tickets** — Break plan into phased tasks in Notion. Group by phase with human checkpoints between phases.
6. **Human checkpoint** — Final validation before implementation begins.

## Brainstorm Guide

When brainstorming a new PRD, follow this sequence:

```
📍 Planning: [Project Name] PRD

1. Problem & solution
2. User personas
3. User stories & acceptance criteria
4. Negative requirements
5. Design references
6. Architecture & stack
7. Data model
8. API / interfaces
9. Infrastructure
10. Phase breakdown & tickets
```

One question per step. Summarize before moving on.

## Sync Rule

When spec.md or plan.md is updated in the repo, update the Notion project page to match. The repo is the source of truth; Notion is the mirror.

## Templates

See `assets/spec-template.md` and `assets/plan-template.md` for ready-to-use templates.
