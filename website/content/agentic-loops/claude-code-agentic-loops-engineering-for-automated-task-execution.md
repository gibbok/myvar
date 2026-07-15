+++
title = 'Claude Code Agentic Loops - Engineering for Automated Task Execution'
date = 2026-07-14T14:24:12.458964
draft = false
tags = ['Agentic-loops', 'Claude-Code', 'AI-automation']
description = 'Learn about agentic loops in Claude Code where agents repeat work cycles until a stop condition is met. Covers types, optimization, and progression.'
+++

## Overview

Loop engineering in Claude Code defines agents repeating cycles of work until a specific stop condition is met, advancing processes from manual to automated and proactive. This optimizes agent performance and task execution.

## Key Insights

*   **Agentic Loops Defined:** Agents execute recurring work cycles until a predefined stop condition is met.
*   **Categorization:** Loops are categorized by trigger, stop criteria, Claude Code primitive, and task suitability.
*   **Simplicity First:** Prioritize the simplest viable solution; complex loops are not always necessary.
*   **Code Quality:** Maintain clean codebases, enable agent **self-verification via skills**, and leverage **secondary agents for unbiased code reviews**.
*   **Token Management:** Optimize resource usage through appropriate primitive/model selection, clear exit criteria, piloting large runs, and usage review tools.
*   **Progression:** Evolve from manual turn-based interactions to automated, goal-oriented, time-driven, and proactive event-driven systems.

## Technical Details

### Understanding Agentic Loops

The Claude Code team defines **loops** as agents that repeat work cycles until a stop condition is met. These loops are categorized by their trigger, stop criteria, the specific Claude Code primitive used, and their optimal task type.

### Types of Agentic Loops

#### Turn-Based Loops

Turn-based loops represent the fundamental **agentic loop**, where a user manually directs each step.

*   **Trigger:** User prompt.
*   **Stop Criteria:** Claude judges task completion or requests more context.
*   **Use Cases:** Shorter, exploratory tasks not part of a regular process.
*   **Usage Management:** Write precise prompts and enhance verification with **skills** to minimize turns.
*   **Example:** Claude creates a "like" button. Claude edits code, runs tests, and provides a solution. The user then manually verifies and issues the next prompt. Verification improves by encoding manual steps into a `SKILL.md` file, enabling Claude to perform end-to-end checks. Quantitative checks are most effective for self-verification.

**Example `SKILL.md` for UI verification:**

```
---
name: verify-frontend-change
description: Verify any UI change end-to-end before declaring it done.
---
# Verifying frontend changes
Never report a UI change as complete based on a successful edit alone. Verify it the way a human reviewer would:
1. Start the dev server and open the edited page in the browser.
2. Interact with the change directly. For a new control (button, input, toggle): click it, confirm the expected state change, and screenshot before/after.
3. Check the browser console: zero new errors or warnings.
4. Use the Chrome Devtools MCP, run a performance trace and audit Core Web Vitals.
If any step fails, fix the issue and rerun from step 1 — do not hand back partially verified work.
```

#### Goal-Based Loops (`/goal`)

Goal-based loops extend agent iteration by defining explicit success criteria.

*   **Trigger:** Manual prompt in real-time.
*   **Stop Criteria:** Goal achieved OR maximum number of turns reached.
*   **Use Cases:** Tasks with clearly verifiable exit criteria.
*   **Usage Management:** Set precise completion criteria and explicit turn limits (e.g., "stop after 5 tries").
*   **Mechanism:** An evaluator model checks the defined condition after each attempt, directing the agent back to work until the goal is met or the turn limit is reached. Deterministic criteria (e.g., test pass count, score threshold) are highly effective.
*   **Example:** `/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.`

#### Time-Based Loops (`/loop` and `/schedule`)

Time-based loops automate recurring work or interactions with external systems.

*   **Trigger:** Specified time interval.
*   **Stop Criteria:** User cancellation, or work completion (e.g., PR merges, queue empties).
*   **Use Cases:** Recurring tasks with consistent inputs, or interfacing with external environments (e.g., checking for PR reviews or CI failures).
*   **Usage Management:** Set longer intervals or react based on events rather than fixed times.
*   **Primitives:**
    *   **`/loop`:** Re-runs a prompt on your local machine at an interval. Stops if the computer is turned off.
    *   **`/schedule`:** Moves the loop to the cloud, creating an independently running routine.
*   **Example:** `/loop 5m check my PR, address review comments, and fix failing CI`

#### Proactive Loops

Proactive loops compose multiple primitives to manage long-running, well-defined streams of work without real-time human intervention.

*   **Trigger:** Event or schedule, without real-time human input.
*   **Stop Criteria:** Individual tasks exit upon goal achievement; the overall routine runs until explicitly turned off.
*   **Use Cases:** Recurring, well-defined work streams like bug reports, issue triage, migrations, or dependency upgrades.
*   **Usage Management:** Route routine tasks to smaller, faster models; use the most capable model for critical judgment.
*   **Composition:** Combines `/schedule` (research preview), `/goal`, skills, **dynamic workflows** (research preview), and **auto mode**.
*   **Example:** Handling incoming feedback:
    *   `/schedule every hour: check #project-feedback for bug reports.`
    *   `/goal: don't stop until every report found this run is triaged, actioned, and responded to.`
    *   *When fixing a bug, use a workflow to explore three solutions in parallel worktrees and have a judge adversarially review them.*

### Maintaining Code Quality in Loops

A loop's output effectiveness directly correlates with the surrounding system design.

*   **Clean Codebase:** Claude emulates existing patterns and conventions. A clean codebase promotes high-quality output.
*   **Self-Verification with Skills:** Encode "good enough" criteria into **skills** (`SKILL.md`) for end-to-end work verification.
*   **Accessible Documentation:** Ensure up-to-date framework and library documentation with best practices is readily available.
*   **Second Agent for Code Reviews:** Utilize a separate, unbiased agent (e.g., built-in `/code-review` skill or Code Review for GitHub) for fresh context and bias reduction.
*   **Systemic Improvement:** When results fail to meet standards, encode the fix to improve the system for all future iterations, not just the isolated issue.

### Managing Token Usage

Efficient token usage is critical for cost-effective loop engineering.

*   **Right Primitive and Model:** Match tasks to the simplest appropriate primitive and model. Smaller tasks often use cheaper, faster models without complex agents or loops.
*   **Clear Success and Stop Criteria:** Specific "done" criteria guide Claude to solutions faster, reducing unnecessary iterations.
*   **Pilot Before Large Runs:** For **dynamic workflows** spawning numerous agents, pilot on a smaller subset to gauge token usage before full deployment.
*   **Scripts for Deterministic Work:** Pre-defined scripts are more cost-effective than Claude repeatedly reasoning through deterministic steps.
*   **Appropriate Routine Intervals:** Match loop intervals to the actual frequency of change in the monitored system.
*   **Review Usage:** Utilize commands like `/usage` (for skills, subagents, MCPs), `/goal` (without arguments for turns and token usage), and `/workflows` (for individual agent usage) to monitor and optimize token consumption.

## Getting Started with Loop Design

Identify workflow bottlenecks and automate aspects to begin loop engineering.

| Loop Type    | You Hand Off          | Use It When                             | Claude Code Primitive  |
| :----------- | :-------------------- | :-------------------------------------- | :--------------------- |
| **Turn-based** | The check             | You are exploring or deciding           | Custom verification skills |
| **Goal-based** | The stop condition    | You know what "done" looks like         | `/goal`                |
| **Time-based** | The trigger           | Work happens outside your project on a schedule | `/loop`, `/schedule`   |
| **Proactive**  | The prompt            | Work is recurring and well-defined      | All of the above, and dynamic workflows |

Consider what part of a task can be handed off: can you write the verification check? Is the goal clear? Does the work arrive on a schedule? Formulate a loop idea, execute it, observe behavior, identify stalls or over-reaches, and iterate on its design.

For more information, consult the Claude Code documentation on running agents in parallel, and specific pages for `/loop`, `/schedule`, `/goal`, and **dynamic workflows**.