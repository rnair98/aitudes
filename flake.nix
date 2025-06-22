{
  description = "Aitudes AI Agents Platform - Polyglot Development Environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = {
            allowUnfree = true; # For CUDA packages if needed
          };
        };

        # AI/ML optimized Python environment matching your current setup
        aiPythonEnv = pkgs.python311.withPackages (ps: with ps; [
          # Core aitudes dependencies (from your pyproject.toml)
          openai
          loguru
          numpy
          jinja2

          # AI/ML stack
          torch
          transformers
          huggingface-hub

          # MCP protocol (when available)
          # Note: mcp package might need manual installation via pip in shell

          # Development and testing tools
          pkgs.python311Packages.pytest
          pkgs.python311Packages.black
          ruff
          pkgs.python311Packages.mypy
          pkgs.python311Packages.ipykernel

          # Additional packages from your current setup
          requests
          typing-extensions
        ]);

        # Base development tools
        baseDevTools = with pkgs; [
          # Bazel ecosystem
          bazel_7
          buildifier
          buildozer

          # Version control and environment
          git
          direnv

          # Utilities
          jq
          curl
          wget

          # UV for Python package management (transitional)
          python311Packages.uv
        ];

      in
      {
        # Development environments
        devShells = {
          # Main development environment
          default = pkgs.mkShell {
            buildInputs = baseDevTools ++ [
              aiPythonEnv
              pkgs.nodejs_20
              pkgs.nodePackages.pnpm
              pkgs.go_1_22
            ];

            shellHook = ''
              echo "🚀 Aitudes AI Development Environment"
              echo "======================================"
              echo "📦 Bazel: $(bazel version --short 2>/dev/null || echo 'installing...')"
              echo "🐍 Python: $(python --version)"
              echo "📜 Node.js: $(node --version)"
              echo "🐹 Go: $(go version | cut -d' ' -f3)"
              echo ""
              echo "🧠 AI/ML Stack:"
              python -c "
import sys
try:
    import torch; print(f'  - PyTorch: {torch.__version__}')
except: print('  - PyTorch: not available')
try:
    import transformers; print(f'  - Transformers: {transformers.__version__}')
except: print('  - Transformers: not available')
try:
    import openai; print(f'  - OpenAI: {openai.__version__}')
except: print('  - OpenAI: not available')
" 2>/dev/null || echo "  - Python packages loading..."
              echo ""
              echo "💡 Available commands:"
              echo "  - bazel build //libs/swarm:all"
              echo "  - bazel test //libs/swarm:all"
              echo "  - python -m pytest (legacy testing)"
              echo ""

              # Set up Python path for local development
              export PYTHONPATH="$PWD/libs:$PWD/smolagents:$PYTHONPATH"

              # Set reasonable defaults for AI development
              export TOKENIZERS_PARALLELISM=false
              export HF_HOME="$HOME/.cache/huggingface"

              # Development helpers
              alias bazel-build="bazel build //..."
              alias bazel-test="bazel test //..."
              alias python-test="python -m pytest"
              alias format-python="ruff format . && ruff check --fix ."

              # Install MCP if not available in nixpkgs yet
              if ! python -c "import mcp" 2>/dev/null; then
                echo "📦 Installing MCP package via pip..."
                pip install mcp[cli]>=1.9.1 --user --quiet || echo "⚠️  MCP installation failed"
              fi

              echo "✅ Environment ready! Use 'direnv allow' for auto-activation"
            '';
          };

          # Minimal environment for CI/CD
          ci = pkgs.mkShell {
            buildInputs = [
              aiPythonEnv
              pkgs.bazel_7
              pkgs.git
              pkgs.ruff
            ];

            shellHook = ''
              echo "🤖 Aitudes CI Environment"
              echo "Minimal environment for automated testing"
              export PYTHONPATH="$PWD/libs:$PWD/smolagents:$PYTHONPATH"
            '';
          };
        };

        # Packages for Bazel integration
        packages = {
          python = aiPythonEnv;
          bazel = pkgs.bazel_7;
          nodejs = pkgs.nodejs_20;
          go = pkgs.go_1_21;
        };

        # Apps for direct execution
        apps = {
          # Run agent directly
          agent = {
            type = "app";
            program = "${aiPythonEnv}/bin/python";
            args = [ "-m" "libs.swarm.main" ];
          };
        };
      }
    );
}
