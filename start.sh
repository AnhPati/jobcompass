#!/bin/bash
export STREAMLIT_EMAIL=""
export STREAMLIT_ANALYTICS_ENABLED="false"

# Force Streamlit to use the PORT environment variable
export STREAMLIT_SERVER_PORT=$PORT
export STREAMLIT_SERVER_ADDRESS="0.0.0.0"
export STREAMLIT_SERVER_HEADLESS="true"
export STREAMLIT_BROWSER_GATHER_USAGE_STATS="false"

streamlit run main.py