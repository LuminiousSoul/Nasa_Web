# import pandas as pd
# import streamlit as st
# from collections import Counter
# import re
# import matplotlib.pyplot as plt

# # ------------------------------
# # Load dataset
# # ------------------------------
# file_path = r"C:\Users\HP\Desktop\Nasa\space_bio_kg\data\SB_publications\SB_publication_PMC.csv"
# df = pd.read_csv(file_path)

# # Make sure columns are standardized
# df.columns = [c.strip() for c in df.columns]

# # ------------------------------
# # Streamlit page setup
# # ------------------------------
# st.set_page_config(page_title="NASA Space Biology Knowledge Engine", page_icon="🥱", layout="wide")

# st.title("🚀 NASA Space Biology Knowledge Engine")
# st.markdown("Search through **608 open-access Space Biology publications**")

# # ------------------------------
# # Sidebar filters
# # ------------------------------
# st.sidebar.header("🔍 Filters")

# # Keyword input
# query = st.sidebar.text_input("Search keyword:", "")

# # Year filter (if year column exists, otherwise skip)
# year_col = None
# for col in df.columns:
#     if "year" in col.lower():
#         year_col = col
#         break

# if year_col:
#     min_year = int(df[year_col].min())
#     max_year = int(df[year_col].max())
#     year_range = st.sidebar.slider("Filter by Year", min_year, max_year, (min_year, max_year))
#     df_filtered = df[(df[year_col] >= year_range[0]) & (df[year_col] <= year_range[1])]
# else:
#     df_filtered = df.copy()

# # ------------------------------
# # Keyword search
# # ------------------------------
# if query:
#     results = df_filtered[df_filtered['Title'].str.contains(query, case=False, na=False)]
# else:
#     results = df_filtered.copy()

# st.subheader(f"📄 Search Results ({len(results)})")
# if results.empty:
#     st.warning("No results found.")
# else:
#     for _, row in results.head(20).iterrows():  # show only first 20
#         st.markdown(f"- **{row['Title']}**  \n  [Read Paper]({row['Link']})")

# # ------------------------------
# # Keyword frequency analysis
# # ------------------------------
# st.subheader("📊 Keyword Trends in Results")

# if not results.empty:
#     text = " ".join(results['Title']).lower()
#     words = re.findall(r'\b[a-z]+\b', text)

#     stopwords = {
#         "of", "the", "and", "in", "for", "to", "on", "a", "an", "with", "by", "at", 
#         "from", "into", "during", "after", "effect", "effects", "study", "studies"
#     }
#     filtered = [w for w in words if w not in stopwords]

#     common = Counter(filtered).most_common(10)

#     if common:
#         keywords, counts = zip(*common)
#         fig, ax = plt.subplots()
#         ax.barh(keywords[::-1], counts[::-1], color="skyblue")
#         ax.set_xlabel("Frequency")
#         ax.set_ylabel("Keyword")
#         ax.set_title("Top Keywords in Selected Papers")
#         st.pyplot(fig)
#     else:
#         st.info("Not enough words to generate keyword chart.")
import pandas as pd
import streamlit as st
from collections import Counter
import re
import matplotlib.pyplot as plt

# ------------------------------
# Load dataset
# ------------------------------
file_path = r"C:\Users\HP\Desktop\Nasa\space_bio_kg\data\SB_publications\SB_publication_PMC.csv"
df = pd.read_csv(file_path)

# Standardize columns
df.columns = [c.strip() for c in df.columns]

# ------------------------------
# Summarization function (naive but works for titles/abstracts)
# ------------------------------
def make_summary(text: str) -> str:
    words = text.split()
    if len(words) <= 15:
        return text
    return " ".join(words[:12]) + " ..."

# ------------------------------
# Streamlit page setup
# ------------------------------
st.set_page_config(page_title="NASA Space Biology Knowledge Engine", page_icon="🚀", layout="wide")

st.title("🚀 NASA Space Biology Knowledge Engine")
st.markdown("Search through **608 open-access Space Biology publications**")

# ------------------------------
# Sidebar: Filters
# ------------------------------
st.sidebar.header("⚙️ Controls")

audience = st.sidebar.radio(
    "Select Audience Mode:",
    ["Scientist 👩‍🔬", "Manager 💼", "Mission Architect 🚀"],
    index=0
)

query = st.sidebar.text_input("Search keyword:", "")

# ------------------------------
# Search results
# ------------------------------
if query:
    results = df[df['Title'].str.contains(query, case=False, na=False)]
else:
    results = df.copy()

st.subheader(f"📄 Results for '{query}' ({len(results)})")

if results.empty:
    st.warning("No results found.")
else:
    if audience == "Scientist 👩‍🔬":
        st.info("Mode: Scientist → Showing short paper summaries (knowledge distillation).")
        for _, row in results.head(15).iterrows():
            summary = make_summary(row['Title'])
            st.markdown(f"**{summary}**  \n[Read Paper]({row['Link']})")

    elif audience == "Manager 💼":
        st.info("Mode: Manager → Showing research trends & counts.")
        text = " ".join(results['Title']).lower()
        words = re.findall(r'\b[a-z]+\b', text)
        stopwords = {
            "of", "the", "and", "in", "for", "to", "on", "a", "an", "with", "by", "at",
            "from", "into", "during", "after", "effect", "effects", "study", "studies"
        }
        filtered = [w for w in words if w not in stopwords]
        common = Counter(filtered).most_common(10)
        if common:
            keywords, counts = zip(*common)
            fig, ax = plt.subplots()
            ax.barh(keywords[::-1], counts[::-1], color="orange")
            ax.set_xlabel("Frequency")
            ax.set_ylabel("Keyword")
            ax.set_title("Top Keywords in Selected Papers")
            st.pyplot(fig)

    elif audience == "Mission Architect 🚀":
        st.info("Mode: Mission Architect → Highlighting risk-related keywords.")
        risk_words = ["radiation", "immune", "bone", "muscle", "microgravity", "health", "stress"]
        for _, row in results.head(20).iterrows():
            title = row['Title']
            highlighted = title
            for rw in risk_words:
                highlighted = re.sub(f"({rw})", r"**\1**", highlighted, flags=re.IGNORECASE)
            st.markdown(f"- {highlighted}  \n  [Read Paper]({row['Link']})")
