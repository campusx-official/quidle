---
description: Create a spec file and feature branch for the next Inkwell step
argument-hint: "Step number and feature name e.g. 2 login-system"
allowed-tools: Read, Write, Glob, Bash(git:*), Bash(git switch:*), Bash(git checkout:*)
---

You are a senior developer spinning up a new feature for the 
Inkwell blogging platform. Always follow the rules in CLAUDE.md.

User input: $ARGUMENTS

## Step 1 — Check working directory is clean
Run `git status` and check for uncommitted, unstaged, or 
untracked files. If any exist, stop immediately and tell 
the user to commit or stash changes before proceeding. 
DO NOT CONTINUE until the working directory is clean.

## Step 2 — Parse the arguments
From $ARGUMENTS extract:

1. `step_number` — the step number from the roadmap (e.g. 02)
   - Zero-pad to 2 digits: 2 → 02, 11 → 11

2. `feature_title` — human readable title in Title Case
   - Example: "Login System" or "Admin Panel"

3. `feature_slug` — git and file safe slug
   - Lowercase, kebab-case
   - Only a-z, 0-9 and -
   - Replace spaces and punctuation with -
   - Collapse multiple - into one
   - Trim - from start and end
   - Maximum 40 characters
   - Example: login-system, admin-panel

4. `branch_name` — format: feature/<feature_slug>
   - Example: feature/login-system

If you cannot infer these from $ARGUMENTS, ask the user 
to clarify before proceeding.

## Step 3 — Check branch name is not taken
Run `git branch` to list existing branches.
If `branch_name` is already taken, append a number:
feature/login-system-01, feature/login-system-02, etc.

## Step 4 — Switch to main and pull latest
```
git checkout main
git pull origin main
```
This ensures the new branch is always based on latest main.

## Step 5 — Create and switch to the feature branch
```
git checkout -b <branch_name>
```
Confirm the branch was created successfully before continuing.

## Step 6 — Research the codebase
Read the following files before writing the spec:
- CLAUDE.md — current roadmap and conventions
- app.py — existing routes and structure
- database/db.py — existing schema
- All files in .claude/specs/ — avoid duplicating existing specs

Check CLAUDE.md to confirm the requested step is not already 
marked complete. If it is, warn the user and stop.

## Step 7 — Write the spec
Generate a spec document with this exact structure:

# Spec: <feature_title>

## Overview
One paragraph describing what this feature does and why
it exists at this stage of the Inkwell roadmap.

## Depends on
List which previous steps this feature requires to be 
complete first.

## Routes
Every new route needed:
- METHOD /path — description — access level (public/logged-in/admin)

If no new routes: state "No new routes".

## Database changes
Any new tables, columns, or constraints.
Always verify against database/db.py before writing this section.
If none: state "No database changes".

## Templates
- Create: list new templates with their path
- Modify: list existing templates and what changes

## Files to change
Every file that will be modified.

## Files to create
Every new file that will be created.

## New dependencies
Any new pip packages. If none: state "No new dependencies".

## Rules for implementation
Any specific constraints Claude must follow when 
implementing this feature. Always include:
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords must be hashed with werkzeug

## Definition of done
A specific, testable checklist. Each item must be 
something that can be verified by running the app.

## Step 8 — Save the spec
Save the spec to:
.claude/specs/<step_number>-<feature_slug>.md

## Step 9 — Stage and commit the spec
```
git add .claude/specs/<step_number>-<feature_slug>.md
git commit -m "chore: add spec for <feature_title>"
```

## Step 10 — Report to the user
Print a short summary in this exact format:

Branch: <branch_name>
Spec file: .claude/specs/<step_number>-<feature_slug>.md
Title: <feature_title>

Then tell the user:
"Review the spec at .claude/specs/<step_number>-<feature_slug>.md 
then enter Plan Mode with Shift+Tab twice to begin implementation."

Do not print the full spec in chat output unless explicitly asked.