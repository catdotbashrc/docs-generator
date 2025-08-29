"""
Invoke tasks for DDD Framework development and demo preparation.
Run 'invoke --list' to see all available tasks.
"""

from invoke import task, Collection
from pathlib import Path
import sys
import os

# Add colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


@task
def install(c):
    """Install all dependencies including dev dependencies."""
    print(f"{Colors.YELLOW}📦 Installing dependencies...{Colors.NC}")
    c.run("uv pip install -e '.[dev]'")
    print(f"{Colors.GREEN}✅ Dependencies installed{Colors.NC}")


@task
def format(c, check=False):
    """Format code with black and ruff."""
    print(f"{Colors.YELLOW}🎨 Formatting code...{Colors.NC}")
    
    if check:
        c.run("black src/ tests/ --line-length 100 --check")
        c.run("ruff check src/ tests/")
    else:
        c.run("black src/ tests/ --line-length 100")
        c.run("ruff check src/ tests/ --fix")
    
    print(f"{Colors.GREEN}✅ Code formatted{Colors.NC}")


@task
def lint(c):
    """Run linting checks."""
    print(f"{Colors.YELLOW}🔍 Linting code...{Colors.NC}")
    c.run("ruff check src/ tests/")
    print(f"{Colors.GREEN}✅ Linting complete{Colors.NC}")


@task
def test(c, critical=False, coverage=False, verbose=False):
    """
    Run tests.
    
    Args:
        critical: Run only critical tests that must pass
        coverage: Include coverage report
        verbose: Verbose output
    """
    print(f"{Colors.YELLOW}🧪 Running tests...{Colors.NC}")
    
    cmd = "uv run pytest"
    
    if critical:
        cmd += " tests/test_abstract_extractor.py tests/test_coverage.py"
        print("Running critical tests only...")
    
    if coverage:
        cmd += " --cov=src --cov-report=term-missing:skip-covered --cov-fail-under=70"
    
    if verbose:
        cmd += " -v"
    else:
        cmd += " -q --tb=short"
    
    result = c.run(cmd, warn=True)
    
    if result.ok:
        print(f"{Colors.GREEN}✅ Tests passed{Colors.NC}")
    else:
        if critical:
            print(f"{Colors.RED}❌ Critical tests failed - these MUST pass!{Colors.NC}")
            sys.exit(1)
        else:
            print(f"{Colors.YELLOW}⚠️ Some tests failed - review before demo{Colors.NC}")


@task
def test_cli(c):
    """Test CLI functionality."""
    print(f"{Colors.YELLOW}🖥️ Testing CLI...{Colors.NC}")
    
    result = c.run("uv run ddd --help", hide=True, warn=True)
    if result.ok:
        print(f"{Colors.GREEN}✅ CLI working{Colors.NC}")
    else:
        print(f"{Colors.RED}❌ CLI broken{Colors.NC}")
        sys.exit(1)
    
    # Test on demo project if it exists
    if Path("./demo-project").exists():
        print(f"{Colors.YELLOW}Testing on demo project...{Colors.NC}")
        c.run("uv run ddd measure ./demo-project", warn=True)


@task
def docs(c, live=False, clean=False, open_browser=False):
    """
    Build documentation.
    
    Args:
        live: Start live-reload server
        clean: Clean before building
        open_browser: Open in browser after building
    """
    print(f"{Colors.YELLOW}📚 Building documentation...{Colors.NC}")
    
    os.chdir("docs")
    
    if clean:
        c.run("rm -rf _build api", warn=True)
    
    if live:
        c.run("sphinx-autobuild . _build/html --port 8000 --open-browser")
    else:
        # Generate API docs
        c.run("sphinx-apidoc -o api ../src/ddd -f -e -M", warn=True)
        
        # Build HTML
        result = c.run("sphinx-build -b html . _build/html", warn=True)
        
        if result.ok:
            print(f"{Colors.GREEN}✅ Docs built at docs/_build/html/index.html{Colors.NC}")
            if open_browser:
                c.run("open _build/html/index.html", warn=True)
        else:
            print(f"{Colors.YELLOW}⚠️ Documentation had warnings{Colors.NC}")
    
    os.chdir("..")


@task
def hooks(c):
    """Install pre-commit hooks."""
    print(f"{Colors.YELLOW}🔧 Installing pre-commit hooks...{Colors.NC}")
    c.run("pre-commit install")
    print(f"{Colors.GREEN}✅ Pre-commit hooks installed{Colors.NC}")


@task
def pre_commit(c, all=False):
    """Run pre-commit checks."""
    print(f"{Colors.YELLOW}🔍 Running pre-commit checks...{Colors.NC}")
    
    if all:
        c.run("pre-commit run --all-files")
    else:
        c.run("pre-commit run")


@task(pre=[install, hooks])
def setup(c):
    """Complete setup for development."""
    print(f"{Colors.GREEN}✅ Development environment ready!{Colors.NC}")


@task(pre=[format, test])
def check(c):
    """Run all checks (format, lint, test)."""
    print(f"{Colors.GREEN}✅ All checks complete{Colors.NC}")


@task
def demo_prep(c):
    """Prepare everything for leadership demo."""
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}     DDD Framework - Demo Preparation{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}\n")
    
    # Install dependencies
    install(c)
    
    # Set up hooks
    hooks(c)
    
    # Format code
    format(c)
    
    # Run critical tests
    test(c, critical=True)
    
    # Run full tests (informational)
    test(c, coverage=True)
    
    # Test CLI
    test_cli(c)
    
    # Build docs
    docs(c, clean=True)
    
    # Create directories
    print(f"{Colors.YELLOW}📁 Creating directories...{Colors.NC}")
    Path("docs/generated").mkdir(parents=True, exist_ok=True)
    Path("docs/runbooks").mkdir(parents=True, exist_ok=True)
    print(f"{Colors.GREEN}✅ Directories ready{Colors.NC}")
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}           DEMO READINESS REPORT{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}\n")
    
    print(f"{Colors.YELLOW}Demo Commands:{Colors.NC}")
    print(f"  {Colors.BLUE}ddd measure ./baseline/ansible{Colors.NC}")
    print(f"  {Colors.BLUE}ddd assert-coverage ./baseline/ansible{Colors.NC}")
    print(f"  {Colors.BLUE}ddd demo ./baseline/ansible{Colors.NC}")
    
    print(f"\n{Colors.YELLOW}View Documentation:{Colors.NC}")
    print(f"  {Colors.BLUE}invoke docs --open-browser{Colors.NC}")
    
    print(f"\n{Colors.GREEN}🎉 DEMO IS READY!{Colors.NC}")


@task
def clean(c):
    """Clean all generated files."""
    print(f"{Colors.YELLOW}🧹 Cleaning generated files...{Colors.NC}")
    
    # Clean Python cache
    c.run("find . -type d -name __pycache__ -exec rm -rf {} +", warn=True)
    c.run("find . -type f -name '*.pyc' -delete", warn=True)
    
    # Clean test/coverage files
    c.run("rm -rf .pytest_cache .coverage htmlcov", warn=True)
    
    # Clean docs
    c.run("rm -rf docs/_build docs/api", warn=True)
    
    # Clean build artifacts
    c.run("rm -rf build dist *.egg-info", warn=True)
    
    print(f"{Colors.GREEN}✅ Cleaned{Colors.NC}")


# Create namespace
ns = Collection()
ns.add_task(install)
ns.add_task(format)
ns.add_task(lint)
ns.add_task(test)
ns.add_task(test_cli)
ns.add_task(docs)
ns.add_task(hooks)
ns.add_task(pre_commit)
ns.add_task(setup)
ns.add_task(check)
ns.add_task(demo_prep)
ns.add_task(clean)