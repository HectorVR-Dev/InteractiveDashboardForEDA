import oracledb
import streamlit as st
from src.utils import GenerateQuerys, convert_oracle_to_df

query_singles = {
    "SELECT": "EC.COD_PLAN, CP.PLAN",
    "FROM": {
        "table": "ESTUDIANTES_CLEAR",
        "as": "EC"
    },
    "JOIN": {
        "table": "COD_PLAN",
        "as": "CP",
        "on": "COD_PLAN"
    },
    "GROUP BY": "EC.COD_PLAN"
}

query = GenerateQuerys(query_singles)
print(query)
print(convert_oracle_to_df(query_singles))
