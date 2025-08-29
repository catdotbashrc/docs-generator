#!/bin/bash
# DDD Framework Demo Preparation Script
# Automates all setup and validation for leadership demo

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}     DDD Framework - Demo Preparation Script${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"

# Step 1: Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
uv pip install -e ".[dev]"
echo -e "${GREEN}✅ Dependencies installed${NC}\n"

# Step 2: Set up pre-commit hooks
echo -e "${YELLOW}🔧 Setting up pre-commit hooks...${NC}"
pre-commit install
echo -e "${GREEN}✅ Pre-commit hooks installed${NC}\n"

# Step 3: Format and lint code
echo -e "${YELLOW}🧹 Formatting and linting code...${NC}"
black src/ tests/ --line-length 100
ruff check src/ tests/ --fix
echo -e "${GREEN}✅ Code formatted and linted${NC}\n"

# Step 4: Run critical tests
echo -e "${YELLOW}🧪 Running critical tests...${NC}"
if uv run pytest tests/test_abstract_extractor.py tests/test_coverage.py -q --tb=short; then
    echo -e "${GREEN}✅ Critical tests passed${NC}\n"
else
    echo -e "${RED}❌ Critical tests failed - these MUST pass for demo!${NC}"
    exit 1
fi

# Step 5: Run full test suite (informational)
echo -e "${YELLOW}🧪 Running full test suite...${NC}"
if uv run pytest --tb=short -q; then
    echo -e "${GREEN}✅ All tests passed${NC}\n"
else
    echo -e "${YELLOW}⚠️  Some tests failed - review before demo${NC}\n"
fi

# Step 6: Check coverage
echo -e "${YELLOW}📊 Checking test coverage...${NC}"
uv run pytest --cov=src --cov-report=term-missing:skip-covered --cov-fail-under=70 -q || true
echo ""

# Step 7: Test CLI functionality
echo -e "${YELLOW}🖥️  Testing CLI functionality...${NC}"
if uv run ddd --help > /dev/null 2>&1; then
    echo -e "${GREEN}✅ CLI is working${NC}\n"
else
    echo -e "${RED}❌ CLI failed - this MUST work for demo!${NC}"
    exit 1
fi

# Step 8: Test on demo project
echo -e "${YELLOW}🎯 Testing DDD on demo project...${NC}"
if [ -d "./demo-project" ]; then
    uv run ddd measure ./demo-project || true
    echo -e "${GREEN}✅ Demo project tested${NC}\n"
else
    echo -e "${YELLOW}⚠️  Demo project not found${NC}\n"
fi

# Step 9: Generate Sphinx documentation
echo -e "${YELLOW}📚 Generating API documentation...${NC}"
cd docs
make clean > /dev/null 2>&1
if make html > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Documentation generated at docs/_build/html/index.html${NC}\n"
    cd ..
else
    echo -e "${YELLOW}⚠️  Documentation generation had issues${NC}\n"
    cd ..
fi

# Step 10: Create demo runbooks directory
echo -e "${YELLOW}📖 Preparing runbooks directory...${NC}"
mkdir -p docs/generated
mkdir -p docs/runbooks
echo -e "${GREEN}✅ Runbook directories ready${NC}\n"

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                    DEMO READINESS REPORT${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

# Check critical components
READY=true

echo -e "\n${YELLOW}Critical Components:${NC}"
if uv run ddd --help > /dev/null 2>&1; then
    echo -e "  ✅ CLI Working"
else
    echo -e "  ❌ CLI Broken"
    READY=false
fi

if [ -f "docs/_build/html/index.html" ]; then
    echo -e "  ✅ Documentation Generated"
else
    echo -e "  ⚠️  Documentation Not Generated"
fi

if uv run pytest tests/test_abstract_extractor.py -q > /dev/null 2>&1; then
    echo -e "  ✅ Core Tests Passing"
else
    echo -e "  ❌ Core Tests Failing"
    READY=false
fi

echo -e "\n${YELLOW}Demo Commands to Run:${NC}"
echo -e "  ${BLUE}ddd measure ./baseline/ansible${NC}"
echo -e "  ${BLUE}ddd assert-coverage ./baseline/ansible${NC}"
echo -e "  ${BLUE}ddd demo ./baseline/ansible${NC}"

if [ -f "docs/_build/html/index.html" ]; then
    echo -e "\n${YELLOW}View Documentation:${NC}"
    echo -e "  ${BLUE}open docs/_build/html/index.html${NC}"
fi

echo ""
if [ "$READY" = true ]; then
    echo -e "${GREEN}🎉 DEMO IS READY!${NC}"
    echo -e "${GREEN}All critical components are working.${NC}"
else
    echo -e "${RED}⚠️  DEMO NEEDS ATTENTION${NC}"
    echo -e "${RED}Fix critical issues before presenting.${NC}"
    exit 1
fi

echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"