import streamlit as st
import requests

API_URL = "https://huskiness-antiques-theatrics.ngrok-free.dev"

st.set_page_config(
    page_title="AI Purchase Assistant",
    page_icon="💻"
)

st.title("💻 AI Purchase Assistant")

st.write(
    "Find the best laptop based on your needs, budget, and priorities."
)

st.caption(
    "Enter your requirements and add up to 3 product URLs. "
    "The AI will analyze and compare them for you."
)

st.subheader("📝 Your Requirements")

user_text = st.text_area(
    "Describe what you need",
    placeholder=(
        "Example:\n"
        "I need a laptop for gaming and programming.\n"
        "My budget is 85000 EGP.\n"
        "I want at least 16GB RAM and a good GPU.\n"
        "Battery life is also important."
    ),
    height=150
)

st.subheader("🔗 Products to Compare")

st.caption(
    "Paste up to 3 product URLs from the same or different stores."
)

url1 = st.text_input(
    "Product URL 1",
    placeholder="https://example.com/product-1"
)

url2 = st.text_input(
    "Product URL 2",
    placeholder="https://example.com/product-2"
)

url3 = st.text_input(
    "Product URL 3",
    placeholder="https://example.com/product-3"
)

if st.button(
    "🔍 Find Best Laptop",
    use_container_width=True
):

    urls = [
        url for url in [url1, url2, url3]
        if url.strip()
    ]

    if not user_text.strip():
        st.warning("Please describe what you are looking for.")

    elif not urls:
        st.warning("Please provide at least one product URL.")

    else:

        with st.spinner(
            "🔎 Scraping products and analyzing your requirements..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/recommend",
                    json={
                        "user_text": user_text,
                        "urls": urls
                    },
                    headers={
                        "ngrok-skip-browser-warning": "true"
                    },
                    timeout=300
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ The request took too long. Please try again."
                )

                st.stop()

            except requests.exceptions.RequestException:

                st.error(
                    "🔌 Could not connect to the AI service. "
                    "Please make sure the backend is running."
                )

                st.stop()

        if response.status_code == 200:
            result = response.json()

            st.session_state["recommendation"] = result["recommendation"]
            st.session_state["products"] = result["products"]

            recommendation = result["recommendation"]
            products = result["products"]

            lines = recommendation.splitlines()

            recommendation_text = ""
            reason_text = ""

            for line in lines:
                if line.startswith("Recommendation:"):
                    recommendation_text = line.replace(
                        "Recommendation:", ""
                    ).strip()

                elif line.startswith("Reason:"):
                    reason_text = line.replace(
                        "Reason:", ""
                    ).strip()

            st.subheader("🏆 Recommended Laptop")

            st.success(
                f"**{recommendation_text}**"
            )

            st.subheader("💡 Why this laptop?")

            st.info(
                reason_text
            )
            st.divider()


        else:

            st.error(
                f"⚠️ Something went wrong while analyzing the products."
            )

            st.caption(
                f"API Error: {response.status_code}"
            )

if "products" in st.session_state:

    if st.button(
        "📊 Compare Products",
        use_container_width=True
    ):

        st.subheader("📊 Product Comparison")

        st.caption(
            "Compare the specifications and prices of all analyzed products."
        )

        products = st.session_state["products"]
        recommendation = st.session_state["recommendation"]

        # Get recommended product name
        recommended_product = None

        for product in products:
            if product["name"] in recommendation:
                recommended_product = product
                break

        # Put recommended product first
        if recommended_product:
            products = [
                recommended_product
            ] + [
                product
                for product in products
                if product != recommended_product
            ]

        comparison_data = []

        for product in products:
            comparison_data.append({
            "Product": product["name"],
            "Price (EGP)": f"{product['price']:,.0f}",
            "RAM": product["ram"],
            "Storage": product["storage"],
            "Processor": product["processor"],
            "Graphics": product["graphics"],
            "Display": product["display"],
            "Available": "Yes" if product["available"] else "No"
        })

        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True
        )