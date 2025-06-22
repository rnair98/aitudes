# Bazel + Nix Flakes Development Environment Setup

## ✅ Completed Setup

This document summarizes the successful implementation of a modern, reproducible development environment for the aitudes monorepo using Bazel and Nix Flakes.

### ✅ What's Been Implemented

#### 1. **Nix Flakes Configuration** (`flake.nix`)

- Modern, reproducible development environment with pinned dependencies
- Python 3.11 with AI/ML packages (numpy, pandas, scikit-learn, torch, transformers)
- Node.js 20, Go 1.21, and Bazel for polyglot development
- Development tools: pytest, black, ruff, mypy, ipykernel
- Onboarding shellHook with environment setup and usage instructions
- Lock file for reproducible builds (`flake.lock`)

#### 2. **Bazel Build System**

- **WORKSPACE**: Configured with rules_nixpkgs for Nix integration, Python rules, Node.js rules, Go rules
- **Root BUILD.bazel**: Project structure definition with file groups and aliases
- **libs/BUILD.bazel**: Library aggregation for monorepo organization
- **libs/swarm/BUILD.bazel**: Complete Python library build configuration with:
  - `py_library` targets for the swarm AI agent library
  - `py_binary` target for CLI usage
  - `py_test` targets for unit testing
  - Build validation and exports

#### 3. **Environment Integration**

- **`.envrc`**: direnv configuration for automatic Nix environment activation
- **`.bazelrc`**: Optimized Bazel configuration with performance settings, CI/dev configs
- **Environment variables**: Project-specific settings for development workflow

#### 4. **Project Structure Validation**

- ✅ Python swarm library imports successfully
- ✅ Dummy tests execute correctly
- ✅ All BUILD.bazel files have valid syntax
- ✅ Git integration with conventional commits and pre-commit hooks

### 🏗️ Architecture Overview

```
aitudes/                     # Monorepo root
├── flake.nix               # Nix Flakes environment definition
├── flake.lock              # Pinned dependency versions
├── .envrc                  # direnv + Nix Flakes integration
├── WORKSPACE               # Bazel workspace with Nix integration
├── BUILD.bazel             # Root build configuration
├── .bazelrc                # Bazel optimization settings
└── libs/                   # Libraries directory
    ├── BUILD.bazel         # Library aggregation
    └── swarm/              # Python AI agent library
        ├── BUILD.bazel     # Swarm build targets
        ├── __init__.py     # Package initialization
        ├── main.py         # CLI application
        ├── models.py       # AI models and config
        ├── types.py        # Type definitions
        ├── utils.py        # Utility functions
        ├── dummy_test.py   # Test infrastructure
        └── utils/          # Utilities subpackage
            └── BUILD.bazel # Utils build config
```

### 🚀 Getting Started

#### Prerequisites
- Nix with flakes enabled
- direnv (optional but recommended)
- Git

#### Quick Start

1. **Clone and enter the environment:**
   ```bash
   cd /path/to/aitudes
   nix develop  # Enter Nix environment
   # OR with direnv:
   direnv allow  # Auto-activate on cd
   ```

2. **Validate the setup:**
   ```bash
   # Test Python library
   python libs/swarm/dummy_test.py

   # Check Bazel (when available)
   bazel version
   bazel build //libs/swarm:swarm
   bazel test //libs/swarm:dummy_test
   ```

3. **Development workflow:**
   ```bash
   # Build all libraries
   bazel build //libs:all

   # Run all tests
   bazel test //libs:test_all

   # Run swarm CLI
   bazel run //libs/swarm:swarm_cli
   ```

## 🔄 Daily Development Workflow

### 🌅 Starting Your Day

#### 1. **Environment Activation**
```bash
cd /path/to/aitudes

# Option A: Manual activation
nix develop

# Option B: Automatic with direnv (recommended)
# Just cd into the directory - environment loads automatically
```

#### 2. **Health Check**
```bash
# Verify your environment
which python bazel node go
python --version
bazel version

# Quick validation
python libs/swarm/dummy_test.py
```

### 💻 Core Development Cycle

#### **Code → Build → Test → Iterate**

```bash
# 1. DEVELOPMENT: Work on your code
vim libs/swarm/main.py  # or your preferred editor

# 2. BUILD: Fast incremental builds
bazel build //libs/swarm:swarm           # Build specific target
bazel build //libs/swarm:...             # Build all swarm targets
bazel build //...                        # Build entire project (careful!)

# 3. TEST: Run tests at different scopes
bazel test //libs/swarm:models_test      # Specific test
bazel test //libs/swarm:...              # All swarm tests
bazel test //libs:test_all               # All library tests

# 4. RUN: Execute your applications
bazel run //libs/swarm:swarm_cli         # Run CLI directly
bazel run //libs/swarm:swarm_cli -- --help  # With arguments
```

### 🎯 Common Workflows

#### **Working on Python Code**
```bash
# Quick iteration cycle for Python development
bazel build //libs/swarm:swarm && bazel test //libs/swarm:test

# Run with hot reloading for development
bazel run //libs/swarm:swarm_cli -- --dev-mode

# Python-specific debugging
bazel run --run_under="python -m pdb" //libs/swarm:swarm_cli

# Check code quality
bazel run @rules_python//python/runfiles:pytest -- libs/swarm/
```

#### **Adding New Dependencies**
```bash
# 1. Add to flake.nix for system-level deps
vim flake.nix
# Add package to buildInputs list

# 2. Rebuild Nix environment
nix flake update  # Update lock file if needed
nix develop --reload  # Reload with new packages

# 3. Add to BUILD.bazel for Python packages
vim libs/swarm/BUILD.bazel
# Add to deps list in py_library

# 4. Test the integration
bazel build //libs/swarm:swarm
```

#### **Working with Multiple Languages**
```bash
# Switch contexts seamlessly (all tools available)
bazel build //frontend:app      # TypeScript/Node.js project
bazel build //backend:server    # Go backend service
bazel build //libs/swarm:swarm  # Python AI library

# Run services together
bazel run //backend:server &
bazel run //frontend:dev_server &
bazel run //libs/swarm:swarm_cli
```

### 🐛 Debugging & Troubleshooting

#### **Build Issues**
```bash
# Clean slate rebuild
bazel clean --expunge
nix develop --reload
bazel build //libs/swarm:swarm

# Verbose build output
bazel build //libs/swarm:swarm --verbose_failures --sandbox_debug

# Check what's actually built
bazel query //libs/swarm:swarm --output=build
```

#### **Environment Issues**
```bash
# Diagnose Nix environment
nix develop --command env | grep -E "(PATH|PYTHON)"
which python bazel

# Reset Nix environment
nix flake update
rm -rf .direnv  # If using direnv
direnv reload

# Check Bazel configuration
bazel info
bazel info workspace
bazel info execution_root
```

#### **Dependency Issues**
```bash
# Analyze dependency graph
bazel query "deps(//libs/swarm:swarm)" --output=graph

# Find circular dependencies
bazel query "somepath(//libs/swarm:swarm, //libs/swarm:swarm)"

# Check what files are actually included
bazel query "//libs/swarm:swarm" --output=xml
```

### 🚀 Performance Optimization

#### **Fast Development Iteration**
```bash
# Use Bazel's watch mode (if available)
bazel run //tools:watch -- //libs/swarm:test

# Build only what changed
bazel build --keep_going //libs/swarm:...

# Use build event stream for analysis
bazel build //libs/swarm:swarm --build_event_json_file=build_events.json
```

#### **Caching Strategies**
```bash
# Local cache optimization
bazel build //libs/swarm:swarm --disk_cache=/tmp/bazel-cache

# Remote cache (team setup)
bazel build //libs/swarm:swarm --remote_cache=https://your-cache-server

# Check cache hit rates
bazel info | grep cache
```

### 🧪 Testing Workflows

#### **Test-Driven Development**
```bash
# Write test first
vim libs/swarm/test_new_feature.py

# Add test to BUILD.bazel
vim libs/swarm/BUILD.bazel

# Red: Run failing test
bazel test //libs/swarm:test_new_feature

# Green: Implement feature
vim libs/swarm/main.py
bazel test //libs/swarm:test_new_feature

# Refactor: Clean up
bazel test //libs/swarm:... # All tests pass
```

#### **Continuous Testing**
```bash
# Run tests on file changes (using entr or similar)
find libs/swarm -name "*.py" | entr -c bazel test //libs/swarm:...

# Pre-commit testing
bazel test //libs/swarm:... && git commit -m "feat: add new feature"
```

### 📦 Release & Deployment

#### **Building for Production**
```bash
# Optimized production build
bazel build --config=prod //libs/swarm:swarm

# Create distributable package
bazel build //libs/swarm:swarm_dist

# Test production build
bazel run --config=prod //libs/swarm:swarm_cli
```

#### **CI/CD Integration**
```bash
# CI pipeline commands
nix develop --command bazel build //...
nix develop --command bazel test //...
nix develop --command bazel run //tools:lint
```

### 🔧 IDE Integration

#### **VS Code Setup**
```bash
# Generate compile_commands.json for C++ (if needed)
bazel run @hedron_compile_commands//:refresh_all

# Python path for IDE
bazel info execution_root
export PYTHONPATH="$(bazel info execution_root):$PYTHONPATH"
```

#### **IntelliJ/PyCharm Setup**
```bash
# Import Bazel project
# Use the Bazel plugin for IntelliJ
# Point to WORKSPACE file as project root
```

### 🤝 Team Collaboration

#### **Syncing with Team**
```bash
# Pull latest changes
git pull origin main

# Update Nix environment
nix flake update
nix develop --reload

# Rebuild everything
bazel clean
bazel build //...
```

#### **Sharing Build Artifacts**
```bash
# Build outputs that can be shared
bazel build //libs/swarm:swarm_dist
cp bazel-bin/libs/swarm/swarm_dist.tar.gz /shared/artifacts/

# Reproducible builds for debugging
bazel build //libs/swarm:swarm --embed_labels --stamp
```

### 💡 Pro Tips & Shortcuts

#### **Bash Aliases**
```bash
# Add to your ~/.bashrc or ~/.zshrc
alias bb='bazel build'
alias bt='bazel test'
alias br='bazel run'
alias bc='bazel clean'
alias nd='nix develop'

# Project-specific aliases
alias swarm-build='bazel build //libs/swarm:swarm'
alias swarm-test='bazel test //libs/swarm:...'
alias swarm-run='bazel run //libs/swarm:swarm_cli'
```

#### **Environment Variables**
```bash
# Speed up builds
export BAZEL_CACHE_DIR=/tmp/bazel-cache
export BAZEL_JOBS=8  # Match your CPU cores

# Python development
export PYTHONPATH="$(pwd):$PYTHONPATH"
export PYTHONDONTWRITEBYTECODE=1
```

#### **Keyboard Shortcuts**
```bash
# Quick commands with history
Ctrl+R: Search command history
!!: Repeat last command
!bb: Repeat last command starting with 'bb'

# Terminal multiplexing
tmux new -s dev  # New development session
tmux attach -t dev  # Attach to existing session
```

### 🎯 Workflow Examples

#### **Morning Routine**
```bash
cd ~/projects/aitudes    # Auto-loads Nix environment with direnv
git pull origin main     # Get latest changes
swarm-test              # Quick validation
# Ready to code!
```

#### **Feature Development**
```bash
git checkout -b feature/new-ai-model
vim libs/swarm/models.py          # Implement feature
swarm-build                       # Quick build check
vim libs/swarm/test_models.py     # Add tests
swarm-test                        # Run tests
git add . && git commit -m "feat: add new AI model"
git push origin feature/new-ai-model
```

#### **Bug Investigation**
```bash
bazel test //libs/swarm:... --test_output=all  # See full test output
bazel run --run_under="python -m pdb" //libs/swarm:swarm_cli  # Debug
bazel build //libs/swarm:swarm --compilation_mode=dbg  # Debug build
```
