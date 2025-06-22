"""
Dummy test file for swarm library.
This allows Bazel testing to work even when specific test files don't exist.
"""


def test_dummy():
    """Dummy test that always passes."""
    assert True, "This is a dummy test that should always pass"


if __name__ == "__main__":
    test_dummy()
    print("Dummy test passed!")
