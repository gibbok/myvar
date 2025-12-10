+++
title = 'Cloudflare Web Analytics on Astro Starlight'
date = 2025-11-18T09:00:00-07:00
draft = false
tags = ['frontend-development', 'cloudflare', 'astro', 'web-analytics']
description = 'Integrate Cloudflare Web Analytics into your Astro Starlight documentation site. Get simple, privacy-first performance metrics without impacting your sites speed or using cookies.'
+++

## Definition and Categories

The term **“AI bot”** refers to three distinct use cases, which differ significantly in purpose, architecture, and impact for detection teams:

- **LLM scrapers/crawlers**  
  Collect content at scale to train large language models (LLMs). Examples include GPTBot and ClaudeBot.

- **RAG/search bots**  
  Retrieve real-time information to augment LLM responses, acting narrowly and only in response to specific user queries. Examples include ChatGPT-User and Claude-User.

- **AI agents**  
  Perform actions on behalf of users, such as navigating websites, filling out forms, or making purchases.

## Detection of Scrapers and RAG Bots

- **LLM scrapers**  
  Often identifiable, rate-limited, and transparent (e.g., via documented user agents). Detection decisions are frequently policy-based rather than purely technical.

- **RAG bots**  
  Operate on behalf of a human and typically perform targeted one-off fetches; blocking them can break legitimate functionality for AI-powered search engines and assistants.

## Disruptiveness of AI Agents

AI agents are the most disruptive category because they automate high-risk workflows and challenge traditional fraud assumptions.

### Types

- **Cloud-based agents**  
  Run on provider infrastructure (e.g., OpenAI’s Operator).

- **Local agents**  
  Run on the user’s device or inside the user’s browser context (e.g., Perplexity’s Comet).

### Stealth

Most AI agents deliberately avoid exposing their presence. They typically do not use custom user agent strings and avoid bot signals such as `navigator.webdriver = true`, blending in with legitimate browser traffic.

### Detection Challenge

Automation is no longer inherently suspicious, pushing detection pipelines to shift away from static fingerprints or IP-based checks. Instead, detection must focus on intent, delegation patterns, and whether the action aligns with a real user’s goals.

### Authentication Issues

Cloud-based agents often share the same IP infrastructure, making IP reputation ineffective, while local agents mimic legitimate user behavior, making them difficult to isolate or verify.

