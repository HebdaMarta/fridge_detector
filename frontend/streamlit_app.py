import streamlit as st
import requests

with open("frontend/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.set_page_config(
    page_title="AI Fridge Chef",
    page_icon="🥗",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at top left,
            #dbeafe,
            transparent 30%
        ),
        radial-gradient(
            circle at top right,
            #dcfce7,
            transparent 30%
        ),
        #f8fafc;
}

.block-container {
    padding-top: 2rem;
}

.stButton > button {
    width: 100%;
    border-radius: 16px;
    height: 55px;
    font-size: 18px;
    font-weight: 600;
}

.product-card {
    padding: 12px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534;
    margin: 5px;
    display: inline-block;
    font-weight: 600;
}

.inventory-card {
    padding: 15px;
    border-radius: 15px;
    background: white;
    border: 1px solid #e2e8f0;
    box-shadow:
        0 4px 12px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div style="
padding:30px;
border-radius:25px;
background:linear-gradient(
135deg,
#22c55e,
#3b82f6
);
color:white;
margin-bottom:25px;
">

<h1>🥗 AI Fridge Chef</h1>

<p style="font-size:20px;">
Turn your fridge into personalized recipes using AI
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.recipe-card {
    background: white;
    border-radius: 24px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
    height: 100%;
    transition: 0.2s;
}

.recipe-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.12);
}

.recipe-time {
    display:inline-block;
    background:#eff6ff;
    color:#2563eb;
    padding:6px 12px;
    border-radius:999px;
    font-size:14px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)


inventory = st.session_state.get("inventory")

if inventory is not None:

    confirmed_products = inventory.get(
        "confirmed_products",
        []
    )

    possible_products = inventory.get(
        "possible_products",
        []
    )

if "uploaded_image" not in st.session_state:
    st.session_state["uploaded_image"] = None

if st.session_state.get("inventory") is None:

    image = st.file_uploader(
        "Upload fridge photo",
        type=["jpg", "jpeg", "png"]
    )

else:

    image = st.session_state["uploaded_image"]


if st.button("🔍 Analyze Fridge"):

    if image is None:

        st.warning(
            "Please upload an image first."
        )

    else:

        with st.spinner(
            "Analyzing fridge..."
        ):

            response = requests.post(
                "http://localhost:8000/recipe",
                files={
                    "image": (
                        image.name,
                        image.getvalue(),
                        image.type
                    )
                },
                data={
                    "preference": ""
                }
            )

        if response.status_code != 200:

            st.error(
                f"Backend error: {response.status_code}"
            )

            st.text(response.text)

        else:

            st.session_state["inventory"] = response.json()
            st.session_state["uploaded_image"] = image

            st.success(
                "Fridge analyzed successfully!"
            )

            st.rerun()


if "inventory" in st.session_state:

    inventory = st.session_state["inventory"]

    confirmed_products = inventory.get(
        "confirmed_products",
        []
    )

    possible_products = inventory.get(
        "possible_products",
        []
    )

    st.progress(33)

    st.divider()

    left, right = st.columns(
        [1, 1]
    )

    selected_products = []


    with left:

        if image is not None:

            st.markdown(
                "## 📸 Uploaded Fridge"
            )

            st.image(
                image,
                width="stretch"
            )


    with right:

        st.markdown(
            "### 🟢 Confirmed Products"
        )

        for product in confirmed_products:

            label = (
                f"{product['name']} "
                f"({product['quantity']})"
            )

            checked = st.checkbox(
                label,
                value=True,
                key=f"confirmed_{product['name']}"
            )

            if checked:

                selected_products.append(
                    product["name"]
                )

        st.markdown(
            "### 🟡 Review These Products"
        )

        for product in possible_products:

            label = (
                f"{product['name']} "
                f"({product['quantity']})"
            )

            checked = st.checkbox(
                label,
                value=False,
                key=f"possible_{product['name']}"
            )

            if checked:

                selected_products.append(
                    product["name"]
                )

    st.session_state[
        "selected_products"
    ] = selected_products

    st.divider()

    st.progress(66)

    st.markdown("### Selected ingredients")
    html = ""

    for product in selected_products:
        html += f"""
        <span class="product-card">
            {product}
        </span>
        """

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ## 🍽 Recipe Preferences
    
        Tell the AI what kind of meal you want.
        """
    )

    preference = st.text_area(
        "",
        height=180,
        placeholder="""
    Examples:

    • Healthy dinner

    • Vegetarian recipe

    • High protein meal

    • Quick lunch

    • Italian cuisine
    """
    )

    if st.button("🍳 Generate Recipes"):

        with st.spinner(
                "AI is preparing recipes..."
        ):

            response = requests.post(
                "http://localhost:8000/generate_recipes",
                json={
                    "products": selected_products,
                    "preference": preference
                }
            )

        if response.status_code != 200:

            st.error(
                f"Backend error: {response.status_code}"
            )

            st.text(response.text)

        else:

            st.session_state["recipes"] = response.json()

            st.session_state.pop(
                "chosen_recipe",
                None
            )

            st.rerun()

    if "recipes" in st.session_state:

        recipes = st.session_state["recipes"]["recipes"]

        st.divider()

        st.markdown(
            "# 🍽 Recipe Suggestions"
        )

        cols = st.columns(3)

        for idx, recipe in enumerate(recipes):

            with cols[idx]:

                selected = (
                        "chosen_recipe" in st.session_state
                        and
                        st.session_state["chosen_recipe"]["title"]
                        == recipe["title"]
                )

                card_class = "recipe-card"

                if "chosen_recipe" in st.session_state:

                    if selected:

                        card_class += " recipe-card-selected"

                    else:

                        card_class += " recipe-card-faded"

                st.markdown(
                    f"""
                    <div class="{card_class}">

                    <h3>
                    🍽 {recipe["title"]}
                    </h3>

                    <div class="recipe-time">
                    ⏱ {recipe["time"]}
                    </div>

                    <br><br>

                    {recipe["description"]}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                        "✨ Select",
                        key=f"recipe_{idx}"
                ):
                    st.session_state["chosen_recipe"] = recipe
                    st.rerun()


        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(
            [2, 1, 2]
        )

        with c2:
            st.markdown(
                """
                <center>
                <h3>
                🤔 None of these recipes look good?
                </h3>
                </center>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                    "✨ Generate 3 New Recipes",
                    use_container_width=True
            ):
                st.session_state.pop(
                    "recipes",
                    None
                )

                st.session_state.pop(
                    "chosen_recipe",
                    None
                )

                st.rerun()
