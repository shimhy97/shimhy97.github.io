# Ralph Agent Instructions for This Blog

You are an autonomous coding agent working on a Jekyll-based GitHub Pages technical blog.

## Project Context

- This repository is a technical blog for a data scientist.
- The owner is new to GitHub Pages and wants outputs that remain understandable.
- The site uses Jekyll with the `minimal-mistakes-jekyll` gem and deploys through GitHub Actions Pages.
- The site must keep building with `./scripts/blog-build.sh`.

## Repository Rules

- Read `AGENTS.md` before editing.
- Follow the repository documentation rule: when code changes need explanation, prefer Korean comments and docs.
- Keep commit messages in Korean using this pattern:
  - `동사:수행한 이유 + 수행한 내역`
  - Example: `정리:블로그 소개 문구와 About 페이지를 실제 운영 정보로 수정`

## Your Task

1. Read `./prd.json`.
2. Read `./progress.txt`, especially the `## Codebase Patterns` section.
3. Check the target branch from `prd.json.branchName`. If needed, create it from `main`.
4. Pick the highest-priority user story where `passes` is `false`.
5. Implement only that single story.
6. Run the quality check for this repository:
   - `./scripts/blog-build.sh`
7. If you discover reusable knowledge, update nearby `AGENTS.md` files.
8. If the quality check passes, commit all related changes with a Korean commit message that follows this repository rule.
9. Update `prd.json` so the completed story has `passes: true`.
10. Append a progress report to `progress.txt`.

## Progress Report Format

Append to `progress.txt`:

```text
## [Date/Time] - [Story ID]
Thread: [tool thread or manual]
- What was implemented
- Files changed
- Learnings for future iterations:
  - Reusable patterns
  - Gotchas
  - Useful context
---
```

## Quality Requirements

- Do not work on more than one story per iteration.
- Do not commit broken code.
- Keep changes small and reviewable.
- Prefer project-root files for Ralph state:
  - `./prd.json`
  - `./progress.txt`
  - `./tasks/`

## Blog-Specific Notes

- `_config.yml` holds the site metadata, author info, and plugins.
- `_data/navigation.yml` holds the top navigation.
- `_posts/` stores technical posts.
- `_pages/` stores static pages such as About, Tags, and Categories.
- If you change content or layout, make sure links and permalinks still work after build.
- For GitHub user-page deployment, the repository name must remain `shimhy97.github.io`.

## Stop Condition

After a successful story, check whether all stories in `prd.json` have `passes: true`.

If all stories pass, reply with:

```text
<promise>COMPLETE</promise>
```

Otherwise, end normally so the next Ralph iteration can continue.
