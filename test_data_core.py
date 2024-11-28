import pytest
import pandas as pd
import numpy as np
from data_sources import local_data

# Define a fixture that sets up the DataFrame
@pytest.fixture
def df():
    return local_data("SELECT TOP 1000 * FROM aProperties_Tasaciones;")

# check if column exist
def test_col_exists(df):
    name = "valor"
    assert name in df.columns, f"Column '{name}' does not exist in the DataFrame"

# check for nulls
def test_null_check(df):
    name = "valor"
    assert np.where(df[name].isnull())

#chach values are unique
def test_unique_check(df):
    name = "property"
    assert pd.Series(df[name]).is_unique, f"Column '{name}' have repeated values"
