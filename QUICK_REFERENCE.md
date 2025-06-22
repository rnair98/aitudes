# 🚀 Nix + Bazel Quick Reference

## ⚡ Essential Commands

### Environment
```bash
nix develop                    # Enter development environment
direnv allow                   # Auto-activate environment
nix flake update              # Update dependencies
```

### Build & Test
```bash
bazel build //libs/swarm:swarm          # Build library
bazel test //libs/swarm:...             # Test all swarm targets
bazel run //libs/swarm:swarm_cli        # Run CLI application
```

### Quick Development Cycle
```bash
# The 3-step development loop:
1. Edit code
2. bazel build //libs/swarm:swarm       # Fast incremental build
3. bazel test //libs/swarm:test         # Validate changes
```

## 🔧 Troubleshooting

### Build Problems
```bash
bazel clean --expunge         # Nuclear option - clean everything
nix develop --reload          # Reload Nix environment
```

### Environment Issues
```bash
which python bazel            # Verify tools are available
nix develop --command env     # Check environment variables
```

## 💡 Pro Tips

### Aliases (add to ~/.bashrc)
```bash
alias bb='bazel build'
alias bt='bazel test'
alias br='bazel run'
alias swarm='bazel run //libs/swarm:swarm_cli'
```

### Common Workflows
```bash
# Morning routine
cd ~/projects/aitudes && git pull && bt //libs/swarm:...

# Feature development
git checkout -b feature/name
# code...
bb //libs/swarm:swarm && bt //libs/swarm:test
git commit -am "feat: description"

# Debug mode
br --run_under="python -m pdb" //libs/swarm:swarm_cli
```

## 📊 Performance

### Faster Builds
```bash
bazel build --jobs=8                    # Parallel builds
bazel build --disk_cache=/tmp/cache     # Local caching
export BAZEL_CACHE_DIR=/tmp/bazel-cache # Persistent cache
```

### Selective Building
```bash
bazel build //libs/swarm:...           # Just swarm library
bazel test //libs/swarm:models_test    # Specific test
bazel build --keep_going //...         # Continue on errors
```

## 🎯 Daily Workflow

1. **Start**: `cd project && nix develop` (or auto with direnv)
2. **Code**: Edit files in your favorite editor
3. **Build**: `bb //libs/swarm:swarm` for quick validation
4. **Test**: `bt //libs/swarm:test` for your changes
5. **Run**: `br //libs/swarm:swarm_cli` to test CLI
6. **Commit**: `git add . && git commit -m "feat: description"`

## 🆘 Help

```bash
bazel help                    # Bazel commands
nix develop --help           # Nix options
bazel query --help          # Query syntax
```
