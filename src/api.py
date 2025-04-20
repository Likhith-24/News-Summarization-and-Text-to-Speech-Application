from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.utils import NewsAnalyzer
from src.config import logger

app = FastAPI(title="News Sentiment Analyzer", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

analyzer = NewsAnalyzer()

class CompanyRequest(BaseModel):
    company_name: str

@app.get("/test")  # Add a test endpoint to verify server
async def test_endpoint():
    logger.info("Test endpoint accessed")
    return {"status": "Server is running!"}

@app.post("/analyze")
async def analyze_sentiment(request: CompanyRequest):
    logger.info(f"Received POST request for company: {request.company_name}")
    try:
        report = analyzer.generate_report(request.company_name)
        if "error" in report:
            logger.error(f"Report generation failed: {report['error']}")
            raise HTTPException(status_code=500, detail=report["error"])
        logger.info(f"Successfully generated report for {request.company_name}")
        return report
    except Exception as e:
        logger.error(f"API error processing {request.company_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")