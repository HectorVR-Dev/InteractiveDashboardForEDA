import oracledb
import streamlit as st
from src.utils import GenerateQuerys, convert_oracle_to_df

params = {
    "SELECT": "PUNTAJE_ADMISION",
    "FROM": "ESTUDIANTES_CLEAR",
    "WHERE": "AVANCE_CARRERA > 50"
}
print(convert_oracle_to_df(params))