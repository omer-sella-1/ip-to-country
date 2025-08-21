#!/bin/bash

echo "🔍 Running code linters and formatters..."
echo ""

echo "📝 Formatting code with Black..."
black src/ tests/

echo ""
echo "📦 Sorting imports with isort..."
isort src/ tests/

echo ""
echo "🔎 Checking code style with Flake8..."
flake8 src/ tests/

echo ""
echo "🔧 Running type checker with mypy..."
mypy src/ tests/ || true

echo ""
echo "✅ Linting complete!"