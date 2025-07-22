#!/bin/bash
export STREAMLIT_EMAIL=""
export STREAMLIT_ANALYTICS_ENABLED="false"

# Debug: Print PORT value
echo "PORT environment variable: $PORT"

# Use explicit CLI args (more reliable than env vars)
exec streamlit run main.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --browser.gatherUsageStats=false