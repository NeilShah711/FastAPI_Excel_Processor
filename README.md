# FastAPI Excel Processor Assignment

## Overview
This FastAPI application reads and processes data from an Excel sheet (`capbudg.xls`) and exposes endpoints to interact with the data as described in the assignment.

## Setup Instructions

1. **Clone the repository and navigate to the project directory.**
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv_iris
   venv_iris\Scripts\activate  # On Windows
   # or
   source venv_iris/bin/activate  # On Unix/Mac
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   # or manually:
   pip install fastapi uvicorn pandas xlrd openpyxl
   ```
4. **Run the FastAPI app:**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 9090
   ```
5. **Base URL:**
   - http://localhost:9090

## API Endpoints

### 1. `GET /list_tables`
- **Description:** List all table names present in the Excel sheet.
- **Response Example:**
  ```json
  {
    "tables": ["INITIAL INVESTMENT", "WORKING CAPITAL", "GROWTH RATES", ...]
  }
  ```

### 2. `GET /get_table_details?table_name=...`
- **Description:** Return the row names (first column values) for the selected table.
- **Response Example:**
  ```json
  {
    "table_name": "INITIAL INVESTMENT",
    "row_names": [
      "Initial Investment=",
      "Opportunity cost (if any)=",
      ...
    ]
  }
  ```

### 3. `GET /row_sum?table_name=...&row_name=...`
- **Description:** Calculate and return the sum of all numerical data points in the specified row of the specified table.
- **Response Example:**
  ```json
  {
    "table_name": "INITIAL INVESTMENT",
    "row_name": "Tax Credit (if any )=",
    "sum": 10.0
  }
  ```
- **Note:** Only numerical values are summed. If a value contains a '%', the '%' is ignored and the number is summed as a float.

## Error Handling
- Returns 404 if the table or row is not found.
- Returns 500 for internal errors or Excel file issues.

## Potential Improvements
- Support for multiple Excel files or user-uploaded files.
- More robust table detection (e.g., named ranges, user-defined delimiters).
- Support for `.xlsx` and other formats.
- Advanced data operations: filtering, aggregation, exporting results.
- UI integration for easier interaction.

## Missed Edge Cases
- Empty Excel files or sections.
- Tables with no numerical data (sum will be 0).
- Malformed or misspelled table/row names (returns 404).
- Rows with mixed data types (non-numeric ignored).
- If a table header is not all uppercase, it may not be detected as a table.

## Testing
- Use the included Postman collection (`postman_collection.json`) to test all endpoints.
- Or, use the interactive docs at `http://localhost:9090/docs` after starting the server. 