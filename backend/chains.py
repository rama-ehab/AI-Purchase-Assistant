# Handles the LLM, chains, requirements extraction, and recommendations.

import re

from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import PydanticOutputParser

from .models import UserRequirements, ProductEvaluation

generator = pipeline(
    "text-generation",
    model="Qwen/Qwen3-4B",
    device=0,
    max_new_tokens=600,
    do_sample=False,
    repetition_penalty=1.1,
    return_full_text=False
)

llm = HuggingFacePipeline(pipeline=generator)

requirements_parser = PydanticOutputParser(
    pydantic_object=UserRequirements
)

requirements_prompt = PromptTemplate.from_template("""
You are a laptop purchase assistant.

Read the user's message and extract their laptop requirements.

Return ONLY a JSON object with exactly these four fields:

{{
    "budget": number or null,
    "usage": ["purpose1", "purpose2"],
    "min_ram": number or null,
    "priorities": ["priority1", "priority2"]
}}

Rules:
- If the user does not mention a budget, use null.
- If the user does not mention minimum RAM, use null.
- Only include information that the user actually provided.
- Do not explain your answer.
- Do not return the schema.
- Return the actual values from the user's message.

User message:
{user_input}

JSON:
""")

requirements_chain = (
    {
        "user_input": RunnablePassthrough()
    }
    | requirements_prompt
    | llm
    | requirements_parser
)

def extract_requirements(user_text):

    requirements = requirements_chain.invoke(user_text)

    return requirements


def evaluate_products(products, requirements):

    evaluated_products = []

    budget = requirements.budget
    min_ram = requirements.min_ram

    for product in products:

        price = product["price"]

        if budget is not None:
            budget_match = (
                "Yes"
                if price <= budget
                else "No"
            )
        else:
            budget_match = "Not specified"

        ram_value = None

        if product["ram"]:
            ram_match_number = re.search(
                r"\d+",
                str(product["ram"])
            )

            if ram_match_number:
                ram_value = int(
                    ram_match_number.group()
                )

        if min_ram is not None and ram_value is not None:
            ram_match = (
                "Yes"
                if ram_value >= min_ram
                else "No"
            )
        else:
            ram_match = "Not specified"

        graphics = str(product["graphics"])

        if "RTX 5060" in graphics:
            gaming_suitability = "Yes"
        else:
            gaming_suitability = "Unknown"

        result = ProductEvaluation(
            product=product["name"],
            budget_match=budget_match,
            ram_match=ram_match,
            gaming_suitability=gaming_suitability
        )

        evaluated_products.append(result)

    return evaluated_products


def choose_best_product(products, requirements):

    budget = requirements.budget
    min_ram = requirements.min_ram

    valid_products = []

    for product in products:

        # Check budget
        if budget is not None and product["price"] > budget:
            continue

        # Check RAM
        ram_value = None

        if product["ram"]:
            match = re.search(
                r"\d+",
                str(product["ram"])
            )

            if match:
                ram_value = int(match.group())

        if (
            min_ram is not None
            and ram_value is not None
            and ram_value < min_ram
        ):
            continue

        valid_products.append(product)

    # No product satisfies the hard requirements
    if not valid_products:
        return None

    # Score the products that passed the hard requirements
    def score_product(product):

        score = 0

        graphics = str(
            product["graphics"]
        ).lower()

        usage = [
            item.lower()
            for item in requirements.usage
        ]

        priorities = [
            item.lower()
            for item in requirements.priorities
        ]

        # Gaming
        if "gaming" in usage:

            if "rtx" in graphics:
                score += 5

            elif "arc" in graphics:
                score += 3

        # Good GPU priority
        if any(
            "gpu" in item or "graphics" in item
            for item in priorities
        ):

            if "rtx" in graphics:
                score += 5

            elif "arc" in graphics:
                score += 3

        # Programming
        if "programming" in usage:
            score += 2

        # More RAM
        if product["ram"]:

            match = re.search(
                r"\d+",
                str(product["ram"])
            )

            if match:
                ram_value = int(match.group())
                score += ram_value / 16

        return score

    best_product = max(
        valid_products,
        key=score_product
    )

    return best_product


def generate_recommendation(
    best_product,
    requirements
):

    if best_product is None:

        return (
            "Recommendation: No suitable laptop found.\n"
            "Reason: None of the provided laptops meet "
            "your budget and minimum requirements."
        )

    reasons = []

    # Budget
    if requirements.budget is not None:
        reasons.append(
            f"it fits your budget of "
            f"{requirements.budget:,.0f} EGP"
        )

    # RAM
    if requirements.min_ram is not None:
        reasons.append(
            f"it has {best_product['ram']} RAM"
        )

    # Usage
    if requirements.usage:
        usage_text = " and ".join(
            requirements.usage
        )

        reasons.append(
            f"it is suitable for {usage_text}"
        )

    # GPU priority
    if any(
        "gpu" in priority.lower()
        or "graphics" in priority.lower()
        for priority in requirements.priorities
    ):

        if best_product["graphics"]:
            reasons.append(
                f"it has {best_product['graphics']}"
            )

    reason_text = ", ".join(reasons)

    return (
        f"Recommendation: {best_product['name']}\n"
        f"Reason: I recommend this laptop because {reason_text}."
    )