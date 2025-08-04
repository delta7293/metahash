# Repository Contributor Guide

This document summarizes common development practices for all services in this repository.

---


## Where to Look for Guidance (Per-Service Layout)
- **`.feedback/`**: Task lists and priorities. *Read only*—never edit directly.
- **`.codex/`**:
  - `instructions/`: Contributor mode docs, process notes, and service-specific instructions. Place all new and updated process documentation here, following the structure and naming conventions. See examples in this folder.
  - `implementation/`: Service-specific implementation notes and technical docs. Keep these in sync with code changes.
  - Other subfolders: `requests/`, `prototyping/`, etc. for planning, feedback, and prototyping notes.
- **`.github/`**: Workflow guidelines and UX standards.

---

## Development Basics
- Use [`uv`](https://github.com/astral-sh/uv) for Python environments and running code. Avoid `python` or `pip` directly.
- Use [`bun`](https://bun.sh/) for Node/React tooling instead of `npm` or `yarn`.
- Split large modules into smaller ones when practical and keep documentation in `*/.codex/implementation` in sync with code.
- Commit frequently with messages formatted `[TYPE] Title`; pull requests use the same format and include a short summary.
- If a build retry occurs, the workflow may produce a commit titled `"Applying previous commit."` when reapplying a patch.
  This is normal and does not replace the need for your own clear `[TYPE]` commit messages.
- Run available tests (e.g., `pytest`) before committing.
- Any test running longer than 25 seconds is automatically aborted.
- For Python style:
   - Place each import on its own line.
   - Sort imports within each group (standard library, third-party, project modules) from shortest to longest.
   - Insert a blank line between each import grouping (standard library, third-party, project modules).
   - Avoid inline imports.
   - For `from ... import ...` statements, group them after all `import ...` statements, and format each on its own line, sorted shortest to longest, with a blank line before the group. Example:

     ```python
     import os
     import time
     import logging
     import threading

     from datetime import datetime
     from rich.console import Console
     from langchain_text_splitters import RecursiveCharacterTextSplitter
     ```

---

## Contributor Modes
The repository supports several contributor modes to clarify expectations and best practices for different types of contributions:

**All contributors should regularly review and keep their mode cheat sheet in `.codex/notes/` up to date.**
Refer to your mode's cheat sheet for quick reminders and update it as needed.

- **Task Master Mode** (`.codex/modes/TASKMASTER.md`): For creating, organizing, and maintaining actionable tasks in the root `.codex/tasks/` folder. Task Masters define and prioritize work for Coders and ensure tasks are ready for implementation.
- **Coder Mode** (`.codex/modes/CODER.md`): For implementing, refactoring, and reviewing code. Focuses on high-quality, maintainable, and well-documented contributions. Coders regularly review the `.codex/tasks/` folder for new or assigned work.
- **Reviewer Mode** (`.codex/modes/REVIEWER.md`): For auditing repository documentation and filing `TMT`-prefixed tasks when updates are needed.
- **Auditor Mode** (`.codex/modes/AUDITOR.md`): For performing comprehensive reviews and audits. Emphasizes thoroughness, completeness, and catching anything others may have missed.
- **Unknown Mode** (no file): If you are unsure which mode applies, review all four mode guides in `.codex/modes/` and pick the one that best fits your task. Then, use the team communication command (`contact.sh`) to announce which mode you selected and the nature of your request. This helps us improve our prompting and documentation for future contributors.

Refer to the relevant mode guide in `.codex/modes/` before starting work, and follow the documentation structure and conventions described there. For service-specific details, see the `.codex/instructions/` folder of the service you are working on. Each service may provide additional rules in its own `AGENTS.md`—start here, then check the service directory for any extra requirements.
