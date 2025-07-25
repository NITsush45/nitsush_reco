from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.recommender import get_recommendations

app = FastAPI()

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend")
async def recommend(request: Request):
    body = await request.json()
    user_query = body.get("query")
    domain = body.get("domain")
    return get_recommendations(query=user_query, domain=domain)
