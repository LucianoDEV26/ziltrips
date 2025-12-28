import streamlit as st
from fpdf import FPDF
from io import BytesIO
import urllib.parse

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="ZilTrips - Smart Travel for Brazil",
    layout="centered"
)

# --------------------------------------------------
# SESSION MEMORY (MVP FREEZE)
# --------------------------------------------------
defaults = {
    "origin": "New York",
    "state": "Rio de Janeiro",
    "city": "Búzios",
    "style": "Beach",
    "days": 5
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --------------------------------------------------
# DATA
# --------------------------------------------------
TRAVEL_STYLES = [
    "Beach",
    "Nature / Ecotourism",
    "Cultural / Historic",
    "Nightlife / Events",
    "Relax / Wellness",
    "Urban / Business",
    "Backpacker / Budget"
]

BRAZIL_DESTINATIONS = {
    "Rio de Janeiro": {
        "capital": "Rio de Janeiro",
        "cities": {
            "Búzios": ["Beach", "Relax"],
            "Arraial do Cabo": ["Beach", "Nature"],
            "Paraty": ["Cultural", "Nature"],
            "Angra dos Reis": ["Beach", "Nature"],
            "Ilha Grande": ["Beach", "Nature", "Backpacker"],
            "Cabo Frio": ["Beach"],
            "Petrópolis": ["Cultural"]
        }
    },
    "São Paulo": {
        "capital": "São Paulo",
        "cities": {
            "São Paulo": ["Urban", "Nightlife"],
            "Santos": ["Beach"],
            "Ubatuba": ["Beach", "Nature"],
            "Ilhabela": ["Beach", "Nature"],
            "Campos do Jordão": ["Relax", "Nature"]
        }
    },
    "Bahia": {
        "capital": "Salvador",
        "cities": {
            "Salvador": ["Cultural", "Beach", "Nightlife"],
            "Trancoso": ["Beach", "Relax"],
            "Porto Seguro": ["Beach", "Nightlife"],
            "Caraíva": ["Beach", "Backpacker"],
            "Itacaré": ["Beach", "Nature"]
        }
    }
}

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def safe_pdf_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

def q(text):
    return urllib.parse.quote(text)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("✈️ ZilTrips")
st.markdown("**Plan smarter. Share faster. Travel better.**")
st.caption("🔁 Your trip is saved automatically")

# --------------------------------------------------
# ORIGIN
# --------------------------------------------------
st.session_state.origin = st.text_input(
    "Origin city",
    st.session_state.origin
)

# --------------------------------------------------
# DESTINATION ENGINE
# --------------------------------------------------
st.subheader("Destination in Brazil")

state = st.selectbox(
    "State",
    list(BRAZIL_DESTINATIONS.keys()),
    index=list(BRAZIL_DESTINATIONS.keys()).index(st.session_state.state)
)
st.session_state.state = state

style = st.selectbox(
    "Travel style",
    TRAVEL_STYLES,
    index=TRAVEL_STYLES.index(st.session_state.style)
)
st.session_state.style = style

cities = BRAZIL_DESTINATIONS[state]["cities"]
filtered = [c for c, tags in cities.items() if style in tags] or list(cities.keys())

city = st.selectbox(
    "City",
    filtered,
    index=filtered.index(st.session_state.city) if st.session_state.city in filtered else 0
)
st.session_state.city = city

destination = f"{city}, {state}, Brazil"

# --------------------------------------------------
# DURATION
# --------------------------------------------------
st.session_state.days = st.number_input(
    "Trip duration (days)",
    min_value=1,
    value=st.session_state.days,
    step=1
)

# --------------------------------------------------
# ✈️ FLIGHTS (SMART)
# --------------------------------------------------
st.subheader("✈️ Recommended Flights")

st.markdown(f"""
- Google Flights: https://www.google.com/travel/flights?q={q(st.session_state.origin)}%20to%20{q(destination)}
- Skyscanner: https://www.skyscanner.com/transport/flights/
- FlightRadar24 (live context): https://www.flightradar24.com/
""")

# --------------------------------------------------
# 🏨 HOTELS (SMART)
# --------------------------------------------------
st.subheader("🏨 Recommended Stays")

st.markdown(f"""
- Google Hotels: https://www.google.com/travel/hotels/{q(destination)}
- Booking.com: https://www.booking.com/searchresults.html?ss={q(destination)}
- Trivago: https://www.trivago.com.br/?sQuery={q(destination)}
- Decolar: https://www.decolar.com/hotels/{q(destination)}
- Airbnb: https://www.airbnb.com.br/s/{q(destination)}/homes
""")

# --------------------------------------------------
# 📤 SHAREABLE SUMMARY
# --------------------------------------------------
st.subheader("📤 Share your trip")

summary = f"""
ZilTrips Travel Plan 🇧🇷

From: {st.session_state.origin}
To: {destination}
Style: {st.session_state.style}
Duration: {st.session_state.days} days

Planned with ZilTrips ✈️
"""

st.text_area("Copy & share", summary.strip(), height=160)

# --------------------------------------------------
# 📄 PDF EXPORT (MONETIZABLE LATER)
# --------------------------------------------------
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(180, 10, safe_pdf_text("ZilTrips - Travel Summary"))

    pdf.set_font("Arial", "", 12)
    pdf.ln(4)
    pdf.multi_cell(180, 8, safe_pdf_text(summary))

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

st.download_button(
    "📄 Download PDF",
    generate_pdf(),
    file_name="ZilTrips_Travel_Plan.pdf",
    mime="application/pdf"
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.success("ZilTrips MVP frozen. Ready to scale.")
