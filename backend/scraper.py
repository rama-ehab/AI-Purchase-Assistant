# Scrapes product information from product URLs.

import requests
from bs4 import BeautifulSoup
import json
import re

def clean_product_section(section):
    lines = [
        line.strip()
        for line in section.get_text("\n", strip=True).splitlines()
        if line.strip()
    ]

    # Common UI / placeholder text
    noise = {
        "نص هيكلي",
        "Skeleton text",
        "تجاوز إلى معلومات المنتج",
        "Skip to product information",
        "سعر الوحدة",
        "Unit price",
        "الكمية",
        "Quantity",
        "Add to basket",
        "إضافة إلى السلة",
        "معلومات إضافية",
        "Additional Information",
    }

    cleaned = []

    for line in lines:

        # Remove UI text
        if line in noise:
            continue

        # Remove review count such as "(1)"
        if re.fullmatch(r"\(\d+\)", line):
            continue

        # Remove discount percentage such as "-17%"
        if re.fullmatch(r"-\d+%", line):
            continue

        cleaned.append(line)

    # Remove consecutive duplicates
    final_lines = []

    for line in cleaned:
        if final_lines and line == final_lines[-1]:
            continue

        final_lines.append(line)

    # Remove trailing internal UI value
    if len(final_lines) >= 2:

        if (
            final_lines[-2] in {"اللون", "Color"}
            and re.fullmatch(r"\d+", final_lines[-1])
        ):
            final_lines = final_lines[:-2]

    return final_lines


def scrape_product(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # --------------------------------------------------
    # Product name
    # --------------------------------------------------

    name_tag = soup.find(
        "h1",
        class_=lambda x: x and "product-title" in x
    )

    if not name_tag:
        raise ValueError("Product name not found")

    name = name_tag.get_text(" ", strip=True)

    # --------------------------------------------------
    # Brand
    # --------------------------------------------------

    vendor = soup.find(
        class_=lambda x: x and "product-info__vendor" in x
    )

    brand = (
        vendor.get_text(" ", strip=True)
        if vendor
        else None
    )

    # --------------------------------------------------
    # Product JSON
    # --------------------------------------------------

    product_data = None

    for script in soup.find_all(
        "script",
        type="application/json"
    ):

        text = script.get_text(strip=True)

        if '"price":' in text and '"compare_at_price":' in text:

            try:
                data = json.loads(text)

                if (
                    "price" in data
                    and "compare_at_price" in data
                ):
                    product_data = data
                    break

            except json.JSONDecodeError:
                continue

    if not product_data:
        raise ValueError(
            "Product price information not found"
        )

    # --------------------------------------------------
    # Price
    # --------------------------------------------------

    current_price = product_data["price"] / 100

    original_price = product_data.get(
        "compare_at_price"
    )

    if original_price:
        original_price = original_price / 100

    # --------------------------------------------------
    # Discount
    # --------------------------------------------------

    discount_amount = None
    discount_percentage = None

    if (
        original_price
        and original_price > current_price
    ):

        discount_amount = (
            original_price - current_price
        )

        discount_percentage = round(
            (
                discount_amount
                / original_price
            ) * 100,
            2
        )

    # --------------------------------------------------
    # SKU & availability
    # --------------------------------------------------

    sku = product_data.get("sku")

    available = product_data.get(
        "available"
    )

    # --------------------------------------------------
    # Dynamic product information
    # --------------------------------------------------

    product_section = soup.find(
        id="QuickViewContainer"
    )

    details = []

    if product_section:

        details = clean_product_section(
            product_section
        )

    # --------------------------------------------------
    # Return product
    # --------------------------------------------------

    return {
        "name": name,
        "brand": brand,
        "current_price": current_price,
        "original_price": original_price,
        "discount_amount": discount_amount,
        "discount_percentage": discount_percentage,
        "sku": sku,
        "available": available,
        "details": details,
        "url": url
    }


def scrape_products(urls):

    products = []

    for url in urls:

        try:
            product = scrape_product(url)
            products.append(product)

            print("✓", product["name"])

        except Exception as e:
            print("✗ Error:", e)

    return products


def structure_products(products):

    structured_products = []

    for product in products:

        details = product["details"]

        product_info = {
            "name": product["name"],
            "price": product["current_price"],
            "ram": None,
            "storage": None,
            "processor": None,
            "graphics": None,
            "display": None,
            "available": product["available"],
            "url": product["url"]
        }

        for i, detail in enumerate(details):

            if detail in ["RAM:", "Memory Ram:"]:
                product_info["ram"] = details[i + 1]

            elif detail == "Storage:":
                product_info["storage"] = details[i + 1]

            elif detail == "Prosessor:":
                product_info["processor"] = details[i + 1]

            elif detail == "Graphics:":
                product_info["graphics"] = details[i + 1]

            elif detail == "Display:":
                product_info["display"] = details[i + 1]

        structured_products.append(product_info)

    return structured_products