# Claude usage transparency

This document logs how Claude was used during the development of this project, following Anthropic's guidance on transparent AI collaboration.

## Model used
`claude-sonnet-4-6` via the Anthropic API

## Usage in the tools

| Tool | How Claude is used | Prompts location |
|------|-------------------|-----------------|
| SpecLab | Analyzes behavioral divergence across model responses; classifies which value each model prioritized; identifies spec implications | `prompts/speclab_analysis.txt` |
| SentinelBench | Acts as the safety monitor; rates transcript suspiciousness 0–100; identifies which blind spot category is being exploited | `prompts/sentinelbench_monitor.txt` |
| SkillForge | Provides Socratic tutoring during AI-assisted task sessions; does not give direct solutions | `prompts/skillforge_tutor.txt` |

## Usage during development

- Used Claude to review statistical analysis approach in `notebooks/`
- Used Claude to generate initial value-conflict scenario seed ideas (then hand-edited and expanded)
- Used Claude to check prompt clarity for the monitor system prompt
- Used Claude to review this README for clarity

## What Claude did NOT do

- Did not write the core Python logic (runner files, CLI, status checker)
- Did not write the application answers
- Did not generate the research hypotheses
- Did not select the research directions or which blind spot categories to focus on

## Prompt design notes

All prompts instruct Claude to return JSON only, with no markdown fences, to support reliable parsing. Prompts are stored as plain text files so changes are tracked in git history.
