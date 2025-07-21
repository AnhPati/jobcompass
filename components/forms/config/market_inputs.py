from constants.labels import FIELD_DATE, FIELD_NUMBER_OF_OFFERS, FIELD_NOTES
from constants.schema.columns import COL_DATE, COL_NUMBER_OF_OFFERS, COL_NOTES

MARKET_FORM_INPUTS = [
    {"key": COL_DATE, "label": FIELD_DATE, "type": "date", "col": 1},
    {"key": COL_NUMBER_OF_OFFERS, "label": FIELD_NUMBER_OF_OFFERS, "type": "number", "col": 2},
    {"key": COL_NOTES, "label": FIELD_NOTES, "type": "text", "col": 3},
]