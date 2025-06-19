# Agent Development Guidelines

## Tooling Preferences

### Package Execution

- **Use `bunx` instead of `npx`** for running Node.js packages
- Bun provides faster execution and better performance than npm
- Example: `bunx markdownlint-cli2 --fix *.md` instead of `npx markdownlint-cli2 --fix *.md`

### Command Line Tools

- Prefer Bun-based tools where available for improved performance
- Maintain consistency across development environment

## Development Standards

### Code Quality

- Follow the comprehensive pair programming instructions in `.github/copilot-instructions.md`
- Implement systematic problem analysis and solution decomposition
- Prioritize maintainability, scalability, and performance

### Architecture Principles

- Apply SOLID principles consistently
- Use proven design patterns (Factory, Observer, Strategy, etc.)
- Implement comprehensive testing strategies (unit, integration, e2e)
- Document architectural decisions and trade-offs

### Build System

- Target migration to Bazel-based polyglot monorepo (see PLAN.md)
- Implement hermetic builds with aggressive caching
- Optimize for incremental compilation and parallel execution

### Version Control & Git Workflow

#### Commit Strategy

- **Use conventional commits** for all changes to maintain clear history
- **Batch thematic changes** into logical commits with descriptive messages
- Follow format: `<type>(<scope>): <description>`
  - Examples: `feat(agent): add multi-provider LLM support`, `refactor(build): migrate to Bazel`
- Include detailed commit body for complex changes explaining the "why"

#### Local Development Workflow

- **Maximize git features** for experimentation and iteration:
  - Use feature branches for all non-trivial changes: `git checkout -b feature/agent-optimization`
  - Leverage git worktrees for parallel development: `git worktree add ../feature-branch feature/new-feature`
  - Utilize interactive rebase for clean history: `git rebase -i HEAD~n`
  - Employ git stash for temporary work: `git stash push -m "WIP: debugging agent runtime"`

#### Experimentation & Iteration

- **Create experimental branches** freely for testing ideas
- **Use git worktrees** to work on multiple features simultaneously without switching context
- **Commit early and often** during development, then clean up with interactive rebase
- **Create backup branches** before major refactoring: `git branch backup-before-refactor`

#### History Management

- **Clean up commit history** before sharing:
  - Squash related commits: `git rebase -i` to combine WIP commits
  - Reorder commits logically to tell a coherent story
  - Split large commits into focused, atomic changes
  - Ensure each commit passes tests and builds successfully

#### Branch Protection & Approval

- **Local branches**: Full freedom to experiment, create, merge, and delete
- **Feature/Development branches**: **Requires explicit human approval before pushing**
  - Request permission: "May I push this feature branch for review?"
  - Provide context: branch purpose, changes included, testing status
  - Wait for explicit approval before `git push origin feature/branch-name`
- **Main/Master branch**: Never push directly, use pull requests only

#### Git Best Practices

- **Write meaningful commit messages** that explain the business value
- **Use git hooks** for automated quality checks (pre-commit, pre-push)
- **Tag releases** with semantic versioning: `git tag -a v1.2.3 -m "Release v1.2.3"`
- **Maintain clean repository** by regularly pruning merged branches
- **Document git aliases** for common workflows in project documentation

## AI/ML Specific Guidelines

### Model Management

- Use semantic versioning for model releases
- Implement proper model asset handling (Git LFS for large files)
- Create reproducible model training and inference pipelines

### Agent Development

- Maintain clear separation between agent core logic and LLM integrations
- Implement robust error handling and fallback mechanisms
- Design for multi-provider LLM support (OpenAI, Google, Perplexity, etc.)

## Notes

- Updated: June 19, 2025
- This file serves as a living document for development preferences and standards
