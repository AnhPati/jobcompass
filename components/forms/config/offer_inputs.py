from constants.labels import *
from constants.schema.columns import *
from constants.labels import RHYTHM_OPTIONS

BASE_FORM_INPUTS = [
    {"key": COL_MARKET, "label": FIELD_MARKET, "type": "select", "required": True},
    {"key": COL_TJM, "label": FIELD_TJM, "type": "text"},
    {"key": COL_SENIORITY, "label": FIELD_SENIORITY, "type": "text"},
    {"key": COL_TECHS_MAIN, "label": FIELD_TECH_MAIN, "type": "text"},
    {"key": COL_TECHS_SECONDARY, "label": FIELD_TECH_SECONDARY, "type": "text"},
    {"key": COL_SKILLS_MAIN, "label": FIELD_SKILLS_MAIN, "type": "text"},
    {"key": COL_SKILLS_SECONDARY, "label": FIELD_SKILLS_SECONDARY, "type": "text"},
    {"key": COL_SECTOR, "label": FIELD_SECTOR, "type": "text"},
    {"key": COL_LOCATION, "label": FIELD_LOCATION, "type": "text"},
    {"key": COL_RHYTHM, "label": FIELD_RHYTHM, "type": "select", "options": RHYTHM_OPTIONS},
    {"key": COL_COMPANY, "label": FIELD_COMPANY, "type": "text"},
    {"key": COL_CONTACT, "label": FIELD_CONTACT, "type": "text"},
]

OFFER_EXTRA_INPUTS = [
    {"key": COL_TITLE, "label": FIELD_TITLE, "type": "text", "required": True},
    {"key": COL_JOB_TITLE, "label": FIELD_JOB_TITLE, "type": "text"},
    {"key": COL_LINK, "label": FIELD_LINK, "type": "text", "required": True},
]

CONTACT_EXTRA_INPUTS = [
    {"key": COL_SOPHISTICATION, "label": FIELD_SOPHISTICATION, "type": "slider", "min": 1, "max": 5, "default": 3},
    {"key": COL_RELIABILITY, "label": FIELD_RELIABILITY, "type": "slider", "min": 1, "max": 5, "default": 3},
]