#!/bin/bash
export STREAMLIT_EMAIL=""
export STREAMLIT_ANALYTICS_ENABLED="false"

# Utiliser la config production et forcer les paramètres
streamlit run main.py \
  --server.port $PORT \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --browser.gatherUsageStats false \
  --server.enableXsrfProtection false