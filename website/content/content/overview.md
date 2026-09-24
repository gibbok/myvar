+++
title = 'Codex Best Practices'
date = 2026-09-23T16:24:37.879337
draft = false
tags = ['codex','ai']
description = 'No description.'
+++

## Overview
Codex functions most effectively when managed as a persistent, configurable teammate across CLI, IDE extensions, and the ChatGPT desktop application. Transitioning from one-off prompts to structured workflows—using contextual files, configuration files, external integrations, custom skills, and scheduled tasks—significantly improves code quality and execution reliability.

## Key Insights
* **Structured Context**: Optimize prompts by explicitly defining the Goal, Context, Constraints, and Completion Criteria ("Done when").
* **Durable Guidance**: Eliminate repetitive instructions by encoding repo-specific standards, build commands, and constraints into `AGENTS.md` files.
* **Layered Configuration**: Set persistent execution defaults, sandbox boundaries, and tool connections using `config.toml` across global, repository, and profile scopes.
* **Extensible Tooling**: Connect external datasets and third-party systems via Model Context Protocol (MCP) servers instead of pasting live data into chats.
* **Modular Automation**: Encapsulate stable, multi-step workflows into `SKILL.md` files and run predictable routines automatically using scheduled tasks in isolated Git worktrees.
* **Context Hygiene**: Maintain chat focus by limiting each thread to a single coherent outcome, leveraging subagents for isolated subtasks, and using `/fork` or `/compact` to prevent performance degradation.

## Technical Details

### Context and Prompt Construction
Providing precise context and clear boundary conditions improves output consistency, especially in large codebases.

Prompts should routinely incorporate four structural components:
* **Goal**: The precise change, feature, or bug fix required.
* **Context**: Explicit references to relevant files, directories, documentation, or error outputs (utilizing `@` file references).
* **Constraints**: Architectural guidelines, linter specs, type requirements, and safety boundaries.
* **Done when**: Unambiguous verification criteria, such as passing test suites or verified runtime behavior.

Adjust model reasoning effort based on task complexity:
* **Low**: Fast execution for narrow, well-defined tasks (e.g., GPT-6 Astra defaults).
* **Medium / High**: Recommended default for complex logic changes, refactoring, and debugging (e.g., GPT-6 Sol, GPT-6 Luna).
* **Extra High**: In-depth reasoning for extended, agentic, multi-file architectural changes.

### Architectural Planning Strategy
For complex or ambiguous tasks, generate an explicit execution plan before generating code.

* **Plan Mode**: Toggle via `/plan` or `Shift+Tab` to allow Codex to inspect the repository, clarify requirements, and outline implementation steps prior to writing code.
* **Interactive Interview**: Prompt Codex to question assumptions and refine vague specifications into concrete requirements before implementation.
* **Execution Templates**: Standardize multi-step initiatives by configuring Codex to execute against structured `PLANS.md` templates.

### Reusable Instructions via AGENTS.md
`AGENTS.md` acts as an automatically loaded contextual manual for coding agents operating within a repository.

#### Included Elements
* Repository layout and key path locations.
* Project boot procedures, build steps, test suites, and linter commands.
* Coding standards, style guides, and PR requirements.
* Strict constraints and prohibited patterns.
* Verification criteria for completed work.

#### Precedence Hierarchy
Codex evaluates guidance files based on proximity to the working directory:
1. **Directory-Specific**: `./subfolder/AGENTS.md` (overrides higher levels).
2. **Repository-Level**: `./.codex/AGENTS.md` or `./AGENTS.md`.
3. **Global Defaults**: `~/.codex/AGENTS.md`.

*Note: Use the `/init` CLI command to generate a baseline `AGENTS.md` file, then customize it based on recurring session retrospectives.*

### Consistent Environment Configuration
Configuration files establish system defaults across CLI, IDE extensions, and the ChatGPT desktop application.

* **Global Preferences**: `~/.codex/config.toml` (or **Settings > Configuration** in the desktop app).
* **Repository Preferences**: `.codex/config.toml`.
* **Profile Overrides**: `$CODEX_HOME/profile-name.config.toml`.

```toml
# Example config.toml structure
model = "gpt-6-luna"
reasoning_effort = "high"

[sandbox]
mode = "workspace-only"
approval_policy = "on-request"
```

#### Sandboxing and Approvals
* **Approval Mode**: Controls when Codex requests execution permission for system commands.
* **Sandbox Mode**: Restricts file read/write access and directory access limits. Start with restrictive permissions and relax them only as workflow needs dictate.

### Continuous Testing, Verification, and Code Review
Incorporate automated checking loops into prompts or `AGENTS.md` guidelines to ensure code quality before acceptance.

#### Review Execution Options
* **Local Diff Inspection**: Review live diffs within the ChatGPT desktop app diff panel; comment on specific lines to feed feedback back into the context.
* **Command-Line Code Review**: Use `/review` to evaluate code against a base branch, inspect uncommitted local changes, analyze specific commits, or run custom review scripts.
* **CI/CD Integration**: Integrate GitHub Cloud review automation to trigger automated pull request analysis directly or via `@Codex` mentions.

### External System Integration with MCP
Model Context Protocol (MCP) connects Codex to external services, databases, and APIs without requiring manual data copying.

* **Supported Server Types**: STDIO and Streamable HTTP with OAuth capabilities.
* **CLI Management**: Add servers using `codex mcp add <name> <url>` or configure them directly via **Settings > MCP Servers**.
* **Best Practice**: Integrate MCP tools selectively to replace high-friction manual data fetching workflows.

### Modular Workflows with Skills
Packaging repetitive tasks into reusable skills ensures standardized execution across teams.

* **Structure**: Defined in `SKILL.md` files containing instructions, trigger phrases, inputs, outputs, and optional supporting scripts.
* **Personal Skills**: Stored in `$HOME/.agents/skills`.
* **Shared Team Skills**: Committed directly to `.agents/skills` within the target repository.
* **Creation**: Use the `$skill-creator` system skill to scaffold new definitions.

```markdown
<!-- Example SKILL.md layout -->
---
name: log-triage
description: Parse and summarize recent error logs from staging builds.
triggers:
  - "triage logs"
  - "analyze staging error"
---
# Instructions
1. Fetch latest log output.
2. Filter for stack traces and high-severity errors.
3. Cross-reference errors with recently modified files.
```

### Automation via Scheduled Tasks
Execute predictable, background maintenance routines directly inside dedicated Git worktrees using the ChatGPT desktop application.

* **Typical Use Cases**: Commit summaries, bug scanning, release note generation, CI failure analysis, and dependency audits.
* **Core Rule**: *Skills define the operational method; scheduled tasks define the execution cadence.* Standardize a workflow as a skill before scheduling it.

### Thread and Context Management
Long-running sessions accumulate stale reasoning, increasing latency and reducing output quality.

* **Scope Limits**: Dedicate one chat session to a single coherent unit of work.
* **Subagent Offloading**: Delegate localized tasks (e.g., test creation, log analysis, parameter research) to subagents to preserve main thread context.
* **Useful Slash Commands**:
  * `/fork`: Branch the current session into a new thread while retaining the context history.
  * `/compact`: Compress earlier transcript context manually (also occurs automatically).
  * `/resume`: Restore a saved local session.
  * `/agent`: Switch active focus between parallel agent threads.
  * `/status`: Inspect active context and session parameters.

### Common Pitfalls to Avoid
* **Overloaded Prompts**: Placing static system rules in every prompt instead of delegating them to `AGENTS.md` or a `SKILL.md`.
* **Hidden Build Context**: Omitting clear command paths for building and testing, preventing Codex from self-correcting errors.
* **Unscoped System Access**: Granting broad execution permissions without sandbox boundaries on untrusted repos.
* **In-Place Concurrent Edits**: Running live automated tasks on active working files without leveraging isolated Git worktrees.
* **Premature Automation**: Scheduling recurring tasks before validating the underlying workflow manually.
* **Monolithic Chat Sessions**: Reusing a single chat thread across multiple unrelated tasks, leading to bloated context windows and high error rates.
