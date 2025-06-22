workspace(name = "aitudes")

# Load rules for Nix integration
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Rules for Nix integration
http_archive(
    name = "io_tweag_rules_nixpkgs",
    strip_prefix = "rules_nixpkgs-0.11.1",
    urls = ["https://github.com/tweag/rules_nixpkgs/releases/download/v0.11.1/rules_nixpkgs-0.11.1.tar.gz"],
    sha256 = "6b5b3949ca77daf81294eccc7f3b5f96b3af77c6df8bd7d9e4b73fc4c9da1e23",
)

load("@io_tweag_rules_nixpkgs//nixpkgs:repositories.bzl", "rules_nixpkgs_dependencies")
rules_nixpkgs_dependencies()

load("@io_tweag_rules_nixpkgs//nixpkgs:nixpkgs.bzl", "nixpkgs_git_repository", "nixpkgs_package", "nixpkgs_flake_package")

# Use the Nix Flake packages as toolchains
nixpkgs_flake_package(
    name = "python3",
    nix_flake_file = "//:flake.nix",
    package = "python311",
)

nixpkgs_flake_package(
    name = "nodejs",
    nix_flake_file = "//:flake.nix",
    package = "nodejs_20",
)

nixpkgs_flake_package(
    name = "go",
    nix_flake_file = "//:flake.nix",
    package = "go_1_21",
)

# Python rules
http_archive(
    name = "rules_python",
    sha256 = "c68bdc4fbec25de5b5493b8819cfc877c4ea299c0dcb15c244c5a00208cde311",
    strip_prefix = "rules_python-0.31.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.31.0/rules_python-0.31.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

python_register_toolchains(
    name = "python3_11",
    python_version = "3.11",
)

load("@python3_11//:defs.bzl", "interpreter")

# Node.js/TypeScript rules
http_archive(
    name = "aspect_rules_js",
    sha256 = "630a71aba66c4023a5b16ab3efafaeed8b1a2865ccd168a34611eb73876b3fc4",
    strip_prefix = "rules_js-1.37.1",
    url = "https://github.com/aspect-build/rules_js/releases/download/v1.37.1/rules_js-v1.37.1.tar.gz",
)

load("@aspect_rules_js//js:repositories.bzl", "rules_js_dependencies")
rules_js_dependencies()

# Go rules
http_archive(
    name = "io_bazel_rules_go",
    sha256 = "6dc2da7ab4cf5d7bfc7c949776b1b7c733f05e56edc4bcd9022bb249d2e2a996",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v0.39.1/rules_go-v0.39.1.zip",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.39.1/rules_go-v0.39.1.zip",
    ],
)

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")
go_rules_dependencies()

go_register_toolchains(version = "1.21.3")

# Testing framework
http_archive(
    name = "bazel_skylib",
    sha256 = "1c531376ac7e5a180e0237938a2536de0c54d93f5c278634818e0efc952dd56c",
    urls = [
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.3/bazel-skylib-1.0.3.tar.gz",
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.0.3/bazel-skylib-1.0.3.tar.gz",
    ],
)

load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
bazel_skylib_workspace()
