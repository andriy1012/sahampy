import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh


symbols = {
    "Antam": "ANTM.JK",
    "Merdeka Gold Resources": "EMAS.JK",
    "Merdeka Copper Gold": "MDKA.JK",
    "Surya Semesta Internusa": "SSIA.JK",
    "GoTo": "GOTO.JK"
}

st.set_page_config(page_title="💰 Cust Saham Bearman", layout="wide")
st.title("💰💸 Harga Saham Indonesia (IDX)>>🏧🏧")

all_data = []

for name, symbol in symbols.items():
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")

    if not hist.empty:
        latest = hist.iloc[-1]
        all_data.append({
            "Nama": name,
            "Id": symbol,
            "Saat ini": round(latest["Close"], 2),
            "Open": round(latest["Open"], 2),
            "High": round(latest["High"], 2),
            "Low": round(latest["Low"], 2),
            "Vol": int(latest["Volume"])
        })
    else:
        all_data.append({
            "Nama": name,
            "Id": symbol,
            "Saat ini": "-",
            "Open": "-",
            "High": "-",
            "Low": "-",
            "Vol": "-"
        })

df = pd.DataFrame(all_data)

# CSS biar responsif + warna tiap kolom
st.markdown(
    """
    <style>
    .responsive-table {
        width: 100%;
        border-collapse: collapse;
    }
    .responsive-table th, .responsive-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }

    /* Warna untuk kolom */
    .col-Open { color: orange; font-weight: bold; }
    .col-Low { color: red; font-weight: bold; }
    .col-High { color: green; font-weight: bold; }

    @media (max-width: 768px) {
        .responsive-table thead {
            display: none;
        }
        .responsive-table tr {
            display: block;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
        }
        .responsive-table td {
            display: block;
            text-align: right;
            font-size: 14px;
            border: none;
            border-bottom: 1px dotted #ccc;
        }
        .responsive-table td::before {
            content: attr(data-label);
            float: left;
            font-weight: bold;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# refresh setiap 60 detik
st_autorefresh(interval=60 * 1000, key="refresh")


def df_to_responsive_html(df):
    thead = "".join([f"<th>{col}</th>" for col in df.columns])
    rows = ""
    for _, row in df.iterrows():
        tds = ""
        for col in df.columns:
            col_class = f"col-{col}" if col in ["Open", "Low", "High"] else ""
            tds += f'<td class="{col_class}" data-label="{col}">{row[col]}</td>'
        rows += f"<tr>{tds}</tr>"
    return f"<table class='responsive-table'><thead><tr>{thead}</tr></thead><tbody>{rows}</tbody></table>"

st.markdown(df_to_responsive_html(df), unsafe_allow_html=True)
