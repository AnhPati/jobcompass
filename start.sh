#!/bin/bash
export STREAMLIT_EMAIL=""
export STREAMLIT_ANALYTICS_ENABLED="false"

# Use PORT if available, fallback to 10000
RENDER_PORT=${PORT:-10000}
echo "Using port: $RENDER_PORT"

# Use explicit CLI args
exec streamlit run main.py \
    --server.port=$RENDER_PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --browser.gatherUsageStats=false