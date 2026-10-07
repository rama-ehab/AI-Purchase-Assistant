# FastAPI backend that connects all AI Purchase Assistant components.

from fastapi import FastAPI
import threading
import uvicorn

from .models import RecommendationRequest
from .scraper import scrape_products, structure_products
from .rag import create_product_retriever, retrieve_products
from .chains import (
    extract_requirements,
    evaluate_products,
    choose_best_product,
    generate_recommendation
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI Purchase Assistant API is running"
    }


@app.post("/recommend")
def recommend(request: RecommendationRequest):

    products = scrape_products(request.urls)

    structured_products = structure_products(products)

    retriever = create_product_retriever(products)

    requirements = extract_requirements(
        request.user_text
    )

    retrieved_docs, retrieved_products_text = retrieve_products(
        requirements,
        retriever
    )

    evaluated_products = evaluate_products(
        structured_products,
        requirements
    )

    best_product = choose_best_product(
        structured_products,
        requirements
    )

    clean_result = generate_recommendation(
        best_product,
        requirements
    )

    return {
        "recommendation": clean_result,
        "products": structured_products
    }


def run_server():

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )


server_thread = threading.Thread(
    target=run_server,
    daemon=True
)

server_thread.start()
print("FastAPI server started!")