from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from excel_utils import list_tables, get_table_rows, get_row_sum

app = FastAPI(title="Excel Processor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/list_tables")
def api_list_tables():
    """List all table names present in the Excel sheet."""
    try:
        tables = list_tables()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_table_details")
def api_get_table_details(table_name: str = Query(..., description="Name of the table")):
    """Return the row names (first column values) for the selected table."""
    try:
        row_names = get_table_rows(table_name)
        return {"table_name": table_name, "row_names": row_names}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/row_sum")
def api_row_sum(
    table_name: str = Query(..., description="Name of the table"),
    row_name: str = Query(..., description="Name of the row")
):
    """Calculate and return the sum of all numerical data points in the specified row of the specified table."""
    try:
        s = get_row_sum(table_name, row_name)
        return {"table_name": table_name, "row_name": row_name, "sum": s}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 