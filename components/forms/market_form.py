import streamlit as st
from constants.labels import FIELD_MARKET_EXISTING, FIELD_MARKET_NEW, BTN_SAVE_MARKET, CHECKBOX_USE_EXISTING_MARKET
from components.forms.config.market_inputs import MARKET_FORM_INPUTS
from constants.schema.columns import COL_DATE, COL_NUMBER_OF_OFFERS, COL_NOTES

def market_form(existing_markets: list[str]):
    # ✅ Si des marchés existent, on propose de choisir entre existant et nouveau
    show_checkbox = len(existing_markets) > 0
    use_existing = True if show_checkbox else False  # ✅ Par défaut coché seulement si utile

    if show_checkbox:
        use_existing = st.checkbox(CHECKBOX_USE_EXISTING_MARKET, value=True)

    with st.form("market_form", clear_on_submit=True):
        if use_existing:
            market = st.selectbox(FIELD_MARKET_EXISTING, options=[""] + existing_markets, key="selected_market")
            new_market = None
        else:
            market = None
            new_market = st.text_input(FIELD_MARKET_NEW, key="new_market")

        final_market = new_market.strip() if new_market else (market if market else "")

        cols = st.columns(3)
        form_values = {}
        for input in MARKET_FORM_INPUTS:
            key = input["key"]
            label = input["label"]
            col_index = input.get("col", 1) - 1
            with cols[col_index]:
                if input["type"] == "text":
                    form_values[key] = st.text_input(label, key=key)
                elif input["type"] == "number":
                    form_values[key] = st.number_input(label, min_value=0, step=1, key=key)
                elif input["type"] == "date":
                    form_values[key] = st.date_input(label, key=key, format="DD/MM/YYYY")

        submitted = st.form_submit_button(BTN_SAVE_MARKET)

        return submitted, final_market, form_values.get(COL_DATE), form_values.get(COL_NUMBER_OF_OFFERS), form_values.get(COL_NOTES)