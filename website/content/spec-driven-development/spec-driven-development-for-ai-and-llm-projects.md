+++
title = 'Spec-driven Development for AI and LLM Projects'
date = 2026-07-27T07:03:10.705008
draft = false
tags = ['spec-driven-dev', 'AI-LLM', 'software-methodology']
description = 'Spec-driven development prioritizes a comprehensive specification before AI implementation. It reduces costs AI hallucination and enhances collaboration.'
+++

## Overview

Spec-driven development is a software construction methodology prioritizing a comprehensive specification before AI implementation. This approach ensures clarity, reduces ambiguity, and optimizes Large Language Model (LLM) use throughout the development lifecycle.

## Key Insights

*   **Cost Efficiency:** A well-defined specification enables the use of lower-tier LLMs, significantly reducing token costs without compromising output quality due to clear instructions.
*   **Reduced AI Hallucination:** Providing a clear spec and reference implementations minimizes LLM "guessing" and hallucination, leading to more accurate and predictable code generation.
*   **Proactive Decision-Making:** The process forces upfront architectural and design decisions, preventing costly "on-the-fly" adjustments during implementation.
*   **Enhanced Collaboration:** Early spec review, as practiced by teams like OpenAI Codex, allows engineers to identify issues and refine the design before coding begins.
*   **Scalability for Complex Projects:** Spec-driven development is particularly beneficial for larger, more complex projects where technical uncertainties are high, saving significant time on rework.

## Technical Details

### The Spec-Driven Development Workflow

The following six-step workflow, as practiced by Larridin, details a structured approach to spec-driven development with AI.

#### 1. Start with a Spike

Before committing to a full specification, conduct a **spike** to resolve significant technical unknowns or "risky" elements of a project.

*   **Purpose:** Prove core concepts or critical paths work. It is not an MVP; it is throwaway-quality work focused solely on answering "does this actually work?"
*   **Goal:** Eliminate technical uncertainty that could otherwise contaminate the spec with multiple options.
*   **Examples:**
    *   Spike critical API edge cases.
    *   Measure the performance of an API's hot path.
    *   Verify an API's ability to return data fast enough for a high-record view.
    *   **Real-world example:** Proving the core logic for an "AI Fluency" measurement model to ensure it works and is token-efficient before designing the surrounding infrastructure (queue, monitoring, database).
*   **Focus:** Stop when the question is answered. Avoid spending time on implementation details like variable naming or file structure.

#### 2. Promote the Spike to Reference Implementation

Once a spike successfully proves a concept, do not discard it. It becomes a **reference implementation**.

*   **Value:** A working example provides concrete evidence to LLMs, guiding their understanding and preventing hallucination.
*   **Location:** Store reference implementations in a known repository location, such as `spec/spikes/reference/referenceName`.
*   **Documentation:** **Comment thoroughly** on the specific parts that prove the approach. Crucially, also comment on shortcuts, missing error handling, or areas where the implementation is not production-ready. More context leads to more accurate LLM output.
*   **Risk:** An uncommented spike can lead LLMs to reproduce flawed parts alongside correct ones.

#### 3. Write the Specification

With technical uncertainties addressed and reference implementations established, create the project specification. This document should be sufficiently detailed for a junior engineer or a small LLM to understand and implement.

*   **AI Assistance:** Utilize higher-tier LLMs to assist in writing the spec. Instruct the AI to:
    *   Restate the required tasks.
    *   List all assumptions.
    *   Flag any ambiguities.
*   **Refinement:** Address any unhandled assumptions or ambiguities by either creating new spikes or updating existing ones.
*   **Desired Spec Structure:**
    *   **Problem Statement:** A concise paragraph defining what is being solved and for whom.
    *   **Non-goals:** Explicitly state what the system will *not* do to prevent over-engineering.
    *   **Assumptions:** Document all pre-decided details (e.g., pagination type, lazy loading) to prevent LLMs from silently making choices.
    *   **Reference Implementation:** Link to the spike, highlighting proven parts versus shortcuts or missing elements.
    *   **Architecture:** Outline the data model, module boundaries, interfaces, and error handling.
    *   **Test Plan:** Detail unit, integration, and end-to-end tests required.
*   **Recommendation:** Write the **smallest spec that unambiguously specifies the system**. Remove fluff. Document even "obvious" decisions, as "obvious to you" is not "obvious to the model."

#### 4. Write/Adjust the Test Plan Before Implementation

Integrate test-driven development principles by defining the **test plan** as part of the spec, *before* the implementation plan.

*   **Timing:** The test plan should be defined once the system's functionality is clear.
*   **Clarity:** Ensure the test plan uses clear bullet points or distinct separations between tests.
*   **Specificity:** Avoid ambiguous tests.
    *   **Instead of:** "Handles large inputs gracefully"
    *   **Use:** "Processes 10k rows in under 2 seconds with memory under 500MB."
    *   **Instead of:** "Fails safely on bad input"
    *   **Use:** "Returns a 400 with a specific error code when the payload is missing the `customer_id` field."
*   **Definition of Done:** The detailed list of named tests, inputs, and expected outputs serves as the clear **definition of done** against which the implementation will be measured.

#### 5. Create the Implementation Plan

With the reference implementation, spec, and test plan complete, generate a highly detailed **implementation plan**.

*   **Detail Level:** This plan outlines a precise sequence of steps, file by file and function by function, leaving no room for LLMs to deviate. It is significantly more detailed than the spec (e.g., 3k lines for implementation plan vs. 800 lines for spec).
*   **AI Generation:** Use an LLM to generate the implementation plan based on the completed spec. Store these plans in a dedicated repository folder (e.g., `plans`).
*   **Review:** Conduct a detailed review of the generated plan.
*   **Critical Rule:** If the implementation plan introduces new architectural decisions, it signals an incomplete spec. **Go back and update the spec first.** Do not manually update the implementation plan with new architectural details without updating the foundational spec. All critical decisions must be finalized during the spec phase.

#### 6. Implement

The implementation phase becomes straightforward once the detailed plan is approved.

*   **Execution:** Instruct a smaller, cost-effective LLM (e.g., Haiku) to generate code based directly on the implementation plan.
*   **Pull Requests (PRs):** Decide on the PR strategy: create them manually, split the project into multiple LLM-generated PRs, or have the LLM adhere to specific PR conventions.

### When to Use Spec-Driven Development (and When Not To)

Spec-driven development is a powerful methodology, but its application should be strategic.

#### Recommended Use Cases

*   **Large, Complex Projects:** Ideal for projects with significant scope, multiple components, or high technical uncertainty. It prevents extensive rework of poorly generated AI code.
*   **Architectural Decisions:** Essential when making important architectural choices, as the spec forces thorough pre-design thinking.
*   **Feasibility Unknowns:** Highly effective when the feasibility of a project is initially unclear, allowing for early validation through spikes.
*   **Cost Optimization:** Beneficial when managing token costs is a priority, as it enables the use of more efficient, lower-tier LLMs for code generation.

#### When Not to Use

*   **Small Changes:** For minor tasks like refactoring a single file or making small feature adjustments, the overhead of a full spec-driven workflow is unnecessary.
*   **Simple Adjustments:** A direct "prompt → review code" workflow is more efficient for straightforward modifications.