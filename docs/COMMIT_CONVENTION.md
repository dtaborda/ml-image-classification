# 📝 Commit Message Convention

This project follows the **Conventional Commits 1.0.0** specification for clear, semantic commit history.

## Quick Reference

### Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Common Types
- **feat** - New feature
- **fix** - Bug fix  
- **docs** - Documentation changes
- **refactor** - Code refactoring
- **test** - Test changes
- **chore** - Maintenance tasks

### Common Scopes
- **api** - FastAPI backend
- **model** - ML service
- **ui** - Streamlit frontend
- **docker** - Infrastructure
- **db** - Database

### Examples

✅ **Good:**
```
feat(api): add user authentication endpoint
fix(docker): resolve h5py compilation on ARM64
docs(readme): update setup for Apple Silicon
test(model): add unit tests for preprocessing
```

❌ **Bad:**
```
Fixed bug
Update code
WIP
changes
```

## Detailed Guidelines

### 1. Type

Choose the appropriate type that describes your change:

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature for the user | `feat(api): add image upload endpoint` |
| `fix` | Bug fix for the user | `fix(model): handle invalid image formats` |
| `docs` | Documentation only | `docs: add API reference guide` |
| `style` | Code style/formatting | `style(api): format with black` |
| `refactor` | Code change (no bug fix or feature) | `refactor(ui): extract upload component` |
| `perf` | Performance improvement | `perf(model): optimize image preprocessing` |
| `test` | Add or modify tests | `test(api): add auth endpoint tests` |
| `build` | Build system changes | `build: update docker base image` |
| `ci` | CI configuration changes | `ci: add lint workflow` |
| `chore` | Other maintenance | `chore: update dependencies` |
| `revert` | Revert previous commit | `revert: feat(api): add upload endpoint` |

### 2. Scope

The scope specifies which part of the codebase is affected:

| Scope | Description | Files |
|-------|-------------|-------|
| `api` | FastAPI backend service | `api/**` |
| `model` | ML model service | `model/**` |
| `ui` | Streamlit UI service | `ui/**` |
| `docker` | Docker/infrastructure | `Dockerfile*`, `docker-compose.yml` |
| `db` | Database related | Database migrations, models |
| `auth` | Authentication/authorization | Auth modules |
| `tests` | Testing infrastructure | Test configuration |
| `docs` | Documentation | `docs/**`, `README.md` |
| `deps` | Dependencies | `requirements.txt`, `package.json` |

**Multiple scopes:** Use the primary scope or `multi` if changes span many areas.

**No scope:** Omit scope for project-wide changes (e.g., `chore: update .gitignore`)

### 3. Subject

The subject is a concise description of the change:

**Rules:**
- ✅ Use **imperative mood**: "add" not "added" or "adds"
- ✅ **Lowercase** first letter
- ✅ **No period** at the end
- ✅ Maximum **72 characters** (aim for 50)
- ✅ Be **specific** and **descriptive**

**Good subjects:**
```
add user profile endpoint
fix memory leak in image preprocessing
update installation instructions
refactor authentication middleware
```

**Bad subjects:**
```
Added feature (past tense)
Fix bug (too vague)
Update (no context)
changes to api (not imperative, too vague)
```

### 4. Body (Optional)

The body provides additional context:

**When to use:**
- The change is not obvious from the diff
- Multiple related changes in one commit
- Need to explain **why** not **what**

**Format:**
- Separate from subject with **blank line**
- Wrap at **72 characters**
- Use **bullet points** for multiple items
- Focus on **motivation** and **context**

**Example:**
```
fix(docker): resolve h5py compilation on ARM64

- Add h5py==3.8.0 before tensorflow in requirements
- Ensures pre-compiled wheel is used instead of source compilation
- Prevents HDF5 library dependency error

This fixes build failures on Apple Silicon (M1/M2/M3) chips
where HDF5 system libraries are not available in the Docker image.
```

### 5. Footer (Optional)

The footer contains metadata:

**Issue references:**
```
Fixes #123
Closes #456, #789
Refs #234
```

**Epic tracking:**
```
Refs: EPIC-2-T3
```

**Breaking changes:**
```
BREAKING CHANGE: Old session-based auth no longer supported.
Clients must now use JWT Bearer tokens in Authorization header.
Migration guide: docs/auth-migration.md
```

## Sprint-Specific Conventions

For epic-based development, include epic tracking:

### Option 1: In subject (recommended for epic tasks)
```
feat(api): [EPIC-2] implement ML prediction endpoint
fix(docker): [EPIC-1] resolve h5py compilation
```

### Option 2: In footer (recommended for bug fixes)
```
fix(model): handle null predictions

When model fails to classify, return empty predictions
instead of crashing.

Refs: EPIC-2-T4
Fixes #42
```

## Complete Examples

### Simple Feature
```
feat(api): add user profile endpoint

Implements GET /user/profile with authentication middleware.
Returns user data including name, email, and registration date.

Refs: EPIC-3-T2
```

### Bug Fix
```
fix(model): resolve memory leak in image preprocessing

The image buffers weren't being released after processing,
causing memory usage to grow over time. Added explicit cleanup
in the finally block.

Fixes #156
```

### Documentation
```
docs(readme): update installation for Apple Silicon

- Add troubleshooting section for M1/M2/M3 chips
- Document TensorFlow 2.13.0 requirement
- Include h5py compatibility notes

Closes #89
```

### Breaking Change
```
feat(api): migrate to JWT authentication

BREAKING CHANGE: Session-based authentication removed.

- Replace session cookies with JWT Bearer tokens
- Add token refresh endpoint at POST /auth/refresh
- Update all endpoints to use Authorization header

Clients must update to include:
Authorization: Bearer <token>

Migration guide: docs/auth-migration.md

Refs: EPIC-5-T1
```

### Refactoring
```
refactor(api,model): standardize error response format

- API returns consistent JSON error structure
- Model service updated to match new format
- Update integration tests for new format

This improves error handling consistency across services
and makes client error parsing simpler.

Refs: EPIC-4-T3
```

## Using the `/commit` Command

For guided commit creation, use:

```bash
/commit
```

The assistant will:
1. Analyze your staged changes
2. Auto-detect type and scope
3. Generate a semantic commit message
4. Allow you to review/edit before committing

**With options:**
```bash
/commit --epic 2              # Add [EPIC-2] tag
/commit --breaking            # Mark as breaking change
/commit --scope docker        # Override scope detection
```

## Commit Message Checklist

Before committing, verify:

- [ ] Type is correct (feat/fix/docs/etc)
- [ ] Scope matches affected area
- [ ] Subject uses imperative mood
- [ ] Subject is lowercase and under 72 chars
- [ ] Subject has no period at the end
- [ ] Body explains WHY if not obvious
- [ ] Footer includes epic/issue references
- [ ] Breaking changes are clearly marked

## Tools & Configuration

### Git Commit Template

The project includes a commit template in `.gitmessage`. To use it:

```bash
git config commit.template .gitmessage
```

This will show the template when you run `git commit` (without `-m`).

### Conventional Commits Tools

**Validation:** Use commitlint to enforce convention

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

**Interactive commits:** Use commitizen

```bash
npm install --save-dev commitizen cz-conventional-changelog
git cz  # Instead of git commit
```

## Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)

## Common Mistakes

### ❌ Mistake 1: Using past tense
```
fix(api): fixed authentication bug
```
✅ **Correct:**
```
fix(api): resolve authentication bug
```

### ❌ Mistake 2: Too vague
```
feat(api): update code
```
✅ **Correct:**
```
feat(api): add pagination to user list endpoint
```

### ❌ Mistake 3: Multiple unrelated changes
```
feat(api): add auth endpoint and fix bug and update docs
```
✅ **Correct:** Split into separate commits
```
feat(api): add user authentication endpoint
fix(api): resolve token expiration bug
docs(api): document authentication flow
```

### ❌ Mistake 4: Subject too long
```
feat(api): add new endpoint for user authentication with JWT tokens and refresh token support
```
✅ **Correct:**
```
feat(api): add JWT authentication endpoint

- Support access and refresh tokens
- Include token expiration handling
- Add refresh endpoint for token renewal
```

---

**Last Updated:** 2026-01-13  
**Version:** 1.0.0
