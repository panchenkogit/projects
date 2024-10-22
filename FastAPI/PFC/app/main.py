from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
async def main_page():
    try:
        with open("frontend/page/main_page.html", 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")
    
@app.get('/products')
async def get_all_product():
    
    return all_product
