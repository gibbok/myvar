+++
title = 'Jev System One Decision Engine Overview'
date = 2026-09-19T15:19:14.569115
draft = false
tags = ['decision-engine', 'ai-reasoning', 'typesafe-ai']
description = 'Jev is a System One decision engine returning typed probabilistic outputs from structured input state.'
+++

## Overview

Jev is TypeSafe AI’s System One decision engine, designed to return typed, probabilistic outputs from structured input state and bounded questions. It offloads fast categorical reasoning to specialized models while leaving policy execution, state changes, and safety thresholds entirely inside application code.

## Key Insights

* **Bounded Decision Space**: Evaluates text, JSON, or array state against predefined answer schemas rather than generating open-ended prose.
* **Native Typed Outputs**: Supports **Choice**, **Score**, and **Boolean** data types accompanied by explicit probability distributions across allowed answers.
* **Independent Semantics**: Evaluates multiple concurrent questions against shared evidence without introducing cross-question bias or prompt contamination common in standard LLM adapters.
* **Structural vs. Semantic Safety**: Guarantees output schema conformance, but requires developer validation against historical data to ensure real-world routing accuracy.
* **Decoupled Execution**: Generates decision traces and routing predictions while keeping action authority strictly within application code.

## Technical Details

### System One Paradigm

Named after Daniel Kahneman’s framework for fast, intuitive reasoning, Jev provides an interface optimized for immediate decision-making. Unlike generative language models that produce freeform text or code, Jev accepts a defined state payload and evaluates explicit, bounded questions to return structured choices.

### Structuring Evidence and Decision Context

To ensure consistent evaluations, applications must separate raw evidence from the decision query:

* **Isolate Evidence Context**: Provide raw logs, user notes, and system state as discrete input objects. Include precise timestamps for every observation to avoid temporal ambiguity across multiple calls.
* **Preserve Unprocessed Claims**: Retain original wording and unverified hypotheses within the state payload rather than converting unconfirmed reports into factual assertions.
* **Maintain Unified State Scope**: Arrays passed as input represent a single, shared evaluation context. Group related events within the same state array; separate unrelated incidents into distinct evaluation calls.

### Defining Bounded Answers

Output categories require well-defined boundaries to enable deterministic application routing:

* **Construct Non-Overlapping Categories**: Define clear, observable criteria for each allowable option (e.g., differentiating `payments` from `storefront` based on service boundary failures rather than subjective labels like `urgent`).
* **Provide Fallback Categories**: Include an explicit `insufficient_evidence` option to prevent forced classifications when the state lacks conclusive data.
* **Align Wording with Action**: Frame questions around provisional routing (e.g., *"Which team should investigate first?"*) rather than unverified causality (e.g., *"Which team caused the outage?"*).

### Supported Decision Types

Calls routed via AI Gateway evaluate three primary return types:

| Type | Function | Example Application Query |
| :--- | :--- | :--- |
| **Choice** | Selects a single option from a bounded list | *Which team owns this investigation context?* |
| **Score** | Evaluates input against an ordinal rubric | *How disruptive is the reported impact (1–5 scale)?* |
| **Boolean** | Computes the probability of truth for a statement | *Does the log trace contain failed purchase requests?* |

Jev evaluates multiple independent questions in parallel across the same evidence payload without allowing one answer to influence another.

### Inspectable Decision Trace

To maintain an auditable system of record, applications should log complete decision payloads alongside execution results:

* **Input Context**: Timestamped log excerpt indicating failure at the payment gateway boundary.
* **Question**: *"Which team should investigate first?"*
* **Allowed Schema**: `[payments, storefront, insufficient_evidence]`
* **Model Output**: `payments` (Probability Distribution: `payments`: 0.70, `storefront`: 0.20, `insufficient_evidence`: 0.10)
* **Application Outcome**: Route ticket to the `payments` review queue.

Storing evidence directly alongside model outputs prevents stale assertions from propagating through downstream systems without supporting context.

### Type Safety vs. Semantic Accuracy

Schema conformance ensures that Jev returns a valid data type, but structural validity does not guarantee semantic correctness.

* **Schema Validation**: Guarantees the output matches the expected JSON structure and allowed enum values.
* **Semantic Verification**: Requires evaluating model assignments against historical, resolved datasets to identify edge cases and misclassifications.
* **Policy Enforcement**: Application code must enforce threshold gating. For example, low-confidence assignments (`< 0.80`) or high-impact operational changes should require human approval before execution.

### System Boundaries and Integration

* **No Text or Code Generation**: Jev does not author narrative updates or source code. Use a dedicated generative LLM for text synthesis using Jev’s decision context as input.
* **Text-Based Inputs Only**: Media files (images, audio) must be transcribed or summarized into text descriptions before submission.
* **API Integration**: Callable via the Vercel AI Gateway using the AI SDK experimental evaluation API.

## Frequently Asked Questions

### What does "System One" mean in this context?
It refers to fast, focused, and typed decision-making models, drawing a conceptual parallel to Kahneman's model of intuitive human cognition.

### Can Jev directly execute production rollbacks or code changes?
No. Jev outputs predictions and probabilities. Application code remains responsible for enforcing execution policies and trigger thresholds.

### How does Jev differ from standard LLM structured outputs?
Standard LLM adapters concatenate multiple questions into a single structured prompt, which can introduce cross-question dependency biases. Jev natively preserves independent evaluation semantics for each query.

### Does a valid typed response mean the decision is correct?
No. Type safety guarantees the output fits the declared schema, but semantic correctness must be measured and validated against known real-world outcomes.