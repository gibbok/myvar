+++
title = 'Brownfield Agentic Engineering for Legacy Codebases'
date = 2026-09-19T06:44:12.562405
draft = false
tags = ['ai-agents', 'legacy-code', 'software-engineering']
description = 'Deploy autonomous AI agents into legacy codebases safely using strict risk zones and automated verification.'
+++

## Overview

**Brownfield agentic engineering** is the practice of deploying autonomous AI agents into legacy codebases by making implicit constraints explicit, establishing verification harnesses, and managing operational blast radiuses. Implementing AI agents in mature systems requires structured boundaries to ensure that automated code generation remains safe, maintainable, and aligned with system architecture.

## Key Insights

* **Define strict risk zones:** Classify codebases into Green, Yellow, and Red zones based on test coverage, module isolation, and domain sensitivity to regulate agent autonomy.
* **Document implicit context:** Feed agents non-inferrable domain knowledge, historical trade-offs, and unwritten architectural constraints rather than redundant raw code dumps.
* **Require durable research artifacts:** Force agents to output persistent comprehension memos during exploration phases so context survives across session resets.
* **Encode review feedback into the harness:** Convert repeated manual PR corrections into automated linter rules, type definitions, and test assertions.
* **Enforce complete migration units:** Fully deprecate and delete legacy code paths in single operational units to avoid "migration blindness" and contradictory codebase patterns.
* **Parallelize verification before execution:** Scale parallel agent execution only after establishing automated judges, as premature scaling creates severe human code-review bottlenecks.

## Technical Details

### Codebase Risk Segmentation

Legacy repositories rarely contain a complete description of system behavior within the source code. Implicit dependencies, production traffic characteristics, and cross-department expectations exist outside the tree. To safely deploy agents, human engineers must draw strict operational zones:

* **Green Zone (High Autonomy):** Code with comprehensive test coverage, modern conventions, and strict isolation. Agents run in tight, autonomous loops.
* **Yellow Zone (Conditional Autonomy):** Code of mixed quality or partial coverage. Agents may modify code only after generating **characterization tests** that lock current runtime behavior.
* **Red Zone (Restricted Autonomy):** Critical systems (e.g., authentication, billing, permissions, complex orchestration). Agents require direct human pairing or are restricted from making unsupervised changes.

#### Rules for Zone Governance
1. **Humans map the zones:** Agents left to select tasks naturally gravitate toward complex, high-risk files due to descriptive naming patterns.
2. **Zones transition through proof:** A Yellow zone transitions to Green only after characterization tests are committed and reviewed by the module owner.
3. **Zone dictates execution mode:** Green allows unattended execution; Yellow requires tests-first staging; Red requires step-by-step human co-authoring.

```
+-------------------------------------------------------------------+
|                           RISK ZONING                             |
+-----------------+--------------------------------+----------------+
| Zone            | Code Attributes                | Agent Autonomy |
+-----------------+--------------------------------+----------------+
| Green Zone      | Isolated, high test coverage   | Autonomous     |
| Yellow Zone     | Mixed quality, partial tests   | Test-First     |
| Red Zone        | Auth, billing, critical paths  | Human-Paired   |
+-----------------+--------------------------------+----------------+
```

### Context Engineering and Durable Artifacts

Frontier models infer structural code relationships well, making massive prompt context dumps counterproductive. Prompts and instruction files should focus strictly on information that **cannot** be inferred from static analysis:

* Domain-specific business logic and edge-case exceptions.
* Historical architectural trade-offs behind non-intuitive implementations.
* Guidelines not enforced by static analyzers or compilers.

#### Preventing Session Memory Loss
Agent exploration must generate persistent artifacts. Before attempting code modifications in Yellow or Red zones, execute a read-only pass that produces a **comprehension memo** detailing entry points, ownership boundaries, callers, test suites, and open questions. 

When transitioning from research to planning, reset the agent's context window. Use the durable research artifact to establish the plan, confirm invariants, and define a clear rollback strategy before generating code.

```
       +----------------------------------------------------+
       |                1. Research Pass                    |
       |  (Read-only, generates persistent research memo)  |
       +-------------------------+--------------------------+
                                 |
                                 v
       +----------------------------------------------------+
       |                2. Context Reset                    |
       |     (Clears ephemeral chat history/compaction)     |
       +-------------------------+--------------------------+
                                 |
                                 v
       +----------------------------------------------------+
       |                 3. Planning Pass                   |
       |    (Evaluates invariants & rollback strategies)    |
       +-------------------------+--------------------------+
                                 |
                                 v
       +----------------------------------------------------+
       |              4. Execution & Review                 |
       |  (Verifies implementation against acceptance gate) |
       +----------------------------------------------------+
```

### Engineering the Verification Harness

An agentic harness consists of the context, tooling, permissions, test suites, and recovery systems surrounding the model. 

* **Instructions:** Store repository-specific operational facts.
* **Skills:** Encapsulate reusable procedures, such as running schema verification or calculating blast radiuses.
* **Plugins:** Provide governed access to internal APIs, ownership registries, and telemetry dashboards.

Every repeated human code-review correction signifies a defect in the harness. Instead of manually correcting pull requests, convert feedback into **linters, custom hooks, type constraints, or automated test cases**.

### Migration Strategy and Preventing Refactor Blindness

Refactoring brownfield software requires locking current behavior before attempting architectural modifications.

#### Characterization Testing & Traffic Shadowing
**Characterization tests** document existing runtime behavior—including known bugs or legacy quirks that upstream systems depend on. When unit testing legacy surfaces is unfeasible, use **traffic shadowing**: replay production traffic against both legacy and refactored code paths, diffing payload responses to guarantee behavioral equivalence.

#### Eliminating Migration Blindness
Partial migrations introduce conflicting patterns into the codebase, confusing language models during subsequent tasks. 

* **Complete Units:** A migration is incomplete until the new path functions reliably and the legacy code path is fully deleted. 
* **Preventing Blindness:** Automated tests may pass even if a rewritten module silently invokes legacy fallback methods underneath. Audit execution paths to verify that legacy dependencies are entirely detached.
* **Codemod Integration:** Use deterministic codemods for routine mechanical transformations across bulk files; reserve AI agents for handling complex edge cases and exception queues.

### Exploration, Parallel Execution, and Sandboxing

Agents drastically reduce the cost of prototyping multiple architectural solutions simultaneously.

#### Multi-Option Prototyping
Instead of committing to a single migration approach, engineers can prompt agents to implement competing solutions (e.g., ports to different frameworks or languages) in parallel branches. Teams then run the identical test harness and benchmark performance across each generated alternative to make data-driven architectural choices.

#### Managing Review Bottlenecks
Parallelizing agent runs scales code generation but quickly overburdens human review capacity. Automated verification gates must filter generated changes before human intervention. Human review should prioritize high blast-radius zones, invariant modifications, and parity diffs rather than line-by-line syntax checks.

#### Sandbox Security
Standard Git worktrees isolate filesystem state but share local network configurations, credentials, and environment metadata. Unattended agents handling third-party dependencies or untrusted input require **containerized sandboxes** and **scoped credentials** to prevent unintended privilege escalation or system side effects.