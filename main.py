from fastapi import FastAPI 
 
app = FastAPI() 
 
@app.post("/api/v1/assess") 
async def assess(): 
    return {"message": "Assessment successful", "data": None} 
@app.get("/api/v1/assess") 
async def assess_get(): 
    return {"message": "GET works"} 
