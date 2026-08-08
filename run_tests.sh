#!/usr/bin/env bash
set -e

echo "Running backend tests..."
(cd backend && pytest)

echo "Running frontend tests..."
(cd frontend && npm test)
