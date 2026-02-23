from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

app = FastAPI(title="Table Generator")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Mount static files directory

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/static")
async def static_files():
    return {"message": "chipi"}







@app.get("/")
async def home(request: Request):
    """Render the home page with a sample table"""
    
    # Sample data for the table
    table_data = {
        "headers": ["ID", "Name", "Age", "Occupation"],
        "rows": [
            {"id": 1, "name": "John Doe", "age": 30, "occupation": "Developer"},
            {"id": 2, "name": "Jane Smith", "age": 25, "occupation": "Designer"},
            {"id": 3, "name": "Bob Johnson", "age": 35, "occupation": "Manager"},
            {"id": 4, "name": "Alice Williams", "age": 28, "occupation": "Engineer"}
        ]
    }
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "table_data": table_data}
    )

@app.get("/dynamic-table")
async def dynamic_table(request: Request, rows: int = 5, columns: int = 3):
    """Generate a dynamic table based on requested dimensions"""
    
    headers = [f"Column {i+1}" for i in range(columns)]
    rows_data = []
    
    for i in range(rows):
        row_data = {f"Column {j+1}": f"Data {i+1}-{j+1}" for j in range(columns)}
        row_data["id"] = str(i + 1)  # Convert to string to fix the linter error
        rows_data.append(row_data)
    
    table_data = {
        "headers": headers,
        "rows": rows_data
    }
    
    return templates.TemplateResponse(
        "dynamic_table.html",
        {"request": request, "table_data": table_data}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 