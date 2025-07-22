import os
import streamlit as st

# Force Streamlit to use Render's PORT
if 'PORT' in os.environ:
    st._config.set_option('server.port', int(os.environ['PORT']))
    st._config.set_option('server.address', '0.0.0.0')
    st._config.set_option('server.headless', True)