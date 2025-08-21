#!/bin/bash

echo "🧪 Running test suite..."
echo ""

echo "📋 Unit Tests:"
pytest tests/unit/ -v

echo ""
echo "🔗 Integration Tests:"
pytest tests/integration/ -v

echo ""
echo "📊 Test Coverage Summary:"
pytest tests/ --tb=short

echo ""
echo "✅ Testing complete!"