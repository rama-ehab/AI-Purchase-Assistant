# Handles embeddings, ChromaDB, and product retrieval.

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_product_retriever(products):

    documents = []

    for product in products:

        details_text = "\n".join(
            product["details"]
        )

        text = f"""
Product: {product["name"]}
Brand: {product["brand"]}
Current Price: {product["current_price"]} EGP
Original Price: {product["original_price"]} EGP
Discount: {product["discount_percentage"]}%
Available: {product["available"]}

Product Details:
{details_text}
"""

        documents.append(
            Document(
                page_content=text.strip(),
                metadata={
                    "name": product["name"],
                    "brand": product["brand"],
                    "price": product["current_price"],
                    "sku": product["sku"],
                    "url": product["url"]
                }
            )
        )

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        collection_name="products"
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever


def format_docs(docs):
    return "\n\n".join(
        doc.page_content for doc in docs
    )


def retrieve_products(requirements, retriever):

    retrieved_docs = retriever.invoke(
        str(requirements)
    )

    retrieved_products_text = format_docs(
        retrieved_docs
    )

    return retrieved_docs, retrieved_products_text