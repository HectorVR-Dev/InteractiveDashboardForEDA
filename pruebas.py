import oracledb
import streamlit as st
from src.utils import GenerateQuerys, convert_oracle_to_df

params = {
    "FROM": "ESTUDIANTES_DIRTY"
}
print(convert_oracle_to_df(params).head(2))