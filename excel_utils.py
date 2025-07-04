import pandas as pd
import re
from typing import List, Dict, Any

EXCEL_PATH = 'capbudg.xls'
SHEET_NAME = 'CapBudgWS'

# Helper to load the sheet
_def_sheet_cache = None
def load_sheet():
    global _def_sheet_cache
    if _def_sheet_cache is not None:
        return _def_sheet_cache
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=None)
    _def_sheet_cache = df
    return df

def get_table_sections() -> List[Dict[str, Any]]:
    """
    Returns a list of dicts: {name: str, start: int, end: int}
    Each section is a 'table' separated by a header row (all caps, not NaN) and blank rows.
    """
    df = load_sheet()
    sections = []
    current = None
    for idx, row in df.iterrows():
        first_cell = str(row[0]) if not pd.isna(row[0]) else ''
        # Table header: all uppercase, not empty, not just NaN
        if first_cell.isupper() and first_cell.strip():
            if current:
                current['end'] = idx - 1
                sections.append(current)
            current = {'name': first_cell.strip(), 'start': idx + 1, 'end': None}
        # Blank row: marks end of section
        elif first_cell.strip() == '' and current and current['end'] is None:
            current['end'] = idx - 1
            sections.append(current)
            current = None
    # If last section goes to end
    if current and current['end'] is None:
        current['end'] = len(df) - 1
        sections.append(current)
    return sections

def list_tables() -> List[str]:
    return [s['name'] for s in get_table_sections()]

def get_table_rows(table_name: str) -> List[str]:
    sections = get_table_sections()
    for s in sections:
        if s['name'] == table_name:
            df = load_sheet().iloc[s['start']:s['end']+1]
            # Row names are first column, non-empty, not all caps
            row_names = [str(r[0]) for _, r in df.iterrows() if str(r[0]).strip() and not str(r[0]).isupper()]
            return row_names
    raise ValueError(f"Table '{table_name}' not found.")

def get_row_sum(table_name: str, row_name: str) -> float:
    sections = get_table_sections()
    for s in sections:
        if s['name'] == table_name:
            df = load_sheet().iloc[s['start']:s['end']+1]
            for _, r in df.iterrows():
                if str(r[0]).strip() == row_name.strip():
                    # Sum all numeric values in the row (ignore NaN, strings, etc.)
                    vals = []
                    for v in r[1:]:
                        if pd.isna(v):
                            continue
                        # Remove % and try to convert
                        if isinstance(v, str):
                            v = v.replace('%', '')
                        try:
                            vals.append(float(v))
                        except Exception:
                            continue
                    return sum(vals)
            raise ValueError(f"Row '{row_name}' not found in table '{table_name}'.")
    raise ValueError(f"Table '{table_name}' not found.") 