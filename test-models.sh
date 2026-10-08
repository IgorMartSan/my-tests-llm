#!/usr/bin/env bash

set -u

test_model() {
  local name="$1"
  local url="$2"
  local model="$3"

  echo "=== Testando ${name} ==="
  curl -sS --max-time 120 \
    -w "\nHTTP_STATUS=%{http_code}\n" \
    "$url" \
    -H 'Content-Type: application/json' \
    -d "{\"model\":\"${model}\",\"messages\":[{\"role\":\"user\",\"content\":\"Responda apenas: ${name} funcionando\"}],\"max_tokens\":30}"
  echo
}

test_model "Gemma 4" "http://localhost:8072/v1/chat/completions" "gemma4"

echo "=== Testando Laya ==="
curl -sS --max-time 30 \
  -w "\nHTTP_STATUS=%{http_code}\n" \
  "http://localhost:8003/health"
