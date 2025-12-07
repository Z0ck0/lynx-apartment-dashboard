import streamlit as st
import pandas as pd
from pathlib import Path
import calendar
import altair as alt
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple


# 🔧 CONFIG
FILE_PATH = Path("Lynx Apartment Tracker.xlsx")
CUSTOM_METRICS_FILE = Path("lynx_custom_metrics.json")
REPORT_TEMPLATES_FILE = Path("lynx_report_templates.json")
CUSTOM_GRAPHS_FILE = Path("lynx_custom_graphs.json")

# Logo assets paths
# Logo files should be placed in the assets/ folder:
# - assets/lynx_logo_light.png: White logo on transparent background (for dark backgrounds)
# - assets/lynx_logo_dark.png: Black logo on transparent background (for light backgrounds)
# NOTE: For best results, logo files should be square (1:1 aspect ratio) to prevent stretching
#       in the browser tab favicon. Recommended size: 32x32px to 512x512px, square format.
LYNX_LOGO_LIGHT = Path("assets/lynx_logo_light.png")  # White logo for dark backgrounds
LYNX_LOGO_DARK = Path("assets/lynx_logo_dark.png")    # Black logo for light backgrounds

st.set_page_config(
    page_title="Lynx Apartment Dashboard",
    layout="wide"
)


# ========= RESPONSIVE CSS FOR MOBILE =========

def inject_responsive_css():
    """
    Inject comprehensive responsive CSS for mobile devices.
    Specifically optimized for iPhone 16 Pro and other mobile devices.
    This CSS forces columns to stack on mobile and ensures no horizontal scrolling.
    """
    st.markdown("""
    <style>
    /* ========================================
       GLOBAL RESPONSIVE CSS
       Optimized for iPhone 16 Pro and mobile devices
       ======================================== */
    
    /* Prevent horizontal scrolling on all devices */
    .main .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Mobile-first: Base styles for small screens */
    @media screen and (max-width: 768px) {
        /* iPhone 16 Pro Portrait: 393px */
        
        /* Force single column layout for Streamlit columns */
        .element-container > div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Responsive padding */
        .main .block-container {
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }
        
        /* Responsive font sizes */
        h1 { font-size: 1.75rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.25rem !important; }
        h4 { font-size: 1.1rem !important; }
        
        /* Metric cards - full width on mobile */
        .metric-card-container {
            width: 100% !important;
            margin-bottom: 1rem;
            padding: 0.875rem !important;
        }
        
        /* Metric card text - responsive */
        .metric-card-container div[style*="font-size:0.9rem"] {
            font-size: 0.85rem !important;
        }
        
        .metric-card-container div[style*="font-size:1.5rem"] {
            font-size: 1.25rem !important;
        }
        
        /* Info icon - larger for touch */
        .metric-info-icon {
            width: 24px !important;
            height: 24px !important;
            font-size: 14px !important;
            top: 0.5rem !important;
            right: 0.5rem !important;
        }
        
        /* Tooltip - full width on mobile */
        .metric-tooltip {
            width: calc(100vw - 2rem) !important;
            max-width: calc(100vw - 2rem) !important;
            left: 0 !important;
            transform: none !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
        
        /* Popup modal - full width on mobile */
        .metric-popup-content {
            max-width: 95vw !important;
            width: 95vw !important;
            padding: 1rem !important;
            margin: 1rem !important;
        }
        
        /* Form inputs - full width */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input,
        .stTextArea > div > div > textarea {
            width: 100% !important;
        }
        
        /* Buttons - full width on mobile for better touch targets */
        .stButton > button {
            width: 100% !important;
            min-height: 44px; /* iOS recommended touch target */
        }
        
        /* Sidebar adjustments */
        .css-1d391kg {
            padding-top: 1rem;
        }
        
        /* Chart containers - ensure they fit */
        .element-container[data-testid="stVerticalBlock"] > div {
            overflow-x: auto;
        }
        
        /* Tables - horizontal scroll on mobile */
        .dataframe {
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }
        
        /* Caption text - smaller on mobile */
        .stCaption {
            font-size: 0.75rem !important;
        }
        
        /* Expander - full width */
        .streamlit-expanderHeader {
            font-size: 1rem !important;
        }
        
        /* Segmented control - stack if needed */
        .stSegmentedControl {
            width: 100% !important;
        }
        
        /* Prevent text overflow */
        * {
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        
        /* Remove white-space: nowrap where it causes issues */
        h2[style*="white-space: nowrap"] {
            white-space: normal !important;
        }
    }
    
    /* Tablet and small desktop (768px - 1024px) */
    @media screen and (min-width: 768px) and (max-width: 1024px) {
        /* Allow 2 columns on tablet */
        .element-container > div[data-testid="column"] {
            flex: 1 1 50% !important;
            max-width: 50% !important;
        }
        
        /* 3-column layouts become 2 columns */
        .element-container > div[data-testid="column"]:nth-child(3) {
            flex: 1 1 100% !important;
            max-width: 100% !important;
        }
    }
    
    /* iPhone 16 Pro Landscape (852px) - Special handling */
    @media screen and (min-width: 800px) and (max-width: 900px) and (orientation: landscape) {
        /* Allow 2 columns in landscape on iPhone */
        .element-container > div[data-testid="column"] {
            flex: 1 1 50% !important;
            max-width: 50% !important;
        }
        
        /* But keep single column for 3-column layouts */
        .element-container > div[data-testid="column"]:nth-child(3) {
            flex: 1 1 100% !important;
            max-width: 100% !important;
        }
    }
    
    /* Desktop (> 1024px) - Keep current behavior */
    @media screen and (min-width: 1024px) {
        .main .block-container {
            max-width: 1200px;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }
    
    /* Additional mobile optimizations */
    @media screen and (max-width: 768px) {
        /* Ensure all Streamlit components respect container width */
        [data-testid="stVerticalBlock"] {
            width: 100% !important;
        }
        
        /* Date input - stack vertically */
        .stDateInput {
            width: 100% !important;
        }
        
        /* Selectbox - full width */
        .stSelectbox {
            width: 100% !important;
        }
        
        /* Number input - full width */
        .stNumberInput {
            width: 100% !important;
        }
        
        /* Text area - full width */
        .stTextArea {
            width: 100% !important;
        }
        
        /* Data editor - scrollable */
        [data-testid="stDataEditor"] {
            overflow-x: auto;
        }
    }
    
    /* Touch-friendly targets (iOS recommendation: 44x44px minimum) */
    @media (pointer: coarse) {
        button, .stButton > button {
            min-height: 44px;
            min-width: 44px;
        }
        
        .metric-info-icon {
            min-width: 44px;
            min-height: 44px;
        }
    }
    
    /* Print styles - hide on print */
    @media print {
        .metric-info-icon,
        .metric-tooltip,
        .metric-popup-overlay {
            display: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# ========= CONSTANTS & HELPERS =========

FX_RATE = 61.51  # 1 euro = 61.51 denars

# ========= METRIC DESCRIPTIONS & INFO =========
# Central configuration for all metric descriptions, formulas, and insights
METRIC_INFO = {
    "Reservations": {
        "description": "Number of completed bookings in the selected period.",
        "formula": "Count of all bookings",
        "insight": "Shows booking volume. Higher numbers indicate more activity and potential revenue."
    },
    "Total nights": {
        "description": "Sum of all booked nights in the selected period.",
        "formula": "Sum of Nights column for all bookings",
        "insight": "Total occupancy nights. Compare with available nights to understand utilization."
    },
    "Occupancy (%)": {
        "description": "Percentage of available nights that were actually booked.",
        "formula": "(Total Nights ÷ Nights Available) × 100",
        "insight": "Key efficiency metric. Higher occupancy means better utilization of your property. Industry standard is typically 60-80%."
    },
    "Total revenue (€)": {
        "description": "Total revenue from all stays in the selected period.",
        "formula": "Sum of Revenue for stay (€) for all bookings",
        "insight": "Primary income metric. Track trends over time to identify growth patterns."
    },
    "Net Profit (€)": {
        "description": "Net profit after per-stay expenses and fixed monthly costs for the selected period.",
        "formula": "Total Revenue - Per-Stay Expenses - Fixed Costs",
        "insight": "True profitability indicator. Positive values mean the property is generating profit after all costs."
    },
    "Net Income Before Fixed Costs (€)": {
        "description": "Net profit after per-stay expenses, before fixed monthly costs.",
        "formula": "Total Revenue - Per-Stay Expenses",
        "insight": "Shows variable profitability. Useful for comparing different platforms or periods without fixed cost allocation."
    },
    "Average price per night (€)": {
        "description": "Average revenue per booked night (same as ADR).",
        "formula": "Total Revenue ÷ Booked Nights",
        "insight": "Pricing efficiency metric. Compare with market rates to optimize pricing strategy."
    },
    "Average stay (nights)": {
        "description": "Average length of stay per reservation.",
        "formula": "Total Nights ÷ Reservations",
        "insight": "Guest behavior indicator. Longer stays reduce turnover costs and increase revenue per booking."
    },
    "Average Monthly Gross Income (€)": {
        "description": "Calculates the average gross income per month for the selected period. Gross income is based on the RevenueForStay of each booking.",
        "formula": "(Sum of RevenueForStay for all bookings in selected period) ÷ (Number of unique months within selected period)",
        "insight": "Monthly gross income average. Helps understand revenue consistency and seasonal patterns. Higher values indicate better monthly performance."
    },
    "Average Monthly Net Income (€)": {
        "description": "Calculates the average net income per month for the selected period. Net income accounts for per-stay expenses and fixed monthly costs.",
        "formula": "(Sum of NetProfit for all bookings in selected period) ÷ (Number of unique months within selected period)",
        "insight": "Monthly net income average. Shows true profitability per month after all costs. Essential for cash flow planning and financial forecasting."
    },
    "Profit Margin (%)": {
        "description": "Percentage of revenue that becomes profit after all costs.",
        "formula": "(Net Profit ÷ Total Revenue) × 100",
        "insight": "Profitability efficiency. Higher margins mean better cost control and pricing power."
    },
    "Cost per Reservation (€)": {
        "description": "Average variable cost per booking.",
        "formula": "Total Per-Stay Expenses ÷ Reservations",
        "insight": "Cost efficiency per booking. Lower values indicate better operational efficiency."
    },
    "Profit per Night (€)": {
        "description": "Profitability per booked night.",
        "formula": "Net Profit ÷ Total Nights",
        "insight": "Nightly profitability. Compare across periods to track efficiency improvements."
    },
    "Profit per Stay (€)": {
        "description": "Average profit per booking.",
        "formula": "Net Profit ÷ Reservations",
        "insight": "Booking-level profitability. Useful for understanding the value of each reservation."
    },
    "Net Income per Night Before Fixed (€)": {
        "description": "Variable profit per night (before fixed costs).",
        "formula": "Net Income Before Fixed Costs ÷ Total Nights",
        "insight": "Shows nightly profitability excluding fixed costs. Useful for scaling decisions."
    },
    "Net Income per Stay Before Fixed (€)": {
        "description": "Variable profit per booking (before fixed costs).",
        "formula": "Net Income Before Fixed Costs ÷ Reservations",
        "insight": "Booking-level profitability excluding fixed costs. Compare platforms on this metric."
    },
    "Cost Percentage of Revenue (%)": {
        "description": "What portion of revenue goes to variable costs.",
        "formula": "(Total Per-Stay Expenses ÷ Total Revenue) × 100",
        "insight": "Cost structure indicator. Lower percentages mean more revenue retained after variable costs."
    },
    "Fixed Cost Percentage of Revenue (%)": {
        "description": "What portion of revenue covers fixed costs.",
        "formula": "(Total Fixed Costs ÷ Total Revenue) × 100",
        "insight": "Fixed cost burden. Lower percentages indicate better revenue relative to fixed expenses."
    },
    "Revenue per Available Night (€)": {
        "description": "Revenue per available night (RevPAR). Standard hotel metric showing revenue efficiency.",
        "formula": "Total Revenue ÷ Nights Available (all days in period)",
        "insight": "Industry-standard efficiency metric. Combines occupancy and pricing. Higher RevPAR means better overall performance."
    },
    "Average Daily Rate (€)": {
        "description": "Average revenue per booked night (ADR). Standard hotel metric showing average price per night.",
        "formula": "Total Revenue ÷ Booked Nights (only occupied nights)",
        "insight": "Pricing power indicator. Compare with market rates. Higher ADR with good occupancy means strong pricing strategy."
    },
    "Airbnb revenue (€)": {
        "description": "Total revenue coming from Airbnb bookings in the selected period.",
        "formula": "Sum of Revenue for stay (€) where Platform = Airbnb",
        "insight": "Platform-specific revenue. Track to understand which platform generates more income."
    },
    "Booking.com revenue (€)": {
        "description": "Total revenue coming from Booking.com bookings in the selected period.",
        "formula": "Sum of Revenue for stay (€) where Platform = Booking.com",
        "insight": "Platform-specific revenue. Compare with Airbnb to optimize channel mix."
    },
    "Airbnb share of revenue (%)": {
        "description": "Percentage of total revenue generated via Airbnb.",
        "formula": "(Airbnb Revenue ÷ Total Revenue) × 100",
        "insight": "Channel diversification indicator. Over-reliance on one platform increases risk."
    },
    "Booking.com share of revenue (%)": {
        "description": "Percentage of total revenue generated via Booking.com.",
        "formula": "(Booking.com Revenue ÷ Total Revenue) × 100",
        "insight": "Channel diversification indicator. Balanced distribution reduces platform dependency risk."
    },
    "Airbnb nights": {
        "description": "Total booked nights that came from Airbnb.",
        "formula": "Sum of Nights where Platform = Airbnb",
        "insight": "Platform occupancy volume. Compare with Booking.com to understand channel performance."
    },
    "Booking.com nights": {
        "description": "Total booked nights that came from Booking.com.",
        "formula": "Sum of Nights where Platform = Booking.com",
        "insight": "Platform occupancy volume. Compare with Airbnb to optimize channel strategy."
    },
    "Airbnb Occupancy (%)": {
        "description": "Occupancy rate specifically from Airbnb.",
        "formula": "(Airbnb Nights ÷ Nights Available) × 100",
        "insight": "Platform-specific efficiency. Compare with Booking.com occupancy to identify stronger channel."
    },
    "Booking.com Occupancy (%)": {
        "description": "Occupancy rate specifically from Booking.com.",
        "formula": "(Booking.com Nights ÷ Nights Available) × 100",
        "insight": "Platform-specific efficiency. Compare with Airbnb occupancy to optimize channel mix."
    },
    "Airbnb RevPAR (€)": {
        "description": "Revenue per available night from Airbnb.",
        "formula": "Airbnb Revenue ÷ Nights Available (all days in period)",
        "insight": "Platform efficiency metric. Higher values indicate better Airbnb performance relative to capacity."
    },
    "Booking.com RevPAR (€)": {
        "description": "Revenue per available night from Booking.com.",
        "formula": "Booking.com Revenue ÷ Nights Available (all days in period)",
        "insight": "Platform efficiency metric. Compare with Airbnb RevPAR to optimize channel strategy."
    },
    "Airbnb ADR (€)": {
        "description": "Average daily rate from Airbnb.",
        "formula": "Airbnb Revenue ÷ Airbnb Booked Nights (only occupied nights)",
        "insight": "Platform pricing power. Compare with Booking.com ADR to understand pricing differences."
    },
    "Booking.com ADR (€)": {
        "description": "Average daily rate from Booking.com.",
        "formula": "Booking.com Revenue ÷ Booking.com Booked Nights (only occupied nights)",
        "insight": "Platform pricing power. Compare with Airbnb ADR to optimize pricing strategy."
    },
    "Platform Profitability Difference (€)": {
        "description": "Difference in profit per booking between Airbnb and Booking.com.",
        "formula": "Airbnb Profit per Reservation - Booking.com Profit per Reservation",
        "insight": "Platform comparison metric. Positive values mean Airbnb is more profitable per booking."
    },
    "Average Stay Length by Platform (nights)": {
        "description": "Average booking duration by platform.",
        "formula": "Platform Nights ÷ Platform Reservations",
        "insight": "Guest behavior by channel. Longer stays reduce turnover costs and increase revenue per booking."
    },
    "Platform Revenue per Reservation (€)": {
        "description": "Average booking value by platform.",
        "formula": "Platform Revenue ÷ Platform Reservations",
        "insight": "Channel value comparison. Higher values indicate more valuable bookings from that platform."
    },
    "Platform Cost per Reservation (€)": {
        "description": "Average variable cost per booking by platform.",
        "formula": "Platform Per-Stay Expenses ÷ Platform Reservations",
        "insight": "Cost efficiency by channel. Lower costs per booking mean better profitability from that platform."
    },
    "Platform Mix (%)": {
        "description": "Share of bookings by platform.",
        "formula": "(Platform Reservations ÷ Total Reservations) × 100",
        "insight": "Channel diversification. Balanced mix reduces dependency risk on a single platform."
    },
    "Revenue Concentration Risk (%)": {
        "description": "How dependent you are on one platform.",
        "formula": "Max(Airbnb Revenue Share, Booking.com Revenue Share)",
        "insight": "Risk indicator. Values above 80% indicate high dependency on one channel. Diversify to reduce risk."
    },
    "Average group size": {
        "description": "Average number of guests per stay.",
        "formula": "Total Guests ÷ Reservations",
        "insight": "Guest behavior indicator. Larger groups may require more amenities but also generate more revenue."
    },
    "Average Revenue per Stay (€)": {
        "description": "Average booking value.",
        "formula": "Total Revenue ÷ Reservations",
        "insight": "Booking value metric. Track trends to understand if average booking value is increasing."
    },
    "Average Cost per Stay (€)": {
        "description": "Average variable cost per booking.",
        "formula": "Total Per-Stay Expenses ÷ Reservations",
        "insight": "Cost efficiency per booking. Lower values indicate better operational efficiency."
    },
    "Average Guests per Booking by Platform": {
        "description": "Average group size by platform.",
        "formula": "Platform Total Guests ÷ Platform Reservations",
        "insight": "Guest behavior by channel. Different platforms may attract different group sizes."
    },
    "Parking Usage (%)": {
        "description": "Percentage of bookings where parking was used.",
        "formula": "(Bookings with Parking = Yes ÷ Total Reservations) × 100",
        "insight": "Amenity utilization. High usage may indicate need for parking availability or pricing."
    },
    "Revenue per Guest (€)": {
        "description": "Average revenue per person.",
        "formula": "Total Revenue ÷ Total Guests",
        "insight": "Per-guest value metric. Higher values indicate better revenue extraction per person."
    },
    "Baby Crib usage (%)": {
        "description": "Percentage of bookings where the baby crib was used.",
        "formula": "(Bookings with Baby Crib = Yes ÷ Total Reservations) × 100",
        "insight": "Amenity utilization. Track to understand guest needs and optimize amenity offerings."
    },
    "Sofa Bed usage (%)": {
        "description": "Percentage of bookings where the sofa bed was used.",
        "formula": "(Bookings with Sofa Bed = Yes ÷ Total Reservations) × 100",
        "insight": "Amenity utilization. High usage indicates capacity flexibility is valued by guests."
    },
    "Total Per-Stay Expenses (€)": {
        "description": "Sum of all variable per-stay costs.",
        "formula": "Sum of Transportation + Laundry + Consumables + Bank Fees",
        "insight": "Total variable costs. Track trends to identify cost reduction opportunities."
    },
    "Total Fixed Costs (€)": {
        "description": "Sum of all fixed monthly costs for the selected period.",
        "formula": "Sum of Monthly Fixed Costs for selected period",
        "insight": "Fixed cost burden. These costs must be covered regardless of occupancy."
    },
    "Average Cost per Night (€)": {
        "description": "Variable cost per booked night.",
        "formula": "Total Per-Stay Expenses ÷ Total Nights",
        "insight": "Nightly cost efficiency. Lower values mean better cost control per night."
    },
    "Fixed Cost per Night (€)": {
        "description": "Fixed cost allocation per booked night.",
        "formula": "Total Fixed Costs ÷ Total Nights",
        "insight": "Fixed cost burden per night. Higher occupancy spreads fixed costs across more nights."
    },
    "Fixed Cost per Reservation (€)": {
        "description": "Fixed cost allocation per booking.",
        "formula": "Total Fixed Costs ÷ Reservations",
        "insight": "Fixed cost burden per booking. More bookings spread fixed costs across more reservations."
    },
    "Variable vs Fixed Cost Ratio": {
        "description": "Ratio of variable to fixed costs.",
        "formula": "Total Per-Stay Expenses ÷ Total Fixed Costs",
        "insight": "Cost structure indicator. Higher ratios mean more scalable cost structure (more variable, less fixed)."
    },
    "Break-even Occupancy (%)": {
        "description": "Minimum occupancy needed to cover fixed costs.",
        "formula": "(Total Fixed Costs ÷ (ADR × Nights Available)) × 100",
        "insight": "Critical threshold. Below this occupancy, you're losing money on fixed costs."
    },
    "Break-even Nights": {
        "description": "Minimum nights needed to cover fixed costs.",
        "formula": "Total Fixed Costs ÷ ADR",
        "insight": "Critical threshold. Below this number of nights, fixed costs aren't covered."
    },
    "Best month by revenue": {
        "description": "Month and year with the highest total revenue.",
        "formula": "Month with maximum Total Revenue",
        "insight": "Peak performance indicator. Identify seasonal patterns and replicate successful strategies."
    },
    "Best Month by Profit (€)": {
        "description": "Month and year with the highest profit.",
        "formula": "Month with maximum Net Profit",
        "insight": "Peak profitability indicator. Analyze what made this month successful."
    },
    "Worst Month by Revenue (€)": {
        "description": "Month and year with the lowest revenue.",
        "formula": "Month with minimum Total Revenue",
        "insight": "Low performance indicator. Identify causes and develop strategies to improve."
    },
    "Projected next-year revenue": {
        "description": "Simple projection: average monthly revenue × 12.",
        "formula": "Average Monthly Revenue × 12",
        "insight": "Basic revenue forecast. Use for planning and goal setting."
    },
    "Projected Next-Year Revenue (Weighted)": {
        "description": "Weighted projection favoring recent performance.",
        "formula": "(Recent 6 Months Avg × 0.6 + Older Months Avg × 0.4) × 12",
        "insight": "More accurate forecast. Recent trends weighted more heavily for better prediction."
    },
    "Projected Next-Year Profit (€)": {
        "description": "Forecast profit based on weighted revenue projection.",
        "formula": "Projected Weighted Revenue × (Average Profit Margin ÷ 100)",
        "insight": "Profit forecast. Use for financial planning and investment decisions."
    },
    "Month-over-Month Revenue Change (%)": {
        "description": "Percentage change in revenue from previous month.",
        "formula": "((Current Month Revenue - Previous Month Revenue) ÷ Previous Month Revenue) × 100",
        "insight": "Short-term trend indicator. Positive values show growth momentum."
    },
    "Year-over-Year Revenue Change (%)": {
        "description": "Percentage change in revenue compared to same period last year.",
        "formula": "((Current Year Revenue - Previous Year Revenue) ÷ Previous Year Revenue) × 100",
        "insight": "Long-term growth indicator. Accounts for seasonality by comparing same periods."
    },
    "3-Month Moving Average Revenue (€)": {
        "description": "Average revenue over the last 3 months.",
        "formula": "Sum of Last 3 Months Revenue ÷ 3",
        "insight": "Smoothed trend indicator. Reduces month-to-month volatility to show underlying trends."
    },
    "Seasonal Index": {
        "description": "Average seasonal index across all months.",
        "formula": "Average of (Monthly Revenue ÷ Annual Average Revenue) × 100",
        "insight": "Seasonality indicator. Values above 100 indicate above-average months, below 100 indicate below-average."
    },
    "Transportation Cost per Stay (€)": {
        "description": "Average transportation cost per booking.",
        "formula": "Total Transportation Cost ÷ Reservations",
        "insight": "Transportation efficiency. Track to identify cost reduction opportunities."
    },
    "Laundry Cost per Stay (€)": {
        "description": "Average laundry cost per booking.",
        "formula": "Total Laundry Cost ÷ Reservations",
        "insight": "Laundry efficiency. Monitor for cost control and optimization opportunities."
    },
    "Consumable Cost per Stay (€)": {
        "description": "Average consumable cost per booking.",
        "formula": "Total Consumable Cost ÷ Reservations",
        "insight": "Consumable efficiency. Track to optimize supply costs and guest experience balance."
    },
    "Bank Fees per Stay (€)": {
        "description": "Average bank fees per booking.",
        "formula": "Total Bank Fees ÷ Reservations",
        "insight": "Payment processing efficiency. Consider alternative payment methods if fees are high."
    },
    "Top Countries by Bookings": {
        "description": "Top 5 countries by number of bookings.",
        "formula": "Top 5 countries sorted by reservation count",
        "insight": "Guest origin analysis. Understand your market and tailor marketing to top countries."
    },
    "Top Countries by Revenue": {
        "description": "Top 5 countries by total revenue.",
        "formula": "Top 5 countries sorted by total revenue",
        "insight": "Revenue source analysis. Focus marketing efforts on high-value country markets."
    }
}


def render_lynx_logo(logo_path: Path, width: int = 50) -> None:
    """
    Render the Lynx logo image in the sidebar.
    
    Args:
        logo_path: Path to the logo file (LYNX_LOGO_LIGHT or LYNX_LOGO_DARK)
        width: Width of the logo in pixels (default: 50px)
    
    Usage:
        - Use LYNX_LOGO_LIGHT (white) for dark backgrounds (sidebar, dark UI)
        - Use LYNX_LOGO_DARK (black) for light backgrounds (reports, HTML exports)
    """
    if logo_path.exists():
        st.sidebar.image(str(logo_path), width=width)
    else:
        # Fallback if logo file is missing
        st.sidebar.markdown("🏡")  # Temporary fallback


def recalc_monthly_costs(df: pd.DataFrame) -> pd.DataFrame:
    """Recalculate euro columns and Total fixed costs from denar values."""
    pairs = [
        ("Electricity (den)", "Electricity (€)"),
        ("Water (den)", "Water (€)"),
        ("Property Management Fee (den)", "Property Management Fee (€)"),
    ]

    for den_col, eur_col in pairs:
        if den_col in df.columns and eur_col in df.columns:
            df[den_col] = pd.to_numeric(df[den_col], errors="coerce").fillna(0)
            df[eur_col] = df[den_col] / FX_RATE

    euro_cols = [c for c in df.columns if "€" in c and c != "Total Fixed Costs (€)"]
    for c in euro_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    if "Total Fixed Costs (€)" in df.columns:
        df["Total Fixed Costs (€)"] = df[euro_cols].sum(axis=1)

    return df


def recalc_toiletries(df: pd.DataFrame) -> pd.DataFrame:
    """Recalculate Total (MKD) = Unit Price (MKD) * Units per Stay."""
    # Support both old and new column names for backward compatibility
    unit_price_col = "Unit Price (MKD)" if "Unit Price (MKD)" in df.columns else "Piece"
    units_col = "Units per Stay" if "Units per Stay" in df.columns else "Quantity per stay"
    total_col = "Total (MKD)" if "Total (MKD)" in df.columns else "Total per stay"
    
    if unit_price_col in df.columns:
        df[unit_price_col] = pd.to_numeric(df[unit_price_col], errors="coerce").fillna(0)
    if units_col in df.columns:
        df[units_col] = pd.to_numeric(df[units_col], errors="coerce").fillna(0)

    if unit_price_col in df.columns and units_col in df.columns:
        df[total_col] = df[unit_price_col] * df[units_col]

    return df


def get_current_consumables_totals(consumables_df: pd.DataFrame) -> tuple[float, float]:
    """
    Calculate current consumables totals from the consumables DataFrame.
    
    Args:
        consumables_df: DataFrame with columns "Total (MKD)" (or "Total per stay" for backward compatibility)
    
    Returns:
        tuple: (total_mkd, total_eur) - Total cost per stay in MKD and EUR
    """
    # Support both new and old column names for backward compatibility
    total_col = "Total (MKD)" if "Total (MKD)" in consumables_df.columns else "Total per stay"
    
    if total_col in consumables_df.columns:
        total_mkd = float(consumables_df[total_col].fillna(0).sum())
    else:
        total_mkd = 0.0
    
    total_eur = total_mkd / FX_RATE if total_mkd > 0 else 0.0
    return total_mkd, total_eur


def clean_bookings(df: pd.DataFrame) -> pd.DataFrame:
    """Drop fully empty rows and rows without check-in date."""
    df = df.dropna(how="all")
    if "Check-in date" in df.columns:
        df = df[df["Check-in date"].notna()]
    return df


def sort_bookings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort bookings by Check-in date ascending and reset the index.
    This keeps the DataFrame in strict chronological order.
    """
    if "Check-in date" in df.columns:
        df = df.sort_values("Check-in date", ascending=True).reset_index(drop=True)
    return df


def compute_nights_available(
    bookings_df: pd.DataFrame, 
    selected_year: int | None = None,
    period_type: str | None = None,
    month: int | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> int:
    """
    Calculate nights available based on period type.
    
    Args:
        bookings_df: Bookings DataFrame (used for date range fallback)
        selected_year: Selected year (for year/month_year periods)
        period_type: Type of period - "month_year", "year", "date_range", or None
        month: Selected month (1-12) for month_year period
        start_date: Start date for date_range period
        end_date: End date for date_range period
    
    Returns:
        Number of nights available in the selected period
    """
    bookings_df = clean_bookings(bookings_df.copy())

    # For monthly reports: calculate days in that specific month
    if period_type == "month_year" and selected_year is not None and month is not None:
        # Get number of days in the specific month/year
        days_in_month = calendar.monthrange(selected_year, month)[1]
        return days_in_month
    
    # For yearly reports: calculate days in that year
    elif period_type == "year" and selected_year is not None:
        # Full calendar year availability
        return 366 if calendar.isleap(selected_year) else 365
    
    # For date range: calculate days in the date range
    elif period_type == "date_range" and start_date is not None and end_date is not None:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        # Calculate days between start and end (inclusive)
        days = (end_dt - start_dt).days + 1
        return max(days, 0)
    
    # Legacy behavior: if selected_year is given but no period_type, assume year
    elif selected_year is not None:
        # Full calendar year availability
        return 366 if calendar.isleap(selected_year) else 365

    # Fallback: if no period info, use date range from bookings
    if bookings_df.empty or "Check-in date" not in bookings_df.columns or "Check-out date" not in bookings_df.columns:
        return 0

    start = bookings_df["Check-in date"].min()
    end = bookings_df["Check-out date"].max()
    if pd.isna(start) or pd.isna(end):
        return 0

    return max((end - start).days, 0)


# ========== CHART CONFIGURATION ==========

# Chart layout options
CHART_LAYOUTS = [
    "Line",
    "Bar",
    "Stacked bar",
    "Area",
    "Platform comparison",
    # Extended layouts for custom graphs
    "Pie",
    "Donut",
    "Horizontal bar",
    "Smooth area",
    "Scatter",
    "Multi-series line",
]

# Chart metric keys
CHART_METRIC_KEYS = [
    "revenue_by_month",
    "nights_by_month",
    "reservations_by_month",
    "adr_by_month",
    "occupancy_by_month",
]

# Chart metric labels (for display)
CHART_METRIC_LABELS = {
    "revenue_by_month": "Revenue by month",
    "nights_by_month": "Nights by month",
    "reservations_by_month": "Reservations by month",
    "adr_by_month": "ADR by month",
    "occupancy_by_month": "Occupancy by month",
}

# Chart metric units (for Y-axis labels)
CHART_METRIC_UNITS = {
    "revenue_by_month": "Revenue (€)",
    "nights_by_month": "Nights",
    "reservations_by_month": "Reservations",
    "adr_by_month": "ADR (€)",
    "occupancy_by_month": "Occupancy (%)",
}


# ========== DATA LAYER ==========

@st.cache_data
def load_data(file_path: Path):
    bookings = pd.read_excel(file_path, sheet_name="Bookings")
    monthly_costs = pd.read_excel(file_path, sheet_name="Monthly_Costs")
    toiletries = pd.read_excel(file_path, sheet_name="Toiletries")

    # Map old column names to new column names for backward compatibility
    # Note: Excel file may have columns with (€) already, so we check both variations
    column_mapping_bookings = {
        "Nights (auto)": "Nights",
        "Month (number, auto)": "Check-in Month",
        "Year (auto)": "Check-in Year",
        "Net income before fixed (auto)": "Net Income Before Fixed Costs (€)",
        "Booker name": "Guest Name",
        "Sofabed": "Sofa Bed",
        # Map Excel column names (with €) to standard names for internal use
        "Transport (to/from) (€)": "Transportation Cost (€)",
        "Laundry (€)": "Laundry Cost (€)",
        "Toiletries (€)": "Consumable Cost (€)",
        "Guest Supplies Cost (€)": "Consumable Cost (€)",  # Map old name to new name
        # Also map old names without € for backward compatibility
        "Transport (to/from)": "Transportation Cost (€)",
        "Laundry": "Laundry Cost (€)",
        "Toiletries": "Consumable Cost (€)",
        "Guest Supplies Cost": "Consumable Cost (€)",  # Map old name to new name
    }
    bookings = bookings.rename(columns=column_mapping_bookings)

    column_mapping_costs = {
        "Building management (den)": "Property Management Fee (den)",
        "Building management (€)": "Property Management Fee (€)",
        "Total fixed costs (auto)": "Total Fixed Costs (€)",
    }
    monthly_costs = monthly_costs.rename(columns=column_mapping_costs)

    # Clean bookings
    bookings = clean_bookings(bookings)

    # Ensure correct dtypes
    if "Check-in date" in bookings.columns:
        bookings["Check-in date"] = pd.to_datetime(bookings["Check-in date"])
    if "Check-out date" in bookings.columns:
        bookings["Check-out date"] = pd.to_datetime(bookings["Check-out date"])

    # Nights
    if "Nights" in bookings.columns:
        missing_nights = bookings["Nights"].isna()
        bookings.loc[missing_nights, "Nights"] = (
            bookings.loc[missing_nights, "Check-out date"]
            - bookings.loc[missing_nights, "Check-in date"]
        ).dt.days

    # Month / Year
    if "Check-in Month" in bookings.columns:
        missing_month = bookings["Check-in Month"].isna()
        bookings.loc[missing_month, "Check-in Month"] = (
            bookings.loc[missing_month, "Check-in date"].dt.month
        )
    if "Check-in Year" in bookings.columns:
        missing_year = bookings["Check-in Year"].isna()
        bookings.loc[missing_year, "Check-in Year"] = (
            bookings.loc[missing_year, "Check-in date"].dt.year
        )

    # Net income before fixed
    if "Net Income Before Fixed Costs (€)" in bookings.columns:
        mask = bookings["Net Income Before Fixed Costs (€)"].isna()
        bookings.loc[mask, "Net Income Before Fixed Costs (€)"] = (
            bookings["Revenue for stay (€)"].fillna(0)
            - bookings["Per-stay expenses (€)"].fillna(0)
        )

    # Always keep bookings sorted chronologically by Check-in date
    bookings = sort_bookings(bookings)

    # Clean toiletries column name & rename columns to new names
    if "Unnamed: 0" in toiletries.columns:
        toiletries = toiletries.rename(columns={"Unnamed: 0": "Item"})
    
    # Rename consumables columns to new names (with backward compatibility)
    column_mapping_toiletries = {}
    if "Piece" in toiletries.columns and "Unit Price (MKD)" not in toiletries.columns:
        column_mapping_toiletries["Piece"] = "Unit Price (MKD)"
    if "Quantity per stay" in toiletries.columns and "Units per Stay" not in toiletries.columns:
        column_mapping_toiletries["Quantity per stay"] = "Units per Stay"
    if "Total per stay" in toiletries.columns and "Total (MKD)" not in toiletries.columns:
        column_mapping_toiletries["Total per stay"] = "Total (MKD)"
    
    if column_mapping_toiletries:
        toiletries = toiletries.rename(columns=column_mapping_toiletries)
    
    toiletries = recalc_toiletries(toiletries)

    # Recalculate monthly costs totals
    monthly_costs = recalc_monthly_costs(monthly_costs)

    return bookings, monthly_costs, toiletries


def save_data(bookings: pd.DataFrame,
              monthly_costs: pd.DataFrame,
              toiletries: pd.DataFrame,
              file_path: Path):
    """Overwrite only Bookings, Monthly_Costs, Toiletries."""
    load_data.clear()

    bookings = clean_bookings(bookings)
    # Ensure bookings are sorted before saving back to Excel
    bookings = sort_bookings(bookings)
    monthly_costs = recalc_monthly_costs(monthly_costs)
    
    # Ensure toiletries columns use new names before saving
    column_mapping_toiletries = {}
    if "Piece" in toiletries.columns and "Unit Price (MKD)" not in toiletries.columns:
        column_mapping_toiletries["Piece"] = "Unit Price (MKD)"
    if "Quantity per stay" in toiletries.columns and "Units per Stay" not in toiletries.columns:
        column_mapping_toiletries["Quantity per stay"] = "Units per Stay"
    if "Total per stay" in toiletries.columns and "Total (MKD)" not in toiletries.columns:
        column_mapping_toiletries["Total per stay"] = "Total (MKD)"
    
    if column_mapping_toiletries:
        toiletries = toiletries.rename(columns=column_mapping_toiletries)
    
    toiletries = recalc_toiletries(toiletries)

    with pd.ExcelWriter(
        file_path,
        engine="openpyxl",
        mode="a",
        if_sheet_exists="replace",
    ) as writer:
        bookings.to_excel(writer, sheet_name="Bookings", index=False)
        monthly_costs.to_excel(writer, sheet_name="Monthly_Costs", index=False)
        toiletries.to_excel(writer, sheet_name="Toiletries", index=False)


def compute_metrics(bookings: pd.DataFrame,
                    monthly_costs: pd.DataFrame,
                    view_mode: str):
    """
    view_mode: 'Overall', 'Airbnb', 'Booking.com'
    """
    df = clean_bookings(bookings.copy())

    # Normalize platform labels
    if "Platform" in df.columns:
        df["Platform"] = df["Platform"].replace({"Booking": "Booking.com"})

    # Filter by platform
    if view_mode == "Airbnb":
        df = df[df["Platform"] == "Airbnb"]
    elif view_mode == "Booking.com":
        df = df[df["Platform"] == "Booking.com"]

    reservations = len(df)
    total_nights = df["Nights"].fillna(0).sum() if "Nights" in df.columns else 0
    total_revenue = df["Revenue for stay (€)"].fillna(0).sum() if "Revenue for stay (€)" in df.columns else 0
    total_per_stay = df["Per-stay expenses (€)"].fillna(0).sum() if "Per-stay expenses (€)" in df.columns else 0

    if "Net Income Before Fixed Costs (€)" in df.columns:
        net_before_fixed = df["Net Income Before Fixed Costs (€)"].fillna(
            df["Revenue for stay (€)"].fillna(0) - df["Per-stay expenses (€)"].fillna(0)
        ).sum()
    else:
        net_before_fixed = total_revenue - total_per_stay

    # Only for Overall: use fixed costs
    if view_mode == "Overall" and "Total Fixed Costs (€)" in monthly_costs.columns:
        total_fixed = monthly_costs["Total Fixed Costs (€)"].fillna(0).sum()
    else:
        total_fixed = None

    avg_price_per_night = total_revenue / total_nights if total_nights > 0 else 0

    metrics = {
        "Reservations": int(reservations),
        "Total nights": int(total_nights),  # Nights should be whole numbers
        "Total revenue (€)": float(total_revenue),
        "Total Per-Stay Expenses (€)": float(total_per_stay),
        "Net Income Before Fixed Costs (€)": float(net_before_fixed),
        "Average price per night (€)": float(avg_price_per_night),
    }

    if total_fixed is not None:
        metrics["Total Fixed Costs (€)"] = float(total_fixed)
        metrics["Net Profit (€)"] = float(net_before_fixed - total_fixed)

    return metrics


def monthly_revenue_by_platform(bookings: pd.DataFrame):
    df = clean_bookings(bookings.copy())

    # Normalize platform labels
    df["Platform"] = df["Platform"].replace({"Booking": "Booking.com"})

    # Make sure revenue is numeric
    df["Revenue for stay (€)"] = pd.to_numeric(
        df["Revenue for stay (€)"], errors="coerce"
    ).fillna(0)

    # Convert year/month to numeric, allow NaN, then drop invalid rows
    df["Year"] = pd.to_numeric(df["Check-in Year"], errors="coerce")
    df["Month"] = pd.to_numeric(df["Check-in Month"], errors="coerce")

    df = df.dropna(subset=["Year", "Month"])

    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(int)

    # Build a Year-Month column
    df["Year-Month"] = pd.to_datetime(
        df["Year"].astype(str) + "-" + df["Month"].astype(str) + "-01"
    )

    grouped = df.groupby(["Year-Month", "Platform"], as_index=False)[
        "Revenue for stay (€)"
    ].sum()

    pivot = grouped.pivot(
        index="Year-Month",
        columns="Platform",
        values="Revenue for stay (€)",
    ).fillna(0)

    if "Airbnb" not in pivot.columns:
        pivot["Airbnb"] = 0
    if "Booking.com" not in pivot.columns:
        pivot["Booking.com"] = 0

    pivot = pivot.sort_index()
    pivot.index.name = "Month"

    return pivot


def monthly_nights_by_platform(bookings: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total nights by month and platform."""
    df = clean_bookings(bookings.copy())
    
    # Normalize platform labels
    df["Platform"] = df["Platform"].replace({"Booking": "Booking.com"})
    
    # Make sure nights is numeric
    df["Nights"] = pd.to_numeric(df["Nights"], errors="coerce").fillna(0)
    
    # Convert year/month to numeric
    df["Year"] = pd.to_numeric(df["Check-in Year"], errors="coerce")
    df["Month"] = pd.to_numeric(df["Check-in Month"], errors="coerce")
    df = df.dropna(subset=["Year", "Month"])
    
    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(int)
    
    # Build Year-Month column
    df["Year-Month"] = pd.to_datetime(
        df["Year"].astype(str) + "-" + df["Month"].astype(str) + "-01"
    )
    
    grouped = df.groupby(["Year-Month", "Platform"], as_index=False)["Nights"].sum()
    
    pivot = grouped.pivot(
        index="Year-Month",
        columns="Platform",
        values="Nights",
    ).fillna(0)
    
    if "Airbnb" not in pivot.columns:
        pivot["Airbnb"] = 0
    if "Booking.com" not in pivot.columns:
        pivot["Booking.com"] = 0
    
    pivot = pivot.sort_index()
    pivot.index.name = "Month"
    return pivot


def monthly_reservations_by_platform(bookings: pd.DataFrame) -> pd.DataFrame:
    """Count reservations by month and platform."""
    df = clean_bookings(bookings.copy())
    
    # Normalize platform labels
    df["Platform"] = df["Platform"].replace({"Booking": "Booking.com"})
    
    # Convert year/month to numeric
    df["Year"] = pd.to_numeric(df["Check-in Year"], errors="coerce")
    df["Month"] = pd.to_numeric(df["Check-in Month"], errors="coerce")
    df = df.dropna(subset=["Year", "Month"])
    
    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(int)
    
    # Build Year-Month column
    df["Year-Month"] = pd.to_datetime(
        df["Year"].astype(str) + "-" + df["Month"].astype(str) + "-01"
    )
    
    grouped = df.groupby(["Year-Month", "Platform"], as_index=False).size()
    grouped.rename(columns={"size": "Count"}, inplace=True)
    
    pivot = grouped.pivot(
        index="Year-Month",
        columns="Platform",
        values="Count",
    ).fillna(0)
    
    if "Airbnb" not in pivot.columns:
        pivot["Airbnb"] = 0
    if "Booking.com" not in pivot.columns:
        pivot["Booking.com"] = 0
    
    pivot = pivot.sort_index()
    pivot.index.name = "Month"
    return pivot


def monthly_adr_by_platform(bookings: pd.DataFrame) -> pd.DataFrame:
    """Calculate ADR (Average Daily Rate) by month and platform."""
    revenue_df = monthly_revenue_by_platform(bookings)
    nights_df = monthly_nights_by_platform(bookings)
    
    # Calculate ADR for each platform
    adr_df = revenue_df.copy()
    for platform in ["Airbnb", "Booking.com"]:
        if platform in revenue_df.columns and platform in nights_df.columns:
            nights_values = nights_df[platform]
            adr_df[platform] = revenue_df[platform] / nights_values.replace(0, pd.NA)
            adr_df[platform] = adr_df[platform].fillna(0)
        else:
            adr_df[platform] = 0
    
    return adr_df


def monthly_occupancy_by_platform(
    bookings: pd.DataFrame,
    nights_available_per_month: dict | None = None,
) -> pd.DataFrame:
    """
    Calculate occupancy percentage by month and platform.
    
    Args:
        bookings: Bookings dataframe
        nights_available_per_month: Dict mapping Year-Month timestamps to available nights.
                                   If None, calculates based on calendar days in each month.
    """
    nights_df = monthly_nights_by_platform(bookings)
    
    # Calculate available nights per month if not provided
    if nights_available_per_month is None:
        nights_available_per_month = {}
        for year_month in nights_df.index:
            year = year_month.year
            month = year_month.month
            days_in_month = calendar.monthrange(year, month)[1]
            nights_available_per_month[year_month] = days_in_month
    
    # Calculate occupancy percentage
    occupancy_df = nights_df.copy()
    for platform in ["Airbnb", "Booking.com"]:
        if platform in nights_df.columns:
            for year_month in nights_df.index:
                available = nights_available_per_month.get(year_month, 0)
                booked = nights_df.loc[year_month, platform]
                if available > 0:
                    occupancy_df.loc[year_month, platform] = (booked / available) * 100
                else:
                    occupancy_df.loc[year_month, platform] = 0
    
    return occupancy_df


def get_monthly_metric_data(
    bookings: pd.DataFrame,
    metric_key: str,
    nights_available_per_month: dict | None = None,
) -> pd.DataFrame:
    """Get monthly aggregated data for a given metric key."""
    if metric_key == "revenue_by_month":
        return monthly_revenue_by_platform(bookings)
    elif metric_key == "nights_by_month":
        return monthly_nights_by_platform(bookings)
    elif metric_key == "reservations_by_month":
        return monthly_reservations_by_platform(bookings)
    elif metric_key == "adr_by_month":
        return monthly_adr_by_platform(bookings)
    elif metric_key == "occupancy_by_month":
        return monthly_occupancy_by_platform(bookings, nights_available_per_month)
    else:
        raise ValueError(f"Unknown metric key: {metric_key}")


def prepare_chart_data(
    metric_df: pd.DataFrame,
    view_mode: str,
) -> pd.DataFrame:
    """
    Prepare chart data based on view mode.
    Returns a dataframe with columns ready for charting.
    """
    if view_mode == "Airbnb":
        chart_df = metric_df[["Airbnb"]].copy()
    elif view_mode == "Booking.com":
        chart_df = metric_df[["Booking.com"]].copy()
    else:
        # Overall or Comparison: show both platforms and total
        chart_df = metric_df[["Airbnb", "Booking.com"]].copy()
        chart_df["Total"] = chart_df["Airbnb"] + chart_df["Booking.com"]
    
    return chart_df


def build_altair_chart(
    chart_df: pd.DataFrame,
    metric_key: str,
    layout: str,
    view_mode: str,
) -> alt.Chart:
    """
    Build an Altair chart based on the layout type.
    
    Args:
        chart_df: DataFrame with index as Year-Month and columns as platforms/metrics
        metric_key: The metric key (e.g., "revenue_by_month")
        layout: Chart layout type ("Line", "Bar", "Stacked bar", "Area", "Platform comparison")
        view_mode: Current view mode ("Overall", "Airbnb", "Booking.com", "Comparison")
    
    Returns:
        Altair chart object
    """
    # Reset index to make Month/Category columns explicit
    df = chart_df.reset_index()

    # If this is a time-series dataframe, expect a "Month" index/column.
    # For aggregated metrics (single value), the index may be something else.
    if "Month" in df.columns:
        if df["Month"].dtype == "datetime64[ns]":
            df["Month"] = df["Month"].dt.strftime("%Y-%m")
        else:
            df["Month"] = df["Month"].astype(str)

    # Get Y-axis label
    y_label = CHART_METRIC_UNITS.get(metric_key, "Value")
    
    # Color scheme for platforms / categories
    platform_colors = {
        "Airbnb": "#FF5A5F",        # Airbnb pink/red
        "Booking.com": "#003580",   # Booking.com blue
        "Total": "#7B68EE",         # Medium slate blue
    }
    
    # ---------- TIME-SERIES LAYOUTS (require Month column) ----------
    if "Month" in df.columns and layout == "Line":
        # Melt dataframe for line chart
        df_melted = df.melt(
            id_vars=["Month"],
            var_name="Platform",
            value_name="Value"
        )
        
        chart = (
            alt.Chart(df_melted)
            .mark_line(point=True, strokeWidth=2)
            .encode(
                x=alt.X("Month:O", title="Month", sort=None),
                y=alt.Y("Value:Q", title=y_label),
                color=alt.Color(
                    "Platform:N",
                    scale=alt.Scale(
                        domain=list(df_melted["Platform"].unique()),
                        range=[platform_colors.get(p, "#808080") for p in df_melted["Platform"].unique()]
                    ),
                    legend=alt.Legend(title="Platform")
                ),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip("Platform:N", title="Platform"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
        )
        
    elif "Month" in df.columns and layout == "Bar":
        # Melt dataframe for bar chart
        df_melted = df.melt(
            id_vars=["Month"],
            var_name="Platform",
            value_name="Value"
        )
        
        chart = (
            alt.Chart(df_melted)
            .mark_bar()
            .encode(
                x=alt.X("Month:O", title="Month", sort=None),
                y=alt.Y("Value:Q", title=y_label),
                color=alt.Color(
                    "Platform:N",
                    scale=alt.Scale(
                        domain=list(df_melted["Platform"].unique()),
                        range=[platform_colors.get(p, "#808080") for p in df_melted["Platform"].unique()]
                    ),
                    legend=alt.Legend(title="Platform")
                ),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip("Platform:N", title="Platform"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
        )
        
    elif "Month" in df.columns and layout == "Stacked bar":
        # Melt dataframe for stacked bar chart
        df_melted = df.melt(
            id_vars=["Month"],
            var_name="Platform",
            value_name="Value"
        )
        # Remove Total from stacked bar (only show platforms)
        df_melted = df_melted[df_melted["Platform"] != "Total"]
        
        chart = (
            alt.Chart(df_melted)
            .mark_bar()
            .encode(
                x=alt.X("Month:O", title="Month", sort=None),
                y=alt.Y("Value:Q", title=y_label, stack="zero"),
                color=alt.Color(
                    "Platform:N",
                    scale=alt.Scale(
                        domain=list(df_melted["Platform"].unique()),
                        range=[platform_colors.get(p, "#808080") for p in df_melted["Platform"].unique()]
                    ),
                    legend=alt.Legend(title="Platform")
                ),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip("Platform:N", title="Platform"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
        )
        
    elif "Month" in df.columns and layout == "Area":
        # Melt dataframe for area chart
        df_melted = df.melt(
            id_vars=["Month"],
            var_name="Platform",
            value_name="Value"
        )
        # Remove Total from area chart (only show platforms)
        df_melted = df_melted[df_melted["Platform"] != "Total"]
        
        chart = (
            alt.Chart(df_melted)
            .mark_area(opacity=0.7)
            .encode(
                x=alt.X("Month:O", title="Month", sort=None),
                y=alt.Y("Value:Q", title=y_label, stack="zero"),
                color=alt.Color(
                    "Platform:N",
                    scale=alt.Scale(
                        domain=list(df_melted["Platform"].unique()),
                        range=[platform_colors.get(p, "#808080") for p in df_melted["Platform"].unique()]
                    ),
                    legend=alt.Legend(title="Platform")
                ),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip("Platform:N", title="Platform"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
        )
        
    elif "Month" in df.columns and layout == "Platform comparison":
        # Side-by-side comparison chart
        df_melted = df.melt(
            id_vars=["Month"],
            var_name="Platform",
            value_name="Value"
        )
        # Remove Total from comparison (only show platforms)
        df_melted = df_melted[df_melted["Platform"] != "Total"]
        
        chart = (
            alt.Chart(df_melted)
            .mark_bar()
            .encode(
                x=alt.X("Month:O", title="Month", sort=None),
                y=alt.Y("Value:Q", title=y_label),
                color=alt.Color(
                    "Platform:N",
                    scale=alt.Scale(
                        domain=list(df_melted["Platform"].unique()),
                        range=[platform_colors.get(p, "#808080") for p in df_melted["Platform"].unique()]
                    ),
                    legend=alt.Legend(title="Platform")
                ),
                column=alt.Column("Platform:N", spacing=10),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip("Platform:N", title="Platform"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
            .resolve_scale(y="independent")
        )
        
    # ---------- TIME-SERIES EXTENDED LAYOUTS ----------
    elif "Month" in df.columns and layout == "Smooth area":
        df_melted = df.melt(
            id_vars=["Month"],
            var_name="Platform",
            value_name="Value"
        )
        chart = (
            alt.Chart(df_melted)
            .mark_area(opacity=0.6, interpolate="monotone")
            .encode(
                x=alt.X("Month:O", title="Month", sort=None),
                y=alt.Y("Value:Q", title=y_label),
                color=alt.Color("Platform:N", legend=alt.Legend(title="Platform")),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip("Platform:N", title="Platform"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
        )

    elif "Month" in df.columns and layout == "Scatter":
        df_melted = df.melt(
            id_vars=["Month"],
            var_name="Platform",
            value_name="Value"
        )
        chart = (
            alt.Chart(df_melted)
            .mark_point(filled=True, size=80)
            .encode(
                x=alt.X("Month:O", title="Month", sort=None),
                y=alt.Y("Value:Q", title=y_label),
                color=alt.Color("Platform:N", legend=alt.Legend(title="Platform")),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip("Platform:N", title="Platform"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
        )

    elif "Month" in df.columns and layout == "Multi-series line":
        df_melted = df.melt(
            id_vars=["Month"],
            var_name="Platform",
            value_name="Value"
        )
        chart = (
            alt.Chart(df_melted)
            .mark_line(point=True, strokeWidth=3)
            .encode(
                x=alt.X("Month:O", title="Month", sort=None),
                y=alt.Y("Value:Q", title=y_label),
                color=alt.Color("Platform:N", legend=alt.Legend(title="Series")),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip("Platform:N", title="Series"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
        )

    # ---------- AGGREGATED / CATEGORY LAYOUTS (no Month column) ----------
    else:
        # For aggregated metrics we expect chart_df to have a single "Value" column
        # and optional "Category" column. If not provided, synthesize a default.
        if "Category" in df.columns and "Value" in df.columns:
            cat_field = "Category"
        else:
            # Synthesize a simple one-row dataframe
            df = pd.DataFrame(
                [{"Category": metric_key, "Value": float(chart_df.squeeze())}]
            )
            cat_field = "Category"

        if layout in ["Pie", "Donut"]:
            base = alt.Chart(df).encode(
                theta=alt.Theta("Value:Q", stack=True),
                color=alt.Color(f"{cat_field}:N", legend=alt.Legend(title="Category")),
                tooltip=[
                    alt.Tooltip(f"{cat_field}:N", title="Category"),
                    alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                ],
            )
            if layout == "Donut":
                chart = base.mark_arc(innerRadius=60)
            else:
                chart = base.mark_arc()

        elif layout == "Horizontal bar":
            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    y=alt.Y(f"{cat_field}:N", title="Category", sort="-x"),
                    x=alt.X("Value:Q", title=y_label),
                    tooltip=[
                        alt.Tooltip(f"{cat_field}:N", title="Category"),
                        alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                    ],
                )
            )

        elif layout == "Bar":
            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X(f"{cat_field}:N", title="Category", sort=None),
                    y=alt.Y("Value:Q", title=y_label),
                    tooltip=[
                        alt.Tooltip(f"{cat_field}:N", title="Category"),
                        alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                    ],
                )
            )

        else:
            # Fallback: simple point chart for other layouts
            chart = (
                alt.Chart(df)
                .mark_point(filled=True, size=100)
                .encode(
                    x=alt.X(f"{cat_field}:N", title="Category"),
                    y=alt.Y("Value:Q", title=y_label),
                    tooltip=[
                        alt.Tooltip(f"{cat_field}:N", title="Category"),
                        alt.Tooltip("Value:Q", title=y_label, format=",.2f"),
                    ],
                )
            )

    return chart


def calculate_number_of_months(start_date, end_date):
    """
    Calculate the number of unique months between start_date and end_date (inclusive).
    
    Args:
        start_date: Start date (datetime, date, or None)
        end_date: End date (datetime, date, or None)
    
    Returns:
        int: Number of unique months in the period
    """
    if start_date is None or end_date is None:
        return 0
    
    # Convert to pandas datetime if needed
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    # Calculate the difference in months
    # We count unique months by creating a date range and counting unique year-month combinations
    months = pd.period_range(start=start_dt, end=end_dt, freq='M')
    
    # If the range doesn't align with month boundaries, we need to count partial months
    # Count unique year-month combinations
    unique_months = set()
    
    # Start from the first day of start_date's month to the last day of end_date's month
    current = pd.Timestamp(year=start_dt.year, month=start_dt.month, day=1)
    end_month = pd.Timestamp(year=end_dt.year, month=end_dt.month, day=1)
    
    while current <= end_month:
        unique_months.add((current.year, current.month))
        # Move to next month
        if current.month == 12:
            current = pd.Timestamp(year=current.year + 1, month=1, day=1)
        else:
            current = pd.Timestamp(year=current.year, month=current.month + 1, day=1)
    
    return len(unique_months)


def calculate_avg_monthly_gross_income(df, start_date, end_date):
    """
    Calculate average monthly gross income for the selected period.
    
    Formula: (Sum of RevenueForStay for all bookings) ÷ (Number of unique months)
    
    Uses the actual date range of bookings in the dataframe, not the theoretical period boundaries,
    to ensure consistency when comparing year selection vs custom date ranges.
    
    Args:
        df: Filtered bookings dataframe
        start_date: Start date of the period (datetime, date, or None) - used as fallback
        end_date: End date of the period (datetime, date, or None) - used as fallback
    
    Returns:
        float: Average monthly gross income
    """
    if df.empty:
        return 0.0
    
    # Use actual date range from the bookings data, not theoretical boundaries
    if "Check-in date" in df.columns and not df["Check-in date"].dropna().empty:
        actual_start = pd.to_datetime(df["Check-in date"].min())
        actual_end = pd.to_datetime(df["Check-in date"].max())
    elif start_date is not None and end_date is not None:
        # Fallback to provided dates if no check-in dates available
        actual_start = pd.to_datetime(start_date)
        actual_end = pd.to_datetime(end_date)
    else:
        return 0.0
    
    # Calculate number of months based on actual data range
    num_months = calculate_number_of_months(actual_start, actual_end)
    if num_months == 0:
        return 0.0
    
    # Sum of RevenueForStay (Revenue for stay (€))
    if "Revenue for stay (€)" in df.columns:
        total_gross = float(df["Revenue for stay (€)"].fillna(0).sum())
    else:
        return 0.0
    
    # Calculate average
    avg_monthly_gross = total_gross / num_months if num_months > 0 else 0.0
    
    return avg_monthly_gross


def calculate_avg_monthly_net_income(df, monthly_costs_filtered, view_mode, start_date, end_date):
    """
    Calculate average monthly net income for the selected period.
    
    Formula: (Sum of NetProfit for all bookings) ÷ (Number of unique months)
    
    NetProfit = Revenue - Per-Stay Expenses - Fixed Costs (for Overall view)
    or NetProfit = Revenue - Per-Stay Expenses (for platform-specific views)
    
    Uses the actual date range of bookings in the dataframe, not the theoretical period boundaries,
    to ensure consistency when comparing year selection vs custom date ranges.
    
    Args:
        df: Filtered bookings dataframe
        monthly_costs_filtered: Filtered monthly costs dataframe
        view_mode: 'Overall', 'Airbnb', or 'Booking.com'
        start_date: Start date of the period (datetime, date, or None) - used as fallback
        end_date: End date of the period (datetime, date, or None) - used as fallback
    
    Returns:
        float: Average monthly net income
    """
    if df.empty:
        return 0.0
    
    # Use actual date range from the bookings data, not theoretical boundaries
    if "Check-in date" in df.columns and not df["Check-in date"].dropna().empty:
        actual_start = pd.to_datetime(df["Check-in date"].min())
        actual_end = pd.to_datetime(df["Check-in date"].max())
    elif start_date is not None and end_date is not None:
        # Fallback to provided dates if no check-in dates available
        actual_start = pd.to_datetime(start_date)
        actual_end = pd.to_datetime(end_date)
    else:
        return 0.0
    
    # Calculate number of months based on actual data range
    num_months = calculate_number_of_months(actual_start, actual_end)
    if num_months == 0:
        return 0.0
    
    # Calculate total revenue
    if "Revenue for stay (€)" in df.columns:
        total_revenue = float(df["Revenue for stay (€)"].fillna(0).sum())
    else:
        return 0.0
    
    # Calculate total per-stay expenses
    if "Per-stay expenses (€)" in df.columns:
        total_per_stay = float(df["Per-stay expenses (€)"].fillna(0).sum())
    else:
        total_per_stay = 0.0
    
    # Calculate net profit
    net_before_fixed = total_revenue - total_per_stay
    
    # For Overall view, subtract fixed costs
    if view_mode == "Overall" and "Total Fixed Costs (€)" in monthly_costs_filtered.columns:
        total_fixed = float(monthly_costs_filtered["Total Fixed Costs (€)"].fillna(0).sum())
        net_profit = net_before_fixed - total_fixed
    else:
        net_profit = net_before_fixed
    
    # Calculate average
    avg_monthly_net = net_profit / num_months if num_months > 0 else 0.0
    
    return avg_monthly_net


def calculate_all_metrics(
    bookings_filtered: pd.DataFrame,
    monthly_costs_filtered: pd.DataFrame,
    view_mode: str,
    nights_available: int,
    selected_year_int: int | None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> dict[str, dict]:
    """
    Calculate all metrics and return them in metric_info format.
    Returns: dict[key] = {label, value, prefix, explanation}
    """
    metric_info: dict[str, dict] = {}

    def add_metric(key, label, value, prefix, explanation):
        metric_info[key] = {
            "label": label,
            "value": value,
            "prefix": prefix,
            "explanation": explanation,
        }

    # Get base metrics
    metrics = compute_metrics(bookings_filtered, monthly_costs_filtered, view_mode)

    total_revenue = float(metrics.get("Total revenue (€)", 0.0))
    total_nights = int(metrics.get("Total nights", 0))  # Nights should be whole numbers
    total_per_stay_expenses = float(metrics.get("Total Per-Stay Expenses (€)", 0.0))
    total_fixed_costs = float(metrics.get("Total Fixed Costs (€)", 0.0))
    reservations = int(metrics.get("Reservations", 0))
    net_before_fixed = float(metrics.get("Net Income Before Fixed Costs (€)", 0.0))

    # Net profit (only available for Overall view)
    if "Net Profit (€)" in metrics:
        net_profit = float(metrics["Net Profit (€)"])
        net_label = "Net Profit (€)"
        net_explanation = (
            "Net profit after per-stay expenses and fixed monthly costs "
            "for the selected period."
        )
    else:
        net_profit = None
        net_label = "Net Income Before Fixed Costs (€)"
        net_explanation = (
            "Net profit after per-stay expenses, before fixed monthly costs "
            "for the selected view/platform."
        )

    # Derived basic metrics
    occupancy_pct = (total_nights / nights_available * 100) if nights_available > 0 else 0.0
    revpar = (total_revenue / nights_available) if nights_available > 0 else 0.0
    adr = (total_revenue / total_nights) if total_nights > 0 else 0.0
    avg_stay_nights = (total_nights / reservations) if reservations > 0 else 0.0

    # Platform statistics
    bookings_for_stats = clean_bookings(bookings_filtered.copy())
    if "Platform" in bookings_for_stats.columns:
        bookings_for_stats["platform_normalized"] = bookings_for_stats["Platform"].replace(
            {"Booking": "Booking.com"}
        )
    else:
        bookings_for_stats["platform_normalized"] = "Unknown"

    airbnb_mask = bookings_for_stats["platform_normalized"] == "Airbnb"
    booking_mask = bookings_for_stats["platform_normalized"] == "Booking.com"

    airbnb_revenue = float(
        bookings_for_stats.loc[airbnb_mask, "Revenue for stay (€)"].sum()
        if "Revenue for stay (€)" in bookings_for_stats.columns
        else 0.0
    )
    booking_revenue = float(
        bookings_for_stats.loc[booking_mask, "Revenue for stay (€)"].sum()
        if "Revenue for stay (€)" in bookings_for_stats.columns
        else 0.0
    )
    airbnb_nights = int(
        bookings_for_stats.loc[airbnb_mask, "Nights"].fillna(0).sum()
        if "Nights" in bookings_for_stats.columns
        else 0
    )
    booking_nights = int(
        bookings_for_stats.loc[booking_mask, "Nights"].fillna(0).sum()
        if "Nights" in bookings_for_stats.columns
        else 0
    )

    airbnb_reservations = int(airbnb_mask.sum()) if not bookings_for_stats.empty else 0
    booking_reservations = int(booking_mask.sum()) if not bookings_for_stats.empty else 0

    airbnb_revenue_share = (airbnb_revenue / total_revenue * 100) if total_revenue > 0 else 0.0
    booking_revenue_share = (booking_revenue / total_revenue * 100) if total_revenue > 0 else 0.0

    # Calculate platform-specific per-stay expenses
    if "Per-stay expenses (€)" in bookings_for_stats.columns:
        airbnb_per_stay_expenses = float(
            bookings_for_stats.loc[airbnb_mask, "Per-stay expenses (€)"].fillna(0).sum()
        )
        booking_per_stay_expenses = float(
            bookings_for_stats.loc[booking_mask, "Per-stay expenses (€)"].fillna(0).sum()
        )
        airbnb_net_before_fixed = airbnb_revenue - airbnb_per_stay_expenses
        booking_net_before_fixed = booking_revenue - booking_per_stay_expenses
    else:
        airbnb_per_stay_expenses = 0.0
        booking_per_stay_expenses = 0.0
        airbnb_net_before_fixed = airbnb_revenue
        booking_net_before_fixed = booking_revenue

    # Guest statistics
    if "Total guests" in bookings_for_stats.columns:
        avg_group_size = float(bookings_for_stats["Total guests"].fillna(0).mean())
        total_guests = float(bookings_for_stats["Total guests"].fillna(0).sum())
    elif {"Adults", "Children"} <= set(bookings_for_stats.columns):
        total_guests = float(
            (bookings_for_stats["Adults"].fillna(0) + bookings_for_stats["Children"].fillna(0)).sum()
        )
        avg_group_size = float(
            (bookings_for_stats["Adults"].fillna(0) + bookings_for_stats["Children"].fillna(0)).mean()
        )
    else:
        avg_group_size = 0.0
        total_guests = 0.0

    # Amenity usage
    baby_usage = None
    sofa_bed_usage = None
    parking_usage = None
    if not bookings_for_stats.empty:
        if "Baby Crib" in bookings_for_stats.columns:
            baby_usage = (
                bookings_for_stats["Baby Crib"].astype(str).str.lower().eq("yes").sum()
                / len(bookings_for_stats)
                * 100
            )
        if "Sofa Bed" in bookings_for_stats.columns:
            sofa_bed_usage = (
                bookings_for_stats["Sofa Bed"].astype(str).str.lower().eq("yes").sum()
                / len(bookings_for_stats)
                * 100
            )
        if "Parking" in bookings_for_stats.columns:
            parking_usage = (
                bookings_for_stats["Parking"].astype(str).str.lower().eq("yes").sum()
                / len(bookings_for_stats)
                * 100
            )

    # Cost breakdown per stay
    # Check for exact column names first, then try alternative names
    transportation_cost = 0.0
    laundry_cost = 0.0
    consumable_cost = 0.0
    bank_fees = 0.0
    
    # Try exact match first, then alternatives
    # Note: Column names are mapped in load_data() from old names to new names
    # When saving bookings, we use: "Transportation Cost (€)", "Laundry Cost (€)", "Consumable Cost (€)", "Bank Fees"
    
    if not bookings_for_stats.empty:
        # Use the mapped column names (after rename in load_data)
        # These should be "Transportation Cost (€)", "Laundry Cost (€)", "Consumable Cost (€)" after mapping
        # But also check original Excel names in case mapping didn't apply
        
        # Transportation Cost - check mapped name first, then Excel original names
        if "Transportation Cost (€)" in bookings_for_stats.columns:
            # Mapped name (preferred)
            col_data = pd.to_numeric(bookings_for_stats["Transportation Cost (€)"], errors="coerce").fillna(0)
            transportation_cost = float(col_data.sum())
        elif "Transport (to/from) (€)" in bookings_for_stats.columns:
            # Excel original name (if mapping didn't apply)
            col_data = pd.to_numeric(bookings_for_stats["Transport (to/from) (€)"], errors="coerce").fillna(0)
            transportation_cost = float(col_data.sum())
        elif "Transportation Cost" in bookings_for_stats.columns:
            col_data = pd.to_numeric(bookings_for_stats["Transportation Cost"], errors="coerce").fillna(0)
            transportation_cost = float(col_data.sum())
        elif "Transport (to/from)" in bookings_for_stats.columns:
            # Legacy name without €
            col_data = pd.to_numeric(bookings_for_stats["Transport (to/from)"], errors="coerce").fillna(0)
            transportation_cost = float(col_data.sum())
        
        # Laundry Cost - check mapped name first, then Excel original names
        if "Laundry Cost (€)" in bookings_for_stats.columns:
            # Mapped name (preferred)
            col_data = pd.to_numeric(bookings_for_stats["Laundry Cost (€)"], errors="coerce").fillna(0)
            laundry_cost = float(col_data.sum())
        elif "Laundry (€)" in bookings_for_stats.columns:
            # Excel original name (if mapping didn't apply)
            col_data = pd.to_numeric(bookings_for_stats["Laundry (€)"], errors="coerce").fillna(0)
            laundry_cost = float(col_data.sum())
        elif "Laundry Cost" in bookings_for_stats.columns:
            col_data = pd.to_numeric(bookings_for_stats["Laundry Cost"], errors="coerce").fillna(0)
            laundry_cost = float(col_data.sum())
        elif "Laundry" in bookings_for_stats.columns:
            # Legacy name without €
            col_data = pd.to_numeric(bookings_for_stats["Laundry"], errors="coerce").fillna(0)
            laundry_cost = float(col_data.sum())
        
        # Consumable Cost - check mapped name first, then Excel original names (backward compatibility)
        if "Consumable Cost (€)" in bookings_for_stats.columns:
            # New mapped name (preferred)
            col_data = pd.to_numeric(bookings_for_stats["Consumable Cost (€)"], errors="coerce").fillna(0)
            consumable_cost = float(col_data.sum())
        elif "Guest Supplies Cost (€)" in bookings_for_stats.columns:
            # Old name (backward compatibility)
            col_data = pd.to_numeric(bookings_for_stats["Guest Supplies Cost (€)"], errors="coerce").fillna(0)
            consumable_cost = float(col_data.sum())
        elif "Toiletries (€)" in bookings_for_stats.columns:
            # Excel original name (if mapping didn't apply)
            col_data = pd.to_numeric(bookings_for_stats["Toiletries (€)"], errors="coerce").fillna(0)
            consumable_cost = float(col_data.sum())
        elif "Consumable Cost" in bookings_for_stats.columns:
            col_data = pd.to_numeric(bookings_for_stats["Consumable Cost"], errors="coerce").fillna(0)
            consumable_cost = float(col_data.sum())
        elif "Guest Supplies Cost" in bookings_for_stats.columns:
            col_data = pd.to_numeric(bookings_for_stats["Guest Supplies Cost"], errors="coerce").fillna(0)
            consumable_cost = float(col_data.sum())
        elif "Toiletries" in bookings_for_stats.columns:
            # Legacy name without €
            col_data = pd.to_numeric(bookings_for_stats["Toiletries"], errors="coerce").fillna(0)
            consumable_cost = float(col_data.sum())
        
        # Bank Fees - Excel has "Bank Fees (€)", no mapping needed
        if "Bank Fees (€)" in bookings_for_stats.columns:
            # Excel original name
            col_data = pd.to_numeric(bookings_for_stats["Bank Fees (€)"], errors="coerce").fillna(0)
            bank_fees = float(col_data.sum())
        elif "Bank Fees" in bookings_for_stats.columns:
            # Without € symbol
            col_data = pd.to_numeric(bookings_for_stats["Bank Fees"], errors="coerce").fillna(0)
            bank_fees = float(col_data.sum())

    # Monthly revenue and seasonality
    best_month_label = "N/A"
    worst_month_label = "N/A"
    best_month_profit_label = "N/A"
    forecast_next_year = 0.0
    forecast_weighted = 0.0
    forecast_profit = 0.0
    mom_change = None
    yoy_change = None
    moving_avg_3m = None
    seasonal_index = None

    if not bookings_filtered.empty and \
       "Check-in Year" in bookings_filtered.columns and \
       "Check-in Month" in bookings_filtered.columns:

        monthly_revenue = (
            bookings_filtered
            .groupby(["Check-in Year", "Check-in Month"])["Revenue for stay (€)"]
            .sum()
            .reset_index()
        )
        monthly_revenue["Check-in Year"] = monthly_revenue["Check-in Year"].astype(int)
        monthly_revenue["Check-in Month"] = monthly_revenue["Check-in Month"].astype(int)
        monthly_revenue["MonthName"] = monthly_revenue["Check-in Month"].apply(
            lambda m: calendar.month_abbr[int(m)]
        )

        if not monthly_revenue.empty:
            best_row = monthly_revenue.loc[monthly_revenue["Revenue for stay (€)"].idxmax()]
            best_month_label = f"{best_row['MonthName']} {int(best_row['Check-in Year'])}"

            worst_row = monthly_revenue.loc[monthly_revenue["Revenue for stay (€)"].idxmin()]
            worst_month_label = f"{worst_row['MonthName']} {int(worst_row['Check-in Year'])}"

            months_count = len(monthly_revenue)
            forecast_next_year = float(
                monthly_revenue["Revenue for stay (€)"].mean() * 12 if months_count > 0 else 0.0
            )

            # Weighted forecast (recent 6 months weighted more)
            if months_count >= 6:
                recent_avg = monthly_revenue.tail(6)["Revenue for stay (€)"].mean()
                older_avg = monthly_revenue.head(months_count - 6)["Revenue for stay (€)"].mean() if months_count > 6 else recent_avg
                forecast_weighted = float((recent_avg * 0.6 + older_avg * 0.4) * 12)
            else:
                forecast_weighted = forecast_next_year

            # Month-over-month change (if we have at least 2 months)
            if months_count >= 2:
                sorted_monthly = monthly_revenue.sort_values(["Check-in Year", "Check-in Month"])
                if len(sorted_monthly) >= 2:
                    current = sorted_monthly.iloc[-1]["Revenue for stay (€)"]
                    previous = sorted_monthly.iloc[-2]["Revenue for stay (€)"]
                    if previous > 0:
                        mom_change = float(((current - previous) / previous) * 100)

            # Year-over-year change
            if selected_year_int is not None and months_count > 0:
                current_year_revenue = monthly_revenue[
                    monthly_revenue["Check-in Year"] == selected_year_int
                ]["Revenue for stay (€)"].sum()
                previous_year_revenue = monthly_revenue[
                    monthly_revenue["Check-in Year"] == selected_year_int - 1
                ]["Revenue for stay (€)"].sum()
                if previous_year_revenue > 0:
                    yoy_change = float(((current_year_revenue - previous_year_revenue) / previous_year_revenue) * 100)

            # 3-month moving average
            if months_count >= 3:
                sorted_monthly = monthly_revenue.sort_values(["Check-in Year", "Check-in Month"])
                moving_avg_3m = float(sorted_monthly.tail(3)["Revenue for stay (€)"].mean())

            # Seasonal index
            if months_count > 0:
                annual_avg = monthly_revenue["Revenue for stay (€)"].mean()
                if annual_avg > 0:
                    monthly_revenue["SeasonalIndex"] = (
                        monthly_revenue["Revenue for stay (€)"] / annual_avg * 100
                    )
                    # Return average seasonal index per month (across years)
                    seasonal_by_month = monthly_revenue.groupby("Check-in Month")["SeasonalIndex"].mean()
                    seasonal_index = float(seasonal_by_month.mean())  # Average across all months

        # Best month by profit
        if "Net Income Before Fixed Costs (€)" in bookings_filtered.columns:
            monthly_profit = (
                bookings_filtered
                .groupby(["Check-in Year", "Check-in Month"])["Net Income Before Fixed Costs (€)"]
                .sum()
                .reset_index()
            )
            if not monthly_profit.empty:
                best_profit_row = monthly_profit.loc[monthly_profit["Net Income Before Fixed Costs (€)"].idxmax()]
                best_month_profit_label = f"{calendar.month_abbr[int(best_profit_row['Check-in Month'])]} {int(best_profit_row['Check-in Year'])}"

    # Country statistics (for demographics section)
    top_countries_bookings = None
    top_countries_revenue = None
    if "Country" in bookings_for_stats.columns and not bookings_for_stats.empty:
        country_stats = bookings_for_stats.groupby("Country").agg({
            "Revenue for stay (€)": ["count", "sum", "mean"],
            "Nights": "mean"
        }).reset_index()
        country_stats.columns = ["Country", "Bookings", "TotalRevenue", "AvgRevenue", "AvgNights"]
        top_countries_bookings = country_stats.nlargest(5, "Bookings")[["Country", "Bookings"]].to_dict("records")
        top_countries_revenue = country_stats.nlargest(5, "TotalRevenue")[["Country", "TotalRevenue"]].to_dict("records")
        avg_revenue_by_country = country_stats[["Country", "AvgRevenue"]].to_dict("records")
        avg_stay_by_country = country_stats[["Country", "AvgNights"]].to_dict("records")

    # ========== CORE FINANCIAL & OCCUPANCY ==========
    add_metric("Reservations", "Reservations", reservations, "", "Number of completed bookings in the selected period.")
    add_metric("Total nights", "Total nights", total_nights, "", "Sum of all booked nights in the selected period.")
    add_metric("Occupancy (%)", "Occupancy (%)", occupancy_pct, "", "Share of available nights that were actually booked.")
    add_metric("Total revenue (€)", "Total revenue (€)", total_revenue, "€ ", "Total revenue from all stays in the selected period.")
    add_metric("Net Profit (€)", net_label, net_profit if net_profit is not None else net_before_fixed, "€ ", net_explanation)
    add_metric("Average price per night (€)", "Average price per night (€) (ADR)", adr, "€ ", "Average revenue per booked night (Total Revenue ÷ Booked Nights - only occupied nights). Same as ADR.")
    add_metric("Average stay (nights)", "Average stay (nights)", avg_stay_nights, "", "Average length of stay per reservation (total nights ÷ reservations).")
    
    # ========== AVERAGE MONTHLY INCOME METRICS ==========
    # Calculate average monthly gross and net income
    # Functions now use actual date range from bookings data, so they work for "All" selection too
    # Always add these metrics to metric_info so they're available in Custom Metrics
    avg_monthly_gross = calculate_avg_monthly_gross_income(bookings_filtered, start_date, end_date)
    avg_monthly_net = calculate_avg_monthly_net_income(bookings_filtered, monthly_costs_filtered, view_mode, start_date, end_date)
    
    add_metric("Average Monthly Gross Income (€)", "Average Monthly Gross Income (€)", avg_monthly_gross, "€ ", 
               "Calculates the average gross income per month for the selected period. Gross income is based on the RevenueForStay of each booking.")
    
    add_metric("Average Monthly Net Income (€)", "Average Monthly Net Income (€)", avg_monthly_net, "€ ", 
               "Calculates the average net income per month for the selected period. Net income accounts for per-stay expenses and fixed monthly costs.")

    # ========== PROFITABILITY METRICS ==========
    if net_profit is not None and total_revenue > 0:
        profit_margin = (net_profit / total_revenue) * 100
        add_metric("Profit Margin (%)", "Profit Margin (%)", profit_margin, "", "Percentage of revenue that becomes profit after all costs.")
    if reservations > 0:
        cost_per_reservation = total_per_stay_expenses / reservations
        add_metric("Cost per Reservation (€)", "Cost per Reservation (€)", cost_per_reservation, "€ ", "Average variable cost per booking.")
    if net_profit is not None:
        if total_nights > 0:
            profit_per_night = net_profit / total_nights
            add_metric("Profit per Night (€)", "Profit per Night (€)", profit_per_night, "€ ", "Profitability per booked night.")
        if reservations > 0:
            profit_per_stay = net_profit / reservations
            add_metric("Profit per Stay (€)", "Profit per Stay (€)", profit_per_stay, "€ ", "Average profit per booking.")
    if total_nights > 0:
        net_income_per_night = net_before_fixed / total_nights
        add_metric("Net Income per Night Before Fixed (€)", "Net Income per Night Before Fixed (€)", net_income_per_night, "€ ", "Variable profit per night (before fixed costs).")
    if reservations > 0:
        net_income_per_stay = net_before_fixed / reservations
        add_metric("Net Income per Stay Before Fixed (€)", "Net Income per Stay Before Fixed (€)", net_income_per_stay, "€ ", "Variable profit per booking (before fixed costs).")
    if total_revenue > 0:
        cost_pct_revenue = (total_per_stay_expenses / total_revenue) * 100
        add_metric("Cost Percentage of Revenue (%)", "Cost Percentage of Revenue (%)", cost_pct_revenue, "", "What portion of revenue goes to variable costs.")
    if total_revenue > 0 and total_fixed_costs > 0:
        fixed_cost_pct_revenue = (total_fixed_costs / total_revenue) * 100
        add_metric("Fixed Cost Percentage of Revenue (%)", "Fixed Cost Percentage of Revenue (%)", fixed_cost_pct_revenue, "", "What portion of revenue covers fixed costs.")

    # ========== PLATFORM PERFORMANCE METRICS ==========
    add_metric("Airbnb revenue (€)", "Airbnb revenue (€)", airbnb_revenue, "€ ", "Total revenue coming from Airbnb bookings in the selected period.")
    add_metric("Booking.com revenue (€)", "Booking.com revenue (€)", booking_revenue, "€ ", "Total revenue coming from Booking.com bookings in the selected period.")
    add_metric("Airbnb share of revenue (%)", "Airbnb share of revenue (%)", airbnb_revenue_share, "", "Percentage of total revenue generated via Airbnb.")
    add_metric("Booking.com share of revenue (%)", "Booking.com share of revenue (%)", booking_revenue_share, "", "Percentage of total revenue generated via Booking.com.")
    add_metric("Airbnb nights", "Airbnb nights", airbnb_nights, "", "Total booked nights that came from Airbnb.")
    add_metric("Booking.com nights", "Booking.com nights", booking_nights, "", "Total booked nights that came from Booking.com.")
    
    if nights_available > 0:
        airbnb_occupancy = (airbnb_nights / nights_available) * 100
        booking_occupancy = (booking_nights / nights_available) * 100
        add_metric("Airbnb Occupancy (%)", "Airbnb Occupancy (%)", airbnb_occupancy, "", "Occupancy rate specifically from Airbnb.")
        add_metric("Booking.com Occupancy (%)", "Booking.com Occupancy (%)", booking_occupancy, "", "Occupancy rate specifically from Booking.com.")
        
        # Platform RevPAR and ADR - display together for comparison
        airbnb_revpar = airbnb_revenue / nights_available
        booking_revpar = booking_revenue / nights_available
        add_metric("Airbnb RevPAR (€)", "Airbnb RevPAR (€)", airbnb_revpar, "€ ", "Revenue per available night from Airbnb (Airbnb Revenue ÷ Nights Available - all days in period).")
        add_metric("Booking.com RevPAR (€)", "Booking.com RevPAR (€)", booking_revpar, "€ ", "Revenue per available night from Booking.com (Booking.com Revenue ÷ Nights Available - all days in period).")
        
        # Platform ADR - display right after RevPAR for comparison
        if airbnb_nights > 0:
            airbnb_adr = airbnb_revenue / airbnb_nights
            add_metric("Airbnb ADR (€)", "Airbnb ADR (€)", airbnb_adr, "€ ", "Average daily rate from Airbnb (Airbnb Revenue ÷ Airbnb Booked Nights - only occupied nights).")
        if booking_nights > 0:
            booking_adr = booking_revenue / booking_nights
            add_metric("Booking.com ADR (€)", "Booking.com ADR (€)", booking_adr, "€ ", "Average daily rate from Booking.com (Booking.com Revenue ÷ Booking.com Booked Nights - only occupied nights).")
    
    if airbnb_reservations > 0 and booking_reservations > 0:
        airbnb_profit_per_res = airbnb_net_before_fixed / airbnb_reservations
        booking_profit_per_res = booking_net_before_fixed / booking_reservations
        platform_profit_diff = airbnb_profit_per_res - booking_profit_per_res
        add_metric("Platform Profitability Difference (€)", "Platform Profitability Difference (€)", platform_profit_diff, "€ ", "Difference in profit per booking between Airbnb and Booking.com (positive = Airbnb more profitable).")
    
    if airbnb_nights > 0 and airbnb_reservations > 0:
        airbnb_avg_stay = airbnb_nights / airbnb_reservations
        add_metric("Average Stay Length by Platform (nights)", "Airbnb Average Stay (nights)", airbnb_avg_stay, "", "Average booking duration from Airbnb.")
    if booking_nights > 0 and booking_reservations > 0:
        booking_avg_stay = booking_nights / booking_reservations
        if "Average Stay Length by Platform (nights)" in metric_info:
            # Update to show both platforms (averages with decimals)
            metric_info["Average Stay Length by Platform (nights)"]["label"] = "Average Stay Length by Platform (nights)"
            metric_info["Average Stay Length by Platform (nights)"]["value"] = f"Airbnb: {airbnb_avg_stay:.2f}, Booking.com: {booking_avg_stay:.2f}"
            metric_info["Average Stay Length by Platform (nights)"]["explanation"] = "Average booking duration by platform."
    
    if airbnb_reservations > 0:
        airbnb_rev_per_res = airbnb_revenue / airbnb_reservations
        add_metric("Platform Revenue per Reservation (€)", "Airbnb Revenue per Reservation (€)", airbnb_rev_per_res, "€ ", "Average booking value from Airbnb.")
    if booking_reservations > 0:
        booking_rev_per_res = booking_revenue / booking_reservations
        if "Platform Revenue per Reservation (€)" in metric_info:
            metric_info["Platform Revenue per Reservation (€)"]["label"] = "Platform Revenue per Reservation (€)"
            metric_info["Platform Revenue per Reservation (€)"]["value"] = f"Airbnb: €{airbnb_rev_per_res:.2f}, Booking.com: €{booking_rev_per_res:.2f}"
            metric_info["Platform Revenue per Reservation (€)"]["prefix"] = ""  # Remove prefix since value already contains € signs
            metric_info["Platform Revenue per Reservation (€)"]["explanation"] = "Average booking value by platform."
    
    if airbnb_reservations > 0:
        airbnb_cost_per_res = airbnb_per_stay_expenses / airbnb_reservations
        add_metric("Platform Cost per Reservation (€)", "Airbnb Cost per Reservation (€)", airbnb_cost_per_res, "€ ", "Average variable cost per booking from Airbnb.")
    if booking_reservations > 0:
        booking_cost_per_res = booking_per_stay_expenses / booking_reservations
        if "Platform Cost per Reservation (€)" in metric_info:
            metric_info["Platform Cost per Reservation (€)"]["label"] = "Platform Cost per Reservation (€)"
            metric_info["Platform Cost per Reservation (€)"]["value"] = f"Airbnb: €{airbnb_cost_per_res:.2f}, Booking.com: €{booking_cost_per_res:.2f}"
            metric_info["Platform Cost per Reservation (€)"]["prefix"] = ""  # Remove prefix since value already contains € signs
            metric_info["Platform Cost per Reservation (€)"]["explanation"] = "Average variable cost per booking by platform."
    
    if reservations > 0:
        platform_mix_airbnb = (airbnb_reservations / reservations) * 100
        platform_mix_booking = (booking_reservations / reservations) * 100
        add_metric("Platform Mix (%)", "Platform Mix (%)", f"Airbnb: {platform_mix_airbnb:.1f}%, Booking.com: {platform_mix_booking:.1f}%", "", "Share of bookings by platform.")
    
    revenue_concentration = max(airbnb_revenue_share, booking_revenue_share)
    add_metric("Revenue Concentration Risk (%)", "Revenue Concentration Risk (%)", revenue_concentration, "", "How dependent you are on one platform (higher = riskier).")

    # ========== GUEST BEHAVIOR METRICS ==========
    add_metric("Average group size", "Average group size", avg_group_size, "", "Average number of guests per stay (adults + children).")
    if reservations > 0:
        avg_revenue_per_stay = total_revenue / reservations
        add_metric("Average Revenue per Stay (€)", "Average Revenue per Stay (€)", avg_revenue_per_stay, "€ ", "Average booking value.")
        avg_cost_per_stay = total_per_stay_expenses / reservations
        add_metric("Average Cost per Stay (€)", "Average Cost per Stay (€)", avg_cost_per_stay, "€ ", "Average variable cost per booking.")
    
    if airbnb_reservations > 0 and "Total guests" in bookings_for_stats.columns:
        airbnb_avg_guests = float(bookings_for_stats.loc[airbnb_mask, "Total guests"].fillna(0).mean())
        booking_avg_guests = float(bookings_for_stats.loc[booking_mask, "Total guests"].fillna(0).mean()) if booking_reservations > 0 else 0.0
        add_metric("Average Guests per Booking by Platform", "Average Guests per Booking by Platform", f"Airbnb: {airbnb_avg_guests:.1f}, Booking.com: {booking_avg_guests:.1f}", "", "Average group size by platform.")
    
    if parking_usage is not None:
        add_metric("Parking Usage (%)", "Parking Usage (%)", parking_usage, "", "Percentage of bookings where parking was used.")
    
    if total_guests > 0:
        revenue_per_guest = total_revenue / total_guests
        add_metric("Revenue per Guest (€)", "Revenue per Guest (€)", revenue_per_guest, "€ ", "Average revenue per person.")
    
    if baby_usage is not None:
        add_metric("Baby Crib usage (%)", "Baby Crib usage (%)", baby_usage, "", "Percentage of bookings where the baby crib was used.")
    if sofa_bed_usage is not None:
        add_metric("Sofa Bed usage (%)", "Sofa Bed usage (%)", sofa_bed_usage, "", "Percentage of bookings where the sofa bed was used.")

    # ========== OPERATIONAL EFFICIENCY METRICS ==========
    add_metric("Total Per-Stay Expenses (€)", "Total Per-Stay Expenses (€)", total_per_stay_expenses, "€ ", "Sum of all variable per-stay costs (transportation, laundry, consumables, bank fees, etc.).")
    add_metric("Total Fixed Costs (€)", "Total Fixed Costs (€)", total_fixed_costs, "€ ", "Sum of all fixed monthly costs (electricity, water, property management fee, etc.) for the selected period.")
    
    if total_nights > 0:
        avg_cost_per_night = total_per_stay_expenses / total_nights
        add_metric("Average Cost per Night (€)", "Average Cost per Night (€)", avg_cost_per_night, "€ ", "Variable cost per booked night.")
        if total_fixed_costs > 0:
            fixed_cost_per_night = total_fixed_costs / total_nights
            add_metric("Fixed Cost per Night (€)", "Fixed Cost per Night (€)", fixed_cost_per_night, "€ ", "Fixed cost allocation per booked night.")
    
    if reservations > 0 and total_fixed_costs > 0:
        fixed_cost_per_reservation = total_fixed_costs / reservations
        add_metric("Fixed Cost per Reservation (€)", "Fixed Cost per Reservation (€)", fixed_cost_per_reservation, "€ ", "Fixed cost allocation per booking.")
    
    if total_fixed_costs > 0:
        variable_fixed_ratio = total_per_stay_expenses / total_fixed_costs
        add_metric("Variable vs Fixed Cost Ratio", "Variable vs Fixed Cost Ratio", variable_fixed_ratio, "", "Ratio of variable to fixed costs (higher = more scalable).")
    
    if adr > 0 and nights_available > 0:
        break_even_occupancy = (total_fixed_costs / (adr * nights_available)) * 100
        add_metric("Break-even Occupancy (%)", "Break-even Occupancy (%)", break_even_occupancy, "", "Minimum occupancy needed to cover fixed costs.")
        break_even_nights = total_fixed_costs / adr if adr > 0 else 0.0
        add_metric("Break-even Nights", "Break-even Nights", break_even_nights, "", "Minimum nights needed to cover fixed costs.")
    
    # RevPAR and ADR - display together for comparison
    add_metric("Revenue per Available Night (€)", "Revenue per Available Night (€) (RevPAR)", revpar, "€ ", "Revenue per available night (Total Revenue ÷ Nights Available - all days in period). Standard hotel metric showing revenue efficiency.")
    add_metric("Average Daily Rate (€)", "Average Daily Rate (€) (ADR)", adr, "€ ", "Average revenue per booked night (Total Revenue ÷ Booked Nights - only occupied nights). Standard hotel metric showing average price per night.")

    # ========== SEASONALITY & TRENDS METRICS ==========
    add_metric("Best month by revenue", "Best month by revenue", best_month_label, "", "Month and year with the highest total revenue in the selected data.")
    if best_month_profit_label != "N/A":
        add_metric("Best Month by Profit (€)", "Best Month by Profit (€)", best_month_profit_label, "", "Month and year with the highest profit in the selected data.")
    add_metric("Worst Month by Revenue (€)", "Worst Month by Revenue (€)", worst_month_label, "", "Month and year with the lowest revenue in the selected data.")
    add_metric("Projected next-year revenue", "Projected next-year revenue", forecast_next_year, "€ ", "Simple projection: average monthly revenue × 12.")
    if forecast_weighted > 0:
        add_metric("Projected Next-Year Revenue (Weighted)", "Projected Next-Year Revenue (Weighted)", forecast_weighted, "€ ", "Weighted projection: recent 6 months × 0.6 + older months × 0.4, then × 12.")
    if forecast_weighted > 0 and net_profit is not None and total_revenue > 0:
        profit_margin_avg = (net_profit / total_revenue) * 100
        forecast_profit = forecast_weighted * (profit_margin_avg / 100)
        add_metric("Projected Next-Year Profit (€)", "Projected Next-Year Profit (€)", forecast_profit, "€ ", "Forecast profit based on weighted revenue projection and average profit margin.")
    if mom_change is not None:
        add_metric("Month-over-Month Revenue Change (%)", "Month-over-Month Revenue Change (%)", mom_change, "", "Percentage change in revenue from previous month.")
    if yoy_change is not None:
        add_metric("Year-over-Year Revenue Change (%)", "Year-over-Year Revenue Change (%)", yoy_change, "", "Percentage change in revenue compared to same period last year.")
    if moving_avg_3m is not None:
        add_metric("3-Month Moving Average Revenue (€)", "3-Month Moving Average Revenue (€)", moving_avg_3m, "€ ", "Average revenue over the last 3 months (smoothed trend).")
    if seasonal_index is not None:
        add_metric("Seasonal Index", "Seasonal Index", seasonal_index, "", "Average seasonal index across all months (100 = average, >100 = above average, <100 = below average).")

    # ========== COST BREAKDOWN METRICS ==========
    # Always show these metrics, even if reservations is 0 (will show 0.00)
    if reservations > 0:
        add_metric("Transportation Cost per Stay (€)", "Transportation Cost per Stay (€)", transportation_cost / reservations, "€ ", "Average transportation cost per booking.")
        add_metric("Laundry Cost per Stay (€)", "Laundry Cost per Stay (€)", laundry_cost / reservations, "€ ", "Average laundry cost per booking.")
        add_metric("Consumable Cost per Stay (€)", "Consumable Cost per Stay (€)", consumable_cost / reservations, "€ ", "Average consumable cost per booking.")
        add_metric("Bank Fees per Stay (€)", "Bank Fees per Stay (€)", bank_fees / reservations, "€ ", "Average bank fees per booking.")
    else:
        # Show 0.00 if no reservations
        add_metric("Transportation Cost per Stay (€)", "Transportation Cost per Stay (€)", 0.0, "€ ", "Average transportation cost per booking.")
        add_metric("Laundry Cost per Stay (€)", "Laundry Cost per Stay (€)", 0.0, "€ ", "Average laundry cost per booking.")
        add_metric("Consumable Cost per Stay (€)", "Consumable Cost per Stay (€)", 0.0, "€ ", "Average consumable cost per booking.")
        add_metric("Bank Fees per Stay (€)", "Bank Fees per Stay (€)", 0.0, "€ ", "Average bank fees per booking.")

    # ========== GUEST DEMOGRAPHICS METRICS ==========
    # Note: These are stored as structured data, not simple values
    # We'll handle them specially in the UI rendering
    if top_countries_bookings:
        countries_str = ", ".join([f"{c['Country']} ({c['Bookings']})" for c in top_countries_bookings[:5]])
        add_metric("Top Countries by Bookings", "Top Countries by Bookings", countries_str, "", "Top 5 countries by number of bookings.")
    if top_countries_revenue:
        countries_str = ", ".join([f"{c['Country']} (€{c['TotalRevenue']:.0f})" for c in top_countries_revenue[:5]])
        add_metric("Top Countries by Revenue", "Top Countries by Revenue", countries_str, "", "Top 5 countries by total revenue.")

    return metric_info


# ========== METRICS CONFIGURATION ==========

# Define metric sections and their order
METRIC_SECTIONS = {
    "Custom": [],  # User-defined favorites (populated via session state)
    "Core Financial & Occupancy": [
        "Reservations",
        "Total nights",
        "Occupancy (%)",
        "Total revenue (€)",
        "Net Profit (€)",
        "Average price per night (€)",
        "Average stay (nights)",
        "Average Monthly Gross Income (€)",
        "Average Monthly Net Income (€)",
    ],
    "Profitability": [
        "Profit Margin (%)",
        "Cost per Reservation (€)",
        "Profit per Night (€)",
        "Profit per Stay (€)",
        "Net Income per Night Before Fixed (€)",
        "Net Income per Stay Before Fixed (€)",
        "Cost Percentage of Revenue (%)",
        "Fixed Cost Percentage of Revenue (%)",
    ],
    "Platform Performance": [
        "Airbnb revenue (€)",
        "Booking.com revenue (€)",
        "Airbnb share of revenue (%)",
        "Booking.com share of revenue (%)",
        "Airbnb nights",
        "Booking.com nights",
        "Airbnb ADR (€)",
        "Booking.com ADR (€)",
        "Airbnb Occupancy (%)",
        "Booking.com Occupancy (%)",
        "Airbnb RevPAR (€)",
        "Booking.com RevPAR (€)",
        "Platform Profitability Difference (€)",
        "Average Stay Length by Platform (nights)",
        "Platform Revenue per Reservation (€)",
        "Platform Cost per Reservation (€)",
        "Platform Mix (%)",
        "Revenue Concentration Risk (%)",
    ],
    "Guest Behavior": [
        "Average group size",
        "Average Revenue per Stay (€)",
        "Average Cost per Stay (€)",
        "Average Guests per Booking by Platform",
        "Parking Usage (%)",
        "Revenue per Guest (€)",
        "Baby Crib usage (%)",
        "Sofa Bed usage (%)",
    ],
    "Operational Efficiency": [
        "Total Per-Stay Expenses (€)",
        "Total Fixed Costs (€)",
        "Average Cost per Night (€)",
        "Fixed Cost per Night (€)",
        "Fixed Cost per Reservation (€)",
        "Variable vs Fixed Cost Ratio",
        "Break-even Occupancy (%)",
        "Break-even Nights",
        "Revenue per Available Night (€)",
        "Average Daily Rate (€)",
    ],
    "Seasonality & Trends": [
        "Best month by revenue",
        "Best Month by Profit (€)",
        "Worst Month by Revenue (€)",
        "Projected next-year revenue",
        "Projected Next-Year Revenue (Weighted)",
        "Projected Next-Year Profit (€)",
        "Month-over-Month Revenue Change (%)",
        "Year-over-Year Revenue Change (%)",
        "3-Month Moving Average Revenue (€)",
        "Seasonal Index",
    ],
    "Cost Breakdown": [
        "Transportation Cost per Stay (€)",
        "Laundry Cost per Stay (€)",
        "Consumable Cost per Stay (€)",
        "Bank Fees per Stay (€)",
    ],
    "Guest Demographics": [
        "Top Countries by Bookings",
        "Top Countries by Revenue",
        "Average Revenue by Country (€)",
        "Average Stay Length by Country (nights)",
    ],
}

# Section display names with icons
SECTION_DISPLAY_NAMES = {
    "Custom": "⭐ Custom Metrics",
    "Core Financial & Occupancy": "💰 Core Financial & Occupancy",
    "Profitability": "📈 Profitability",
    "Platform Performance": "📊 Platform Performance",
    "Guest Behavior": "👥 Guest Behavior",
    "Operational Efficiency": "⚙️ Operational Efficiency",
    "Seasonality & Trends": "📅 Seasonality & Trends",
    "Cost Breakdown": "💸 Cost Breakdown",
    "Guest Demographics": "🌍 Guest Demographics",
}


# ========== UI HELPERS ==========

def get_metric_info(metric_key: str) -> dict:
    """
    Get metric information from central METRIC_INFO dictionary.
    Returns empty dict if metric not found.
    """
    # Try exact match first
    if metric_key in METRIC_INFO:
        return METRIC_INFO[metric_key]
    
    # Try partial matches (for metrics with platform prefixes or variations)
    for key, info in METRIC_INFO.items():
        if key.lower() in metric_key.lower() or metric_key.lower() in key.lower():
            return info
    
    return {}


def inject_metric_tooltip_css():
    """Inject CSS for metric tooltips and info icons."""
    st.markdown("""
    <style>
    /* Metric card container with tooltip support */
    .metric-card-container {
        position: relative;
        padding: 1rem;
        border-radius: 1rem;
        border: 1px solid #333;
        background: rgba(0,0,0,0.35);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        cursor: help;
        transition: all 0.2s ease;
    }
    
    .metric-card-container:hover {
        border-color: #555;
        background: rgba(0,0,0,0.45);
    }
    
    /* Info icon */
    .metric-info-icon {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: rgba(100, 100, 100, 0.6);
        color: #fff;
        font-size: 12px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 10;
        transition: all 0.2s ease;
        pointer-events: auto;
        user-select: none;
        -webkit-tap-highlight-color: transparent;
    }
    
    .metric-info-icon:hover {
        background: rgba(100, 100, 100, 0.9);
        transform: scale(1.1);
    }
    
    .metric-info-icon:active {
        transform: scale(0.95);
    }
    
    /* Tooltip (hover + click toggle) */
    .metric-tooltip {
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        margin-bottom: 8px;
        padding: 10px 12px;
        background: rgba(20, 20, 20, 0.98);
        color: #fff;
        border: 1px solid #555;
        border-radius: 6px;
        font-size: 0.85rem;
        line-height: 1.4;
        white-space: normal;
        width: 280px;
        max-width: 90vw;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        z-index: 1000;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s ease, visibility 0.2s ease;
        visibility: hidden;
    }
    
    /* Desktop: Show on hover */
    @media (hover: hover) and (pointer: fine) {
        .metric-card-container:hover .metric-tooltip {
            opacity: 1;
            visibility: visible;
            pointer-events: auto;
        }
    }
    
    /* Show when toggled via click/tap */
    .metric-tooltip.visible {
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
    }
    
    /* Active state for icon when tooltip is visible */
    .metric-info-icon.active {
        background: rgba(100, 100, 100, 0.9) !important;
        transform: scale(1.1);
    }
    
    .metric-tooltip-title {
        font-weight: 600;
        margin-bottom: 6px;
        color: #4CAF50;
    }
    
    .metric-tooltip-formula {
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        color: #88C0D0;
        margin: 4px 0;
        padding: 4px;
        background: rgba(0,0,0,0.3);
        border-radius: 3px;
    }
    
    .metric-tooltip-insight {
        margin-top: 6px;
        color: #ccc;
        font-size: 0.8rem;
    }
    
    /* Popup modal (click) */
    .metric-popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        z-index: 10000;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    .metric-popup-overlay.active {
        display: flex;
    }
    
    .metric-popup-content {
        background: rgba(20, 20, 20, 0.98);
        border: 1px solid #555;
        border-radius: 10px;
        padding: 20px;
        max-width: 500px;
        width: 100%;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        position: relative;
    }
    
    .metric-popup-close {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(100, 100, 100, 0.6);
        color: #fff;
        border: none;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        font-size: 18px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }
    
        .metric-popup-close:hover {
            background: rgba(150, 150, 150, 0.8);
        }
        
        /* Mobile responsive styles for metric tooltips */
        @media screen and (max-width: 768px) {
            .metric-info-icon {
                width: 24px !important;
                height: 24px !important;
                font-size: 14px !important;
            }
            
            .metric-tooltip {
                width: calc(100vw - 2rem) !important;
                max-width: calc(100vw - 2rem) !important;
                left: 0 !important;
                transform: none !important;
                font-size: 0.8rem !important;
            }
            
            .metric-popup-content {
                max-width: 95vw !important;
                width: 95vw !important;
                padding: 1rem !important;
            }
        }
    
    .metric-popup-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 12px;
        color: #4CAF50;
    }
    
    .metric-popup-section {
        margin-bottom: 16px;
    }
    
    .metric-popup-section-label {
        font-weight: 600;
        color: #88C0D0;
        margin-bottom: 4px;
        font-size: 0.9rem;
    }
    
    .metric-popup-section-content {
        color: #ccc;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .metric-popup-formula {
        font-family: 'Courier New', monospace;
        background: rgba(0,0,0,0.4);
        padding: 8px;
        border-radius: 4px;
        margin-top: 4px;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .metric-tooltip {
            width: 250px;
            font-size: 0.8rem;
        }
        
        .metric-popup-content {
            max-width: 95vw;
            padding: 16px;
        }
        
        .metric-card-container {
            padding: 0.8rem;
        }
    }
    
    /* Touch device support - disable hover on mobile */
    @media (hover: none) {
        .metric-card-container:hover .metric-tooltip {
            opacity: 0;
            visibility: hidden;
        }
        
        /* Larger touch targets on mobile */
        .metric-info-icon {
            width: 24px !important;
            height: 24px !important;
            font-size: 14px !important;
            min-width: 44px;
            min-height: 44px;
            padding: 10px;
        }
    }
    
    /* Mobile-specific tooltip positioning */
    @media screen and (max-width: 768px) {
        .metric-tooltip {
            position: fixed !important;
            bottom: auto !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: calc(100vw - 2rem) !important;
            max-width: calc(100vw - 2rem) !important;
            max-height: 70vh;
            overflow-y: auto;
            margin: 0 !important;
            z-index: 10001 !important;
            padding: 1rem !important;
            font-size: 0.9rem !important;
        }
        
        .metric-tooltip-title {
            font-size: 1rem !important;
            margin-bottom: 0.75rem !important;
        }
        
        .metric-tooltip-formula {
            font-size: 0.85rem !important;
            padding: 0.5rem !important;
        }
        
        .metric-tooltip-insight {
            font-size: 0.85rem !important;
            margin-top: 0.75rem !important;
        }
    }
    
    /* Backdrop for mobile tooltips (created via JS) */
    #metric-tooltip-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        z-index: 10000;
        pointer-events: auto;
    }
    </style>
    """, unsafe_allow_html=True)


def inject_metric_tooltip_js():
    """Inject JavaScript for metric tooltip toggle functionality (hover + click/tap)."""
    st.markdown("""
    <script>
    (function() {
        // Track currently open tooltip
        let currentOpenTooltip = null;
        let currentOpenIcon = null;
        
        // Function to close tooltip
        function closeTooltip() {
            if (currentOpenTooltip) {
                currentOpenTooltip.classList.remove('visible');
            }
            if (currentOpenIcon) {
                currentOpenIcon.classList.remove('active');
            }
            currentOpenTooltip = null;
            currentOpenIcon = null;
            
            // Remove backdrop on mobile
            const backdrop = document.getElementById('metric-tooltip-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
            document.body.style.overflow = '';
        }
        
        // Function to toggle tooltip visibility
        function toggleTooltip(tooltipId, iconElement) {
            const tooltip = document.getElementById(tooltipId);
            if (!tooltip) {
                console.warn('Tooltip not found:', tooltipId);
                return;
            }
            
            // If this tooltip is already open, close it
            if (tooltip.classList.contains('visible')) {
                closeTooltip();
            } else {
                // Close any other open tooltip first
                if (currentOpenTooltip && currentOpenTooltip !== tooltip) {
                    closeTooltip();
                }
                
                // Open this tooltip
                tooltip.classList.add('visible');
                if (iconElement) {
                    iconElement.classList.add('active');
                }
                currentOpenTooltip = tooltip;
                currentOpenIcon = iconElement;
                
                // Add backdrop on mobile
                const isMobile = window.innerWidth <= 768;
                if (isMobile) {
                    let backdrop = document.getElementById('metric-tooltip-backdrop');
                    if (!backdrop) {
                        backdrop = document.createElement('div');
                        backdrop.id = 'metric-tooltip-backdrop';
                        backdrop.addEventListener('click', function(e) {
                            e.stopPropagation();
                            closeTooltip();
                        });
                        document.body.appendChild(backdrop);
                    }
                    document.body.style.overflow = 'hidden';
                }
            }
        }
        
        // Expose function globally
        window.toggleMetricTooltip = toggleTooltip;
        
        // Use event delegation for dynamically added elements
        document.addEventListener('click', function(e) {
            const icon = e.target.closest('.metric-info-icon');
            if (icon) {
                e.preventDefault();
                e.stopPropagation();
                const tooltipId = icon.getAttribute('data-tooltip-id');
                if (tooltipId) {
                    toggleTooltip(tooltipId, icon);
                }
            }
        });
        
        // Close tooltip when clicking outside (desktop)
        document.addEventListener('click', function(e) {
            if (window.innerWidth > 768 && currentOpenTooltip) {
                const isTooltip = e.target.closest('.metric-tooltip');
                const isIcon = e.target.closest('.metric-info-icon');
                
                if (!isTooltip && !isIcon) {
                    closeTooltip();
                }
            }
        });
        
        // Close tooltip on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && currentOpenTooltip) {
                closeTooltip();
            }
        });
        
        // Keyboard support for info icons
        document.addEventListener('keydown', function(e) {
            if ((e.key === 'Enter' || e.key === ' ') && e.target.classList.contains('metric-info-icon')) {
                e.preventDefault();
                const tooltipId = e.target.getAttribute('data-tooltip-id');
                if (tooltipId) {
                    toggleTooltip(tooltipId, e.target);
                }
            }
        });
        
        // Create popup overlay if it doesn't exist (for detailed popup - optional)
        if (!document.getElementById('metric-popup-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'metric-popup-overlay';
            overlay.className = 'metric-popup-overlay';
            overlay.innerHTML = `
                <div class="metric-popup-content">
                    <button class="metric-popup-close" onclick="closeMetricPopup()">×</button>
                    <div id="metric-popup-body"></div>
                </div>
            `;
            document.body.appendChild(overlay);
            
            overlay.addEventListener('click', function(e) {
                if (e.target === overlay) {
                    closeMetricPopup();
                }
            });
        }
        
        // Function to show detailed popup (optional - for future use)
        window.showMetricPopup = function(title, description, formula, insight) {
            const overlay = document.getElementById('metric-popup-overlay');
            const body = document.getElementById('metric-popup-body');
            
            body.innerHTML = `
                <div class="metric-popup-title">${title}</div>
                <div class="metric-popup-section">
                    <div class="metric-popup-section-label">Description</div>
                    <div class="metric-popup-section-content">${description}</div>
                </div>
                <div class="metric-popup-section">
                    <div class="metric-popup-section-label">Formula</div>
                    <div class="metric-popup-section-content">
                        <div class="metric-popup-formula">${formula}</div>
                    </div>
                </div>
                <div class="metric-popup-section">
                    <div class="metric-popup-section-label">Why This Matters</div>
                    <div class="metric-popup-section-content">${insight}</div>
                </div>
            `;
            
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        };
        
        window.closeMetricPopup = function() {
            const overlay = document.getElementById('metric-popup-overlay');
            if (overlay) {
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        };
    })();
    </script>
    """, unsafe_allow_html=True)


def kpi_card(label, value, prefix="", metric_key=None, explanation=None):
    """
    Render a metric card with tooltip and info icon.
    
    Args:
        label: Display label for the metric
        value: Metric value
        prefix: Prefix for value (e.g., "€ ")
        metric_key: Key to look up in METRIC_INFO dictionary
        explanation: Optional explanation override (for backward compatibility)
    """
    # Format nicely: ints no decimals, floats 2 decimals
    if isinstance(value, bool):
        value_str = f"{prefix}{value}"
    elif isinstance(value, int):
        value_str = f"{prefix}{value:,}"
    elif isinstance(value, float):
        value_str = f"{prefix}{value:,.2f}"
    else:
        value_str = f"{prefix}{value}"
    
    # Get metric info
    metric_info = {}
    if metric_key:
        metric_info = get_metric_info(metric_key)
    elif label:
        # Try to find by label
        metric_info = get_metric_info(label)
    
    # Use explanation from metric_info if available, otherwise use provided explanation
    description = metric_info.get("description", explanation or "Metric information not available.")
    formula = metric_info.get("formula", "Formula not available.")
    insight = metric_info.get("insight", "This metric helps track performance.")
    
    # Generate unique ID for this metric card and tooltip
    import hashlib
    card_id = f"metric-{hashlib.md5(label.encode()).hexdigest()[:8]}"
    tooltip_id = f"tooltip-{hashlib.md5(label.encode()).hexdigest()[:8]}"
    icon_id = f"icon-{hashlib.md5(label.encode()).hexdigest()[:8]}"
    
    # Escape HTML in text content
    def escape_html(text):
        if text is None:
            return ""
        return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")
    
    st.markdown(
        f"""
        <div class="metric-card-container" id="{card_id}">
            <div class="metric-info-icon" id="{icon_id}" data-tooltip-id="{tooltip_id}" title="Click for detailed information" role="button" aria-label="Show metric information" tabindex="0">i</div>
            <div class="metric-tooltip" id="{tooltip_id}">
                <div class="metric-tooltip-title">{escape_html(label)}</div>
                <div class="metric-tooltip-formula">{escape_html(formula)}</div>
                <div class="metric-tooltip-insight">{escape_html(insight)}</div>
            </div>
            <div style="font-size:0.9rem;color:#ccc;">{escape_html(label)}</div>
            <div style="font-size:1.5rem;font-weight:600;margin-top:0.3rem;color:#fff;">
                {escape_html(value_str)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_metric_section(metric_key: str) -> str:
    """Find which section a metric belongs to."""
    for section, metrics in METRIC_SECTIONS.items():
        if metric_key in metrics:
            return section
    return "Other"


def load_custom_metrics() -> list[str]:
    """
    Load custom metrics from JSON file.
    Returns empty list if file doesn't exist or is invalid.
    """
    if CUSTOM_METRICS_FILE.exists():
        try:
            with open(CUSTOM_METRICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Validate it's a list of strings
                if isinstance(data, list):
                    return [str(m) for m in data if isinstance(m, str)]
        except (json.JSONDecodeError, IOError, Exception) as e:
            # If file is corrupted or can't be read, return empty list
            st.warning(f"Could not load custom metrics: {e}")
            return []
    return []


def save_custom_metrics(metrics: list[str]) -> None:
    """
    Save custom metrics to JSON file.
    Filters out invalid metric keys before saving.
    """
    try:
        # Validate metrics are strings
        valid_metrics = [str(m) for m in metrics if isinstance(m, str)]
        with open(CUSTOM_METRICS_FILE, "w", encoding="utf-8") as f:
            json.dump(valid_metrics, f, indent=2, ensure_ascii=False)
    except (IOError, Exception) as e:
        st.error(f"Could not save custom metrics: {e}")


def initialize_custom_metrics():
    """
    Initialize session state for custom metrics.
    Loads from JSON file on first run, then uses session state for performance.
    """
    if "custom_metrics" not in st.session_state:
        # Load from persistent storage
        st.session_state["custom_metrics"] = load_custom_metrics()


def load_custom_graphs() -> list[dict]:
    """
    Load custom graphs from JSON file.
    Returns empty list if file doesn't exist or is invalid.
    """
    if CUSTOM_GRAPHS_FILE.exists():
        try:
            with open(CUSTOM_GRAPHS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Validate it's a list of dicts
                if isinstance(data, list):
                    return [g for g in data if isinstance(g, dict) and "name" in g and "metric_key" in g and "layout" in g]
        except (json.JSONDecodeError, IOError, Exception) as e:
            # If file is corrupted or can't be read, return empty list
            st.warning(f"Could not load custom graphs: {e}")
            return []
    return []


def save_custom_graphs(graphs: list[dict]) -> None:
    """
    Save custom graphs to JSON file.
    Filters out invalid graph definitions before saving.
    """
    try:
        # Validate graphs are dicts with required fields
        valid_graphs = []
        for g in graphs:
            if isinstance(g, dict) and "name" in g and "metric_key" in g and "layout" in g:
                # Ensure layout is valid; metric_key can be any known or future metric
                # (including time-series keys like CHART_METRIC_KEYS or KPI keys from METRIC_INFO)
                if g["layout"] in CHART_LAYOUTS and isinstance(g["metric_key"], str):
                    valid_graphs.append(g)
        
        with open(CUSTOM_GRAPHS_FILE, "w", encoding="utf-8") as f:
            json.dump(valid_graphs, f, indent=2, ensure_ascii=False)
    except (IOError, Exception) as e:
        st.error(f"Could not save custom graphs: {e}")


def initialize_custom_graphs():
    """
    Initialize session state for custom graphs.
    Loads from JSON file on first run, then uses session state for performance.
    """
    if "custom_graphs" not in st.session_state:
        # Load from persistent storage
        st.session_state["custom_graphs"] = load_custom_graphs()


# ========== REPORTS SYSTEM ==========

# Built-in report templates
BUILT_IN_REPORT_TEMPLATES = {
    "Monthly Performance Summary": {
        "name": "Monthly Performance Summary",
        "description": "Core KPIs for a selected month or date range",
        "metrics": [
            "Reservations",
            "Total nights",
            "Total revenue (€)",
            "Net Profit (€)",
            "Occupancy (%)",
            "Average price per night (€)",
            "Revenue per Available Night (€)",
            "Average Daily Rate (€)",
            "Profit Margin (%)",
        ],
        "filters": {
            "period_type": "month_year",  # month_year, date_range
            "platform": "Overall",  # Overall, Airbnb, Booking.com
        },
        "charts": ["monthly_revenue_line"],
        "is_builtin": True,
    },
    "Platform Comparison": {
        "name": "Platform Comparison",
        "description": "Compare Airbnb vs Booking.com performance",
        "metrics": [
            "Airbnb revenue (€)",
            "Booking.com revenue (€)",
            "Airbnb nights",
            "Booking.com nights",
            "Airbnb ADR (€)",
            "Booking.com ADR (€)",
            "Airbnb RevPAR (€)",
            "Booking.com RevPAR (€)",
            "Platform Profitability Difference (€)",
            "Airbnb share of revenue (%)",
            "Booking.com share of revenue (%)",
        ],
        "filters": {
            "period_type": "date_range",
            "platform": "Overall",
        },
        "charts": ["platform_comparison_bar", "platform_comparison_table"],
        "is_builtin": True,
    },
    "Profitability & Cost Breakdown": {
        "name": "Profitability & Cost Breakdown",
        "description": "Detailed profitability analysis with cost breakdown",
        "metrics": [
            "Profit Margin (%)",
            "Profit per Night (€)",
            "Profit per Stay (€)",
            "Cost per Reservation (€)",
            "Average Cost per Night (€)",
            "Variable vs Fixed Cost Ratio",
            "Total Fixed Costs (€)",
            "Total Per-Stay Expenses (€)",
            "Transportation Cost per Stay (€)",
            "Laundry Cost per Stay (€)",
            "Consumable Cost per Stay (€)",
            "Bank Fees per Stay (€)",
        ],
        "filters": {
            "period_type": "date_range",
            "platform": "Overall",
        },
        "charts": ["cost_breakdown_pie"],
        "is_builtin": True,
    },
    "Seasonality & Trends": {
        "name": "Seasonality & Trends",
        "description": "Revenue trends and seasonality analysis",
        "metrics": [
            "Best month by revenue",
            "Worst Month by Revenue (€)",
            "Month-over-Month Revenue Change (%)",
            "Year-over-Year Revenue Change (%)",
            "3-Month Moving Average Revenue (€)",
            "Seasonal Index",
            "Projected next-year revenue",
            "Projected Next-Year Revenue (Weighted)",
        ],
        "filters": {
            "period_type": "date_range",
            "platform": "Overall",
        },
        "charts": ["monthly_revenue_line", "revenue_heatmap"],
        "is_builtin": True,
    },
    "Guest Profile Snapshot": {
        "name": "Guest Profile Snapshot",
        "description": "Guest demographics and behavior insights",
        "metrics": [
            "Average group size",
            "Baby Crib usage (%)",
            "Sofa Bed usage (%)",
            "Parking Usage (%)",
            "Top Countries by Bookings",
            "Top Countries by Revenue",
            "Average Revenue per Stay (€)",
            "Revenue per Guest (€)",
        ],
        "filters": {
            "period_type": "date_range",
            "platform": "Overall",
        },
        "charts": [],
        "is_builtin": True,
    },
}


def load_report_templates() -> Dict[str, Dict]:
    """Load user-defined report templates from JSON file."""
    if REPORT_TEMPLATES_FILE.exists():
        try:
            with open(REPORT_TEMPLATES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Filter out corrupted templates (must have 'name' and 'metrics')
                    cleaned = {}
                    for key, template in data.items():
                        if isinstance(template, dict) and 'name' in template and 'metrics' in template:
                            cleaned[key] = template
                        else:
                            # Skip corrupted template
                            continue
                    return cleaned
        except (json.JSONDecodeError, IOError, Exception) as e:
            st.warning(f"Could not load report templates: {e}")
            return {}
    return {}


def save_report_templates(templates: Dict[str, Dict]) -> None:
    """Save user-defined report templates to JSON file."""
    try:
        # Ensure directory exists
        REPORT_TEMPLATES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_TEMPLATES_FILE, "w", encoding="utf-8") as f:
            json.dump(templates, f, indent=2, ensure_ascii=False)
    except (IOError, Exception) as e:
        st.error(f"Could not save report templates: {e}")


def delete_template(template_name: str) -> bool:
    """
    Delete a custom template by name.
    Returns True if deleted successfully, False otherwise.
    Only deletes user-created templates, not built-in ones.
    """
    # Safety check: never delete built-in templates
    if template_name in BUILT_IN_REPORT_TEMPLATES:
        st.error(f"Cannot delete built-in template '{template_name}'")
        return False
    
    try:
        user_templates = load_report_templates()
        if template_name in user_templates:
            del user_templates[template_name]
            save_report_templates(user_templates)
            return True
        else:
            st.warning(f"Template '{template_name}' not found")
            return False
    except Exception as e:
        st.error(f"Error deleting template: {e}")
        return False


def get_all_report_templates() -> Dict[str, Dict]:
    """Get all report templates (built-in + user-defined)."""
    builtin = BUILT_IN_REPORT_TEMPLATES.copy()
    user_templates = load_report_templates()
    return {**builtin, **user_templates}


def generate_report_html_content(
    template: Dict[str, Any],
    metric_info: Dict[str, Dict],
    filter_params: Dict[str, Any],
    generated_time: str,
) -> str:
    """
    Generate HTML content for a report that can be downloaded or converted to PDF.
    This works within Streamlit's constraints - generates clean HTML that can be
    downloaded and opened in a browser or converted to PDF externally.
    """
    # Build filter info string
    filter_info = []
    if filter_params.get("period_type") == "month_year":
        month_name = calendar.month_name[filter_params.get("month", 1)]
        filter_info.append(f"Period: {month_name} {filter_params.get('year', 'N/A')}")
    elif filter_params.get("period_type") == "date_range":
        start = filter_params.get("start_date", "")
        end = filter_params.get("end_date", "")
        filter_info.append(f"Period: {start} to {end}")
    elif filter_params.get("period_type") == "year":
        filter_info.append(f"Year: {filter_params.get('year', 'N/A')}")
    
    if filter_params.get("platform") and filter_params["platform"] != "Overall":
        filter_info.append(f"Platform: {filter_params['platform']}")
    
    filter_str = " | ".join(filter_info) if filter_info else "All data"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{template['name']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1f77b4;
            border-bottom: 3px solid #1f77b4;
            padding-bottom: 10px;
        }}
        .metadata {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 30px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .metric-card {{
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 15px;
            background-color: #fafafa;
            transition: box-shadow 0.2s;
        }}
        .metric-card:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .metric-label {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 5px;
        }}
        .metric-explanation {{
            font-size: 0.8em;
            color: #999;
            font-style: italic;
        }}
        .section-title {{
            font-size: 1.3em;
            color: #333;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 4px solid #1f77b4;
            padding-left: 10px;
        }}
        @media print {{
            body {{
                background-color: white;
                margin: 20px;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{template['name']}</h1>
        <div class="metadata">
            <strong>Generated:</strong> {generated_time}<br>
            <strong>Filters:</strong> {filter_str}
        </div>
        
        <div class="section-title">Key Metrics</div>
        <div class="metrics-grid">
"""
    
    # Add metrics
    metric_keys = template.get("metrics", [])
    for metric_key in metric_keys:
        if metric_key in metric_info:
            mi = metric_info[metric_key]
            value_str = str(mi["value"])
            if isinstance(mi["value"], (int, float)):
                if isinstance(mi["value"], int):
                    value_str = f"{mi['value']:,}"
                else:
                    value_str = f"{mi['value']:,.2f}"
            
            html += f"""
            <div class="metric-card">
                <div class="metric-label">{mi['label']}</div>
                <div class="metric-value">{mi['prefix']}{value_str}</div>
                <div class="metric-explanation">{mi['explanation']}</div>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html


# NOTE: Email export functionality removed from UI - function kept for potential future use
# Email export UI was removed due to SMTP configuration complexity and credential management requirements
def send_email_smtp(
    recipient_email: str,
    subject: str,
    body: str,
    html_content: str,
    smtp_server: str,
    smtp_port: int,
    sender_email: str,
    sender_password: str,
) -> Tuple[bool, str]:
    """
    Send email via SMTP with HTML content as attachment.
    Returns (success: bool, message: str)
    
    NOTE: This function is currently unused - email export UI was removed.
    This requires SMTP credentials. For Gmail, use an App Password.
    Works with any SMTP server (Gmail, Outlook, custom SMTP).
    """
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Add HTML as attachment
        attachment = MIMEBase('text', 'html')
        attachment.set_payload(html_content.encode('utf-8'))
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename=report.html',
        )
        msg.attach(attachment)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent successfully!"
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check your email and password (use App Password for Gmail)."
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


def filter_bookings_by_period(
    bookings: pd.DataFrame,
    period_type: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> pd.DataFrame:
    """Filter bookings based on period type and parameters."""
    df = clean_bookings(bookings.copy())
    
    if period_type == "month_year" and year is not None and month is not None:
        df = df[
            (df["Check-in Year"] == year) & (df["Check-in Month"] == month)
        ]
    elif period_type == "date_range" and start_date is not None and end_date is not None:
        df = df[
            (df["Check-in date"] >= pd.to_datetime(start_date)) &
            (df["Check-in date"] <= pd.to_datetime(end_date))
        ]
    elif period_type == "year" and year is not None:
        df = df[df["Check-in Year"] == year]
    
    return df


def filter_monthly_costs_by_period(
    monthly_costs: pd.DataFrame,
    period_type: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> pd.DataFrame:
    """
    Filter monthly_costs based on period type and parameters.
    
    For month_year: filter by year AND month
    For year: filter by year only (all months in that year)
    For date_range: filter by months that fall within the date range
    For no filter: return all monthly costs
    """
    df = monthly_costs.copy()
    
    # Find the month column (could be "Month", "Month (number)", etc.)
    month_col = None
    for col in df.columns:
        if "month" in col.lower() and "name" not in col.lower():
            month_col = col
            break
    
    if period_type == "month_year" and year is not None and month is not None:
        # Filter by both year AND month for monthly reports
        if month_col:
            df = df[
                (df["Year"] == year) & 
                (df[month_col] == month)
            ]
        else:
            # Fallback: if no month column found, filter by year only
            df = df[df["Year"] == year]
    
    elif period_type == "year" and year is not None:
        # For yearly reports, filter by year only (all months in that year)
        df = df[df["Year"] == year]
    
    elif period_type == "date_range" and start_date is not None and end_date is not None:
        # For date range, filter by months that fall within the date range
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        # Create a mask for months that fall within the date range
        mask = pd.Series([False] * len(df), index=df.index)
        
        if month_col and "Year" in df.columns:
            # Check each row to see if its year-month falls within the date range
            for idx, row in df.iterrows():
                try:
                    year_val = int(row["Year"])
                    month_val = int(row[month_col])
                    # Create a date for the first day of this month
                    month_date = pd.to_datetime(f"{year_val}-{month_val:02d}-01")
                    # Check if this month falls within the date range
                    if start_dt <= month_date <= end_dt:
                        mask.loc[idx] = True
                except (ValueError, TypeError):
                    continue
        
        df = df[mask]
    
    # If no filter or invalid parameters, return all monthly costs
    return df


def render_report(
    template: Dict[str, Any],
    bookings: pd.DataFrame,
    monthly_costs: pd.DataFrame,
    filter_params: Dict[str, Any],
) -> None:
    """Render a report based on template configuration."""
    st.markdown("---")
    st.markdown(f"## {template['name']}")
    
    # Report metadata
    generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"Generated: {generated_time}")
    
    # Show applied filters
    filter_info = []
    if filter_params.get("period_type") == "month_year":
        filter_info.append(f"Period: {calendar.month_name[filter_params.get('month', 1)]} {filter_params.get('year', 'N/A')}")
    elif filter_params.get("period_type") == "date_range":
        start = filter_params.get("start_date", "")
        end = filter_params.get("end_date", "")
        filter_info.append(f"Period: {start} to {end}")
    elif filter_params.get("period_type") == "year":
        filter_info.append(f"Year: {filter_params.get('year', 'N/A')}")
    
    if filter_params.get("platform") and filter_params["platform"] != "Overall":
        filter_info.append(f"Platform: {filter_params['platform']}")
    
    if filter_info:
        st.caption(" | ".join(filter_info))
    
    # Filter data
    bookings_filtered = filter_bookings_by_period(
        bookings,
        filter_params.get("period_type", "year"),
        filter_params.get("year"),
        filter_params.get("month"),
        filter_params.get("start_date"),
        filter_params.get("end_date"),
    )
    
    # Apply platform filter
    platform = filter_params.get("platform", "Overall")
    if platform != "Overall":
        bookings_filtered = bookings_filtered[
            bookings_filtered["Platform"].replace({"Booking": "Booking.com"}) == platform
        ]
    
    # Filter monthly costs using the helper function
    monthly_costs_filtered = filter_monthly_costs_by_period(
        monthly_costs,
        filter_params.get("period_type", "year"),
        filter_params.get("year"),
        filter_params.get("month"),
        filter_params.get("start_date"),
        filter_params.get("end_date"),
    )
    
    # Calculate nights available based on period type
    selected_year = filter_params.get("year")
    nights_available = compute_nights_available(
        bookings_filtered,
        selected_year=selected_year,
        period_type=filter_params.get("period_type"),
        month=filter_params.get("month"),
        start_date=filter_params.get("start_date"),
        end_date=filter_params.get("end_date"),
    )
    
    # Calculate metrics
    # Determine start_date and end_date for metrics calculation
    report_start_date = None
    report_end_date = None
    period_type = filter_params.get("period_type", "year")
    if period_type == "date_range":
        report_start_date = filter_params.get("start_date")
        report_end_date = filter_params.get("end_date")
        if report_start_date:
            report_start_date = pd.Timestamp(report_start_date)
        if report_end_date:
            report_end_date = pd.Timestamp(report_end_date)
    elif period_type == "year" and selected_year is not None:
        # For year selection, use year boundaries
        report_start_date = pd.Timestamp(year=selected_year, month=1, day=1)
        report_end_date = pd.Timestamp(year=selected_year, month=12, day=31)
    
    metric_info = calculate_all_metrics(
        bookings_filtered,
        monthly_costs_filtered,
        platform,
        nights_available,
        selected_year,
        start_date=report_start_date,
        end_date=report_end_date,
    )
    
    # Render metrics
    st.markdown("### Key Metrics")
    metric_keys = template.get("metrics", [])
    
    # Group metrics into columns
    cols = st.columns(3)
    for idx, metric_key in enumerate(metric_keys):
        if metric_key in metric_info:
            mi = metric_info[metric_key]
            with cols[idx % 3]:
                kpi_card(mi["label"], mi["value"], prefix=mi["prefix"], metric_key=metric_key, explanation=mi.get("explanation"))
                st.caption(mi["explanation"])
    
    # Render charts
    charts = template.get("charts", [])
    if charts:
        st.markdown("### Charts")
        
        for chart_type in charts:
            if chart_type == "monthly_revenue_line":
                monthly_revenue_data = monthly_revenue_by_platform(bookings_filtered)
                if platform == "Overall":
                    chart_df = monthly_revenue_data[["Airbnb", "Booking.com"]].copy()
                    chart_df["Total"] = chart_df["Airbnb"] + chart_df["Booking.com"]
                elif platform == "Airbnb":
                    chart_df = monthly_revenue_data[["Airbnb"]]
                else:
                    chart_df = monthly_revenue_data[["Booking.com"]]
                st.line_chart(chart_df)
                st.caption("Monthly revenue trend")
            
            elif chart_type == "platform_comparison_bar":
                monthly_revenue_data = monthly_revenue_by_platform(bookings_filtered)
                comparison_df = monthly_revenue_data[["Airbnb", "Booking.com"]]
                st.bar_chart(comparison_df)
                st.caption("Platform revenue comparison")
            
            elif chart_type == "platform_comparison_table":
                monthly_revenue_data = monthly_revenue_by_platform(bookings_filtered)
                comparison_df = monthly_revenue_data[["Airbnb", "Booking.com"]].copy()
                comparison_df["Difference"] = comparison_df["Airbnb"] - comparison_df["Booking.com"]
                st.dataframe(comparison_df.style.format("{:,.2f}"))
                st.caption("Platform comparison table")
            
            elif chart_type == "cost_breakdown_pie":
                # Cost breakdown pie chart
                reservations_count = metric_info.get("Reservations", {}).get("value", 0)
                if reservations_count > 0:
                    trans_cost = metric_info.get("Transportation Cost per Stay (€)", {}).get("value", 0)
                    laundry_cost = metric_info.get("Laundry Cost per Stay (€)", {}).get("value", 0)
                    supplies_cost = metric_info.get("Consumable Cost per Stay (€)", {}).get("value", 0)
                    bank_fees_cost = metric_info.get("Bank Fees per Stay (€)", {}).get("value", 0)
                    
                    cost_data = {
                        "Transportation": float(trans_cost * reservations_count),
                        "Laundry": float(laundry_cost * reservations_count),
                        "Consumables": float(supplies_cost * reservations_count),
                        "Bank Fees": float(bank_fees_cost * reservations_count),
                    }
                    cost_df = pd.DataFrame(list(cost_data.items()), columns=["Cost Type", "Amount"])
                    if cost_df["Amount"].sum() > 0:
                        cost_chart = (
                            alt.Chart(cost_df)
                            .mark_arc()
                            .encode(
                                theta=alt.Theta(field="Amount", type="quantitative"),
                                color=alt.Color(field="Cost Type", type="nominal"),
                                tooltip=["Cost Type", alt.Tooltip("Amount:Q", format=",.2f")],
                            )
                        )
                        st.altair_chart(cost_chart, use_container_width=True)
                        st.caption("Cost breakdown by type")
                else:
                    st.info("No cost data available for the selected period.")
            
            elif chart_type == "revenue_heatmap":
                heat_source = clean_bookings(bookings_filtered.copy())
                if "Platform" in heat_source.columns:
                    heat_source["platform_normalized"] = heat_source["Platform"].replace({"Booking": "Booking.com"})
                else:
                    heat_source["platform_normalized"] = "Unknown"
                
                if platform != "Overall":
                    heat_source = heat_source[heat_source["platform_normalized"] == platform]
                
                if (
                    "Check-in Year" in heat_source.columns
                    and "Check-in Month" in heat_source.columns
                    and "Revenue for stay (€)" in heat_source.columns
                    and not heat_source.empty
                ):
                    heat_source["Year"] = heat_source["Check-in Year"].astype(int)
                    heat_source["Month"] = heat_source["Check-in Month"].astype(int)
                    
                    heat_grouped = (
                        heat_source.groupby(["Year", "Month"])["Revenue for stay (€)"]
                        .sum()
                        .reset_index()
                    )
                    heat_grouped["MonthName"] = heat_grouped["Month"].apply(
                        lambda m: calendar.month_abbr[int(m)]
                    )
                    heat_grouped.rename(columns={"Revenue for stay (€)": "Revenue"}, inplace=True)
                    
                    heat_chart = (
                        alt.Chart(heat_grouped)
                        .mark_rect()
                        .encode(
                            x=alt.X("MonthName:O", title="Month"),
                            y=alt.Y("Year:O", title="Year"),
                            color=alt.Color("Revenue:Q", title="Revenue (€)", scale=alt.Scale(scheme="blues")),
                            tooltip=[
                                alt.Tooltip("Year:O", title="Year"),
                                alt.Tooltip("MonthName:O", title="Month"),
                                alt.Tooltip("Revenue:Q", title="Revenue (€)", format=",.2f"),
                            ],
                        )
                    )
                    st.altair_chart(heat_chart, use_container_width=True)
                    st.caption("Revenue heatmap by year and month")
    
    # Export section
    st.markdown("---")
    st.markdown("### Export Report")
    
    # Generate HTML content for export
    report_html = generate_report_html_content(
        template,
        metric_info,
        filter_params,
        generated_time,
    )
    
    # PDF/HTML Download - Works in Streamlit
    # NOTE: Streamlit cannot generate PDF directly without external libraries.
    # We provide HTML download which can be converted to PDF using browser's Print to PDF
    # or external tools. This is the most reliable approach in Streamlit.
    st.download_button(
        label="📄 Download Report (HTML)",
        data=report_html,
        file_name=f"{template['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        key=f"download_html_{template['name']}",
        help="Download as HTML file. Open in browser and use 'Print to PDF' for PDF version."
    )
    st.caption("💡 Tip: Open the HTML file in your browser and use 'Print to PDF' for PDF format")
    
    # Note: Email and Google Drive export functionality removed from UI
    # Email export (send_email_smtp) and Google Drive upload were removed due to:
    # - Email: Requires SMTP configuration and credentials management
    # - Google Drive: OAuth 2.0 complexity in Streamlit (redirect URLs, service accounts, token management)
    # Users can download HTML and manually share via email or upload to Drive


# ========== MAIN APP ==========

bookings, monthly_costs, toiletries = load_data(FILE_PATH)

# Inject metric tooltip CSS and JS (once at startup)
inject_metric_tooltip_css()
inject_metric_tooltip_js()
# Inject responsive CSS for mobile devices
inject_responsive_css()

# Sidebar navigation header
# Render Lynx logo
if LYNX_LOGO_LIGHT.exists():
    col_left, col_center, col_right = st.sidebar.columns([1, 2, 1])
    with col_center:
        # Responsive logo - use container width for better mobile support
        st.image(str(LYNX_LOGO_LIGHT), use_container_width=True)
else:
    st.sidebar.markdown("🏡")  # Fallback if logo file is missing

# Title веднаш под логото, малку на лево и одделено од менито
st.sidebar.markdown(
    """
    <h2 style="
        margin: 0 0 0.8rem 6px;
        padding: 0;
        text-align: center;
    ">
        Lynx Apartment
    </h2>
    """,
    unsafe_allow_html=True,
)

# мал вертикален space пред „Navigation“
st.sidebar.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)








# Persist active page in session state
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Dashboard"

# Get page selection, defaulting to session state value
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Bookings", "Expenses", "Reports"],
    index=["Dashboard", "Bookings", "Expenses", "Reports"].index(st.session_state["active_page"]) if st.session_state["active_page"] in ["Dashboard", "Bookings", "Expenses", "Reports"] else 0,
)

# Update session state when page changes
st.session_state["active_page"] = page
st.sidebar.markdown("---")
st.sidebar.caption("Data source: Lynx Apartment Tracker.xlsx")

# -------- DASHBOARD --------

if page == "Dashboard":
    # Reserve a container at the very top for the page header (Dashboard + Target)
    header_container = st.container()

    view_mode = st.segmented_control(
        "View mode",
        options=["Overall", "Airbnb", "Booking.com", "Comparison"],
        default="Overall",
    )

    # -------- DATE FILTERS (YEAR + OPTIONAL CUSTOM RANGE) --------
    # Available years (for year-based filter)
    available_years_bookings = (
        bookings["Check-in Year"].dropna().astype(int).sort_values().unique()
        if "Check-in Year" in bookings.columns
        else []
    )
    available_years_costs = (
        monthly_costs["Year"].dropna().astype(int).sort_values().unique()
        if "Year" in monthly_costs.columns
        else []
    )

    all_years = sorted(set(available_years_bookings) | set(available_years_costs))
    year_options = ["All", "Custom range"] + [str(y) for y in all_years]

    selected_year = st.selectbox("Select period", year_options, index=0)

    # Compute default custom date range: earliest check-in to latest check-out
    start_date_default = None
    end_date_default = None
    if "Check-in date" in bookings.columns and not bookings["Check-in date"].dropna().empty:
        earliest_check_in = bookings["Check-in date"].min()
        if pd.notna(earliest_check_in):
            start_date_default = earliest_check_in.date()
    if "Check-out date" in bookings.columns and not bookings["Check-out date"].dropna().empty:
        latest_check_out = bookings["Check-out date"].max()
        if pd.notna(latest_check_out):
            end_date_default = latest_check_out.date()

    # Custom range is a special option in the same dropdown
    use_custom_range = selected_year == "Custom range"

    start_date = None
    end_date = None

    if use_custom_range:
        c_start, c_end = st.columns(2)
        with c_start:
            start_date = st.date_input(
                "Start date",
                value=start_date_default,
                format="DD-MM-YYYY",
                key="dashboard_start_date",
            )
        with c_end:
            end_date = st.date_input(
                "End date",
                value=end_date_default,
                format="DD-MM-YYYY",
                key="dashboard_end_date",
            )

    # Decide which filter to apply
    if use_custom_range and start_date is not None and end_date is not None:
        # Custom date range overrides year selection
        selected_year_int = None
        bookings_filtered = filter_bookings_by_period(
            bookings,
            period_type="date_range",
            start_date=start_date,
            end_date=end_date,
        )
        monthly_costs_filtered = filter_monthly_costs_by_period(
            monthly_costs,
            period_type="date_range",
            start_date=start_date,
            end_date=end_date,
        )
        nights_available = compute_nights_available(
            bookings_filtered,
            selected_year=None,
            period_type="date_range",
            start_date=start_date,
            end_date=end_date,
        )
    else:
        # Fall back to year selection logic
        if selected_year not in ["All", "Custom range"]:
            selected_year_int = int(selected_year)
            bookings_filtered = filter_bookings_by_period(
                bookings,
                period_type="year",
                year=selected_year_int,
            )
            monthly_costs_filtered = filter_monthly_costs_by_period(
                monthly_costs,
                period_type="year",
                year=selected_year_int,
            )
            nights_available = compute_nights_available(
                bookings_filtered,
                selected_year=selected_year_int,
                period_type="year",
            )
        else:
            selected_year_int = None
            bookings_filtered = bookings
            # For "All" years, use all monthly costs (no filter)
            monthly_costs_filtered = monthly_costs
            nights_available = compute_nights_available(bookings_filtered, None)

    # ===== TARGET REVENUE HEADER ROW (renders at very top via header_container) =====
    with header_container:
        # Total revenue for the currently selected period (year or custom range)
        total_revenue_period = 0.0
        if "Revenue for stay (€)" in bookings_filtered.columns:
            total_revenue_period = float(
                bookings_filtered["Revenue for stay (€)"].fillna(0).sum()
            )

        # Match KPI card width by using a narrower right column
        header_left, header_right = st.columns([2, 1])

        with header_left:
            st.title("📊 Dashboard")

        with header_right:
            # Card-like Target block - simplified without wrapper div
            st.markdown(
                "<div style='font-size:0.75rem; color:#9CA3AF; text-transform:uppercase; "
                "letter-spacing:0.06em; margin-bottom:0.15rem;'>Target (€)</div>",
                unsafe_allow_html=True,
            )

            # Compact input (no visible label) inside the card
            # Initialize default value in session_state if not present
            if "target_revenue" not in st.session_state:
                st.session_state["target_revenue"] = 5000.0  # default EUR target
            
            # Use key only - Streamlit automatically uses session_state value
            target = st.number_input(
                label="",
                min_value=0.0,
                step=100.0,
                key="target_revenue",
                label_visibility="collapsed",
                format="%.0f",
            )

            # Compute progress
            if target > 0:
                progress_pct = (total_revenue_period / target) * 100.0
                # Clamp visual progress to 100% max
                display_pct = max(0.0, min(progress_pct, 100.0))

                # Strong, high-contrast progress bar + bold percentage
                st.markdown(
                    f"""
                    <div style="margin-top:0.4rem; height:6px; border-radius:999px; 
                                background-color:#020617; border:1px solid #1f2937;">
                        <div style="
                            height:100%;
                            width:{display_pct}%;
                            border-radius:999px;
                            background:linear-gradient(90deg,#22C55E,#A3E635);
                            transition:width 0.3s ease-out;
                        "></div>
                    </div>
                    <div style="font-size:0.9rem; color:#F9FAFB; margin-top:0.35rem; font-weight:700;">
                        {progress_pct:.1f}% of target
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                # No target set: just show text, no bar
                st.markdown(
                    """
                    <div style="font-size:0.85rem; color:#F9FAFB; margin-top:0.75rem; font-weight:600;">
                        No target set
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if view_mode != "Comparison":
        # Initialize custom metrics session state
        initialize_custom_metrics()
        # Initialize custom graphs session state
        initialize_custom_graphs()

        # Calculate all metrics using the comprehensive function
        # Determine start_date and end_date for metrics calculation
        metrics_start_date = None
        metrics_end_date = None
        if use_custom_range and start_date is not None and end_date is not None:
            metrics_start_date = pd.Timestamp(start_date)
            metrics_end_date = pd.Timestamp(end_date)
        elif selected_year_int is not None:
            # For year selection, use year boundaries
            metrics_start_date = pd.Timestamp(year=selected_year_int, month=1, day=1)
            metrics_end_date = pd.Timestamp(year=selected_year_int, month=12, day=31)
        
        metric_info = calculate_all_metrics(
            bookings_filtered,
            monthly_costs_filtered,
            view_mode,
            nights_available,
            selected_year_int,
            start_date=metrics_start_date,
            end_date=metrics_end_date,
        )

        # ----- Show core metrics -----
        st.markdown("### KPI overview")

        core_keys = [
            "Reservations",
            "Total nights",
            "Occupancy (%)",
            "Total revenue (€)",
            "Net Profit (€)",
            "Average price per night (€)",
            "Average Monthly Gross Income (€)",
            "Average Monthly Net Income (€)",
        ]

        core_columns = st.columns(3)
        for idx, key in enumerate(core_keys):
            if key not in metric_info:
                continue
            mi = metric_info[key]
            with core_columns[idx % 3]:
                kpi_card(mi["label"], mi["value"], prefix=mi["prefix"], metric_key=key, explanation=mi.get("explanation"))
                st.caption(mi["explanation"])

        # ----- Custom Metrics Section -----
        st.markdown("---")
        st.markdown("#### ⭐ Custom Metrics")
        
        # Get all available metric keys (including core keys so they can be added to Custom Metrics too)
        all_metric_keys = [k for k in metric_info.keys()]
        
        # Filter out invalid metrics from custom_metrics (metrics that no longer exist)
        valid_custom_metrics = [k for k in st.session_state["custom_metrics"] if k in metric_info]
        if len(valid_custom_metrics) != len(st.session_state["custom_metrics"]):
            # Some metrics were removed from code, update session state and save
            st.session_state["custom_metrics"] = valid_custom_metrics
            save_custom_metrics(valid_custom_metrics)
        
        # Custom metrics management UI
        with st.expander("Manage Custom Metrics", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Add metrics to Custom section:**")
                # Show metrics grouped by section for easy selection
                available_to_add = [k for k in all_metric_keys if k not in valid_custom_metrics]
                if available_to_add:
                    metric_to_add = st.selectbox(
                        "Select metric to add",
                        options=[""] + available_to_add,
                        format_func=lambda x: f"{x} ({get_metric_section(x)})" if x else "Choose a metric...",
                        key="add_custom_metric",
                    )
                    if metric_to_add and st.button("➕ Add to Custom"):
                        if metric_to_add not in st.session_state["custom_metrics"]:
                            st.session_state["custom_metrics"].append(metric_to_add)
                            save_custom_metrics(st.session_state["custom_metrics"])
                            st.rerun()
                else:
                    st.info("All metrics are already in Custom section.")
            
            with col2:
                st.markdown("**Remove metrics from Custom section:**")
                if valid_custom_metrics:
                    metrics_to_remove = st.multiselect(
                        "Select metrics to remove",
                        options=valid_custom_metrics,
                        format_func=lambda x: f"{x} ({get_metric_section(x)})",
                        key="remove_custom_metrics",
                    )
                    if metrics_to_remove and st.button("➖ Remove from Custom"):
                        st.session_state["custom_metrics"] = [
                            k for k in st.session_state["custom_metrics"] 
                            if k not in metrics_to_remove
                        ]
                        save_custom_metrics(st.session_state["custom_metrics"])
                        st.rerun()
                    
                    # Reorder Custom metrics
                    st.markdown("**Reorder Custom metrics:**")
                    custom_df = pd.DataFrame({
                        "Metric": valid_custom_metrics,
                        "Section": [get_metric_section(k) for k in valid_custom_metrics],
                        "Order": range(len(valid_custom_metrics)),
                    })
                    edited_df = st.data_editor(
                        custom_df,
                        column_config={
                            "Metric": st.column_config.SelectboxColumn(
                                "Metric",
                                options=all_metric_keys,
                                required=True,
                            ),
                            "Section": st.column_config.TextColumn("Section", disabled=True),
                            "Order": st.column_config.NumberColumn("Order", min_value=0, step=1),
                        },
                        use_container_width=True,
                        num_rows="dynamic",
                        key="custom_metrics_editor",
                    )
                    
                    if st.button("💾 Save Custom Order"):
                        # Sort by Order and update session state
                        edited_df = edited_df.sort_values("Order")
                        new_order = edited_df["Metric"].tolist()
                        # Filter out any invalid metrics
                        new_order = [k for k in new_order if k in metric_info]
                        st.session_state["custom_metrics"] = new_order
                        save_custom_metrics(new_order)
                        st.rerun()
                    
                    if st.button("🗑️ Clear All Custom Metrics"):
                        st.session_state["custom_metrics"] = []
                        save_custom_metrics([])
                        st.rerun()
                else:
                    st.info("No custom metrics yet. Add metrics from the left panel.")

        # Display Custom metrics (always show if they exist, independent of More Metrics selection)
        if valid_custom_metrics:
            custom_columns = st.columns(3)
            for idx, key in enumerate(valid_custom_metrics):
                mi = metric_info[key]
                # Append section name in parentheses for custom metrics
                original_section = get_metric_section(key)
                display_label = f"{mi['label']} ({original_section})" if original_section != "Custom" else mi['label']
                with custom_columns[idx % 3]:
                    kpi_card(display_label, mi["value"], prefix=mi["prefix"], metric_key=key, explanation=mi.get("explanation"))
                    st.caption(mi["explanation"])
        else:
            st.info("⭐ No custom metrics configured. Use 'Manage Custom Metrics' above to add your favorite metrics here.")

        # ----- More Metrics Section -----
        st.markdown("---")
        st.markdown("#### 📊 More Metrics")
        
        # Get selected metrics per section (stored in session state for persistence across expander toggle)
        if "more_metrics_selected" not in st.session_state:
            st.session_state["more_metrics_selected"] = {}

        # Global metric search input state (for autocomplete-style filtering).
        if "metric_search" not in st.session_state:
            st.session_state["metric_search"] = ""

        # Helper: filter metrics based on a search query (by metric key/label, case-insensitive, partial match)
        def filter_metrics_by_search(metric_keys, search_query):
            if not search_query:
                return metric_keys
            q = search_query.lower()
            filtered = []
            for mk in metric_keys:
                meta = metric_info.get(mk, {})
                label = str(meta.get("label", mk))
                if q in mk.lower() or q in label.lower():
                    filtered.append(mk)
            return filtered

        # Helper used conceptually as requested: filter over "all_metrics" style structures
        def filter_metrics(query, all_metrics):
            """
            Given a search query and a list of metric dicts with a 'name' field,
            return only those whose name matches the query (case-insensitive, partial).
            """
            if not query:
                return all_metrics
            q = query.lower()
            return [m for m in all_metrics if q in str(m.get("name", "")).lower()]
        
        # More Metrics expander - contains the selection UI
        with st.expander("Select additional metrics to display", expanded=False):
            # Build a master list of all available metrics across sections (excluding Custom)
            all_available_metrics = []  # list[tuple[str, str]] -> (section_name, metric_key)
            for section_name in METRIC_SECTIONS.keys():
                if section_name == "Custom":
                    continue
                section_metrics = METRIC_SECTIONS[section_name]
                available_section_metrics = [m for m in section_metrics if m in metric_info]
                if not available_section_metrics:
                    continue
                available_section_metrics = [m for m in available_section_metrics if m not in valid_custom_metrics]
                if not available_section_metrics:
                    continue
                for mk in available_section_metrics:
                    all_available_metrics.append((section_name, mk))

            # --- REAL-TIME AUTOCOMPLETE SEARCH FIELD ---
            search_query = st.text_input(
                "Search metrics",
                key="metric_search",
                placeholder="Type to search...",
            )

            # Detect character-by-character changes and force rerun
            if "metric_search_prev" not in st.session_state:
                st.session_state["metric_search_prev"] = ""

            if st.session_state["metric_search_prev"] != search_query:
                st.session_state["metric_search_prev"] = search_query
                st.rerun()

            current_search = search_query.lower().strip()

            # ---- Autocomplete Suggestions ----
            suggestion_container = st.container()
            with suggestion_container:
                suggestions = []
                if current_search:
                    q = current_search
                    for section_name, metric_key in all_available_metrics:
                        meta = metric_info.get(metric_key, {})
                        label = str(meta.get("label", metric_key))
                        if q in metric_key.lower() or q in label.lower():
                            suggestions.append((section_name, metric_key, label))

                max_suggestions = 8
                suggestions = suggestions[:max_suggestions]

                if suggestions:
                    st.caption("Suggestions:")
                    for section_name, metric_key, label in suggestions:
                        section_label = SECTION_DISPLAY_NAMES.get(section_name, section_name)
                        button_label = f"{label} · {section_label}"
                        if st.button(button_label, key=f"suggest_{section_name}_{metric_key}"):
                            # Auto-select this metric in its category and rerun
                            current_selected = st.session_state["more_metrics_selected"].get(section_name, [])
                            if metric_key not in current_selected:
                                current_selected.append(metric_key)
                            st.session_state["more_metrics_selected"][section_name] = current_selected
                            st.rerun()
                elif current_search:
                    st.caption("No matching metrics found.")

            # Get selected metrics per section
            selected_metrics_by_section = {}
            # current_search already derived above from session_state
            
            # Iterate through sections (excluding Custom)
            for section_name in METRIC_SECTIONS.keys():
                if section_name == "Custom":
                    continue
                
                section_metrics = METRIC_SECTIONS[section_name]
                # Filter to only metrics that exist in metric_info
                available_section_metrics = [m for m in section_metrics if m in metric_info]
                
                if not available_section_metrics:
                    continue
                
                # Skip metrics that are in Custom section (they're already shown above)
                available_section_metrics = [m for m in available_section_metrics if m not in valid_custom_metrics]
                
                if not available_section_metrics:
                    continue
                
                # Apply global search filter
                filtered_section_metrics = filter_metrics_by_search(available_section_metrics, current_search)
                
                st.markdown(f"##### {SECTION_DISPLAY_NAMES.get(section_name, section_name)}")
                
                # Preserve previously selected metrics even if they are currently filtered out
                selected_in_section = st.session_state["more_metrics_selected"].get(section_name, []).copy()

                if not filtered_section_metrics:
                    st.caption("No results for this category with the current search.")
                    selected_metrics_by_section[section_name] = selected_in_section
                    continue

                # Use checkboxes for each metric in the filtered list
                cols = st.columns(min(3, len(filtered_section_metrics)))
                for idx, metric_key in enumerate(filtered_section_metrics):
                    with cols[idx % 3]:
                        is_selected = metric_key in selected_in_section
                        checkbox_value = st.checkbox(
                            metric_key,
                            key=f"metric_checkbox_{section_name}_{metric_key}",
                            value=is_selected,
                        )
                        if checkbox_value and metric_key not in selected_in_section:
                            selected_in_section.append(metric_key)
                        elif not checkbox_value and metric_key in selected_in_section:
                            selected_in_section.remove(metric_key)
                
                selected_metrics_by_section[section_name] = selected_in_section
            
            # Update session state with current selections
            st.session_state["more_metrics_selected"] = selected_metrics_by_section

        # Display selected metrics grouped by section (always visible, even when expander is closed)
        any_selected = any(st.session_state["more_metrics_selected"].values())
        if any_selected:
            st.markdown("---")
            st.markdown("#### Selected Additional Metrics")
            
            for section_name, selected_metrics in st.session_state["more_metrics_selected"].items():
                if not selected_metrics:
                    continue
                
                # Filter to only metrics that still exist
                selected_metrics = [k for k in selected_metrics if k in metric_info]
                if not selected_metrics:
                    continue
                
                st.markdown(f"##### {SECTION_DISPLAY_NAMES.get(section_name, section_name)}")
                section_columns = st.columns(3)
                for idx, key in enumerate(selected_metrics):
                    mi = metric_info[key]
                    # Do NOT append section name here - this is the original section display
                    with section_columns[idx % 3]:
                        kpi_card(mi["label"], mi["value"], prefix=mi["prefix"], metric_key=key, explanation=mi.get("explanation"))
                        st.caption(mi["explanation"])

        # ----- Visualizations (Chart Block) -----
        st.markdown("### Visualizations")
        chart_container = st.container()
        
        with chart_container:
            # Initialize chart index in session state if not exists
            if "chart_index" not in st.session_state:
                st.session_state["chart_index"] = 0
            
            # Create predefined chart configs list
            predefined_charts = []
            for metric_key in CHART_METRIC_KEYS:
                for layout in CHART_LAYOUTS:
                    predefined_charts.append({
                        "metric_key": metric_key,
                        "layout": layout,
                    })
            
            # Ensure chart_index is within bounds
            max_index = len(predefined_charts) - 1
            if st.session_state["chart_index"] < 0:
                st.session_state["chart_index"] = 0
            elif st.session_state["chart_index"] > max_index:
                st.session_state["chart_index"] = max_index
            
            # Get current chart config
            current_chart = predefined_charts[st.session_state["chart_index"]]
            current_metric_key = current_chart["metric_key"]
            current_layout = current_chart["layout"]
            
            # Header with title and controls
            col_left, col_right = st.columns([3, 2])
            with col_left:
                st.markdown("#### 📊 Revenue and performance charts")
            with col_right:
                # Carousel navigation buttons
                col_prev, col_next, col_spacer = st.columns([1, 1, 3])
                with col_prev:
                    if st.button("◀ Previous", key="chart_prev"):
                        st.session_state["chart_index"] = max(0, st.session_state["chart_index"] - 1)
                        st.rerun()
                with col_next:
                    if st.button("Next ▶", key="chart_next"):
                        st.session_state["chart_index"] = min(max_index, st.session_state["chart_index"] + 1)
                        st.rerun()
            
            # Dropdowns for direct selection
            col_metric, col_layout = st.columns(2)
            with col_metric:
                metric_option = st.selectbox(
                    "Metric",
                    options=CHART_METRIC_KEYS,
                    index=CHART_METRIC_KEYS.index(current_metric_key) if current_metric_key in CHART_METRIC_KEYS else 0,
                    format_func=lambda x: CHART_METRIC_LABELS.get(x, x),
                    key="chart_metric_select",
                )
            with col_layout:
                layout_option = st.selectbox(
                    "Layout",
                    options=CHART_LAYOUTS,
                    index=CHART_LAYOUTS.index(current_layout) if current_layout in CHART_LAYOUTS else 0,
                    key="chart_layout_select",
                )
            
            # Update chart_index if dropdowns changed
            if metric_option != current_metric_key or layout_option != current_layout:
                # Find the index of the new combination
                for idx, chart in enumerate(predefined_charts):
                    if chart["metric_key"] == metric_option and chart["layout"] == layout_option:
                        st.session_state["chart_index"] = idx
                        break
            
            # Get the current chart config again (in case it changed)
            current_chart = predefined_charts[st.session_state["chart_index"]]
            current_metric_key = current_chart["metric_key"]
            current_layout = current_chart["layout"]
            
            # Calculate nights available per month for occupancy metric
            nights_available_per_month = None
            if current_metric_key == "occupancy_by_month":
                nights_available_per_month = {}
                # Get all unique months from bookings
                df_temp = clean_bookings(bookings_filtered.copy())
                if "Check-in Year" in df_temp.columns and "Check-in Month" in df_temp.columns:
                    df_temp["Year"] = pd.to_numeric(df_temp["Check-in Year"], errors="coerce")
                    df_temp["Month"] = pd.to_numeric(df_temp["Check-in Month"], errors="coerce")
                    df_temp = df_temp.dropna(subset=["Year", "Month"])
                    df_temp["Year"] = df_temp["Year"].astype(int)
                    df_temp["Month"] = df_temp["Month"].astype(int)
                    df_temp["Year-Month"] = pd.to_datetime(
                        df_temp["Year"].astype(str) + "-" + df_temp["Month"].astype(str) + "-01"
                    )
                    for year_month in df_temp["Year-Month"].unique():
                        year = pd.to_datetime(year_month).year
                        month = pd.to_datetime(year_month).month
                        days_in_month = calendar.monthrange(year, month)[1]
                        nights_available_per_month[pd.to_datetime(year_month)] = days_in_month
            
            # Get monthly metric data
            try:
                monthly_metric_data = get_monthly_metric_data(
                    bookings_filtered,
                    current_metric_key,
                    nights_available_per_month,
                )
                
                # Prepare chart data based on view mode
                chart_df = prepare_chart_data(monthly_metric_data, view_mode)
                
                # Build and display chart
                if not chart_df.empty:
                    chart = build_altair_chart(
                        chart_df,
                        current_metric_key,
                        current_layout,
                        view_mode,
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info(f"No data available for {CHART_METRIC_LABELS.get(current_metric_key, current_metric_key)}.")
            except Exception as e:
                st.error(f"Error generating chart: {e}")
                st.info("Please check your data and try again.")
            
            # ----- Custom Graphs Management -----
            st.markdown("---")
            st.markdown("#### 🎨 Custom Graphs")
            
            with st.expander("Manage Custom Graphs", expanded=False):
                # Build dynamic list of eligible metrics for custom graphs.
                # We include:
                # - Time-series keys from CHART_METRIC_KEYS (monthly metrics)
                # - All numeric metrics from metric_info (KPI metrics from METRIC_INFO)
                eligible_metrics: list[tuple[str, str]] = []  # (group_label, metric_key)

                # 1) Time-series metrics group
                if CHART_METRIC_KEYS:
                    for mk in CHART_METRIC_KEYS:
                        eligible_metrics.append(("📅 Time series (by month)", mk))

                # 2) KPI metrics grouped by section, only numeric values
                for section_name, section_metrics in METRIC_SECTIONS.items():
                    if section_name == "Custom":
                        continue
                    group_label = SECTION_DISPLAY_NAMES.get(section_name, section_name)
                    for mk in section_metrics:
                        if mk in metric_info and isinstance(metric_info[mk].get("value"), (int, float)):
                            eligible_metrics.append((group_label, mk))

                # 3) Any additional numeric metrics not explicitly in METRIC_SECTIONS
                already_added = {m for _, m in eligible_metrics}
                for mk, info in metric_info.items():
                    if mk not in already_added and isinstance(info.get("value"), (int, float)):
                        eligible_metrics.append(("Other", mk))

                metric_options = [m for _, m in eligible_metrics]
                group_by_metric = {m: g for g, m in eligible_metrics}

                # Form to create new custom graph
                st.markdown("**Create a new custom graph:**")
                col_name, col_metric, col_layout = st.columns([2, 2, 2])
                with col_name:
                    new_graph_name = st.text_input("Graph name", key="new_graph_name", placeholder="e.g., My Revenue Chart")
                with col_metric:
                    new_graph_metric = st.selectbox(
                        "Metric",
                        options=metric_options,
                        format_func=lambda x: f"{group_by_metric.get(x, '')} · {x}" if x in group_by_metric else x,
                        key="new_graph_metric",
                    )
                    # Show metric description under the dropdown for clarity
                    metric_meta = get_metric_info(new_graph_metric)
                    if metric_meta.get("description"):
                        st.caption(metric_meta["description"])
                with col_layout:
                    new_graph_layout = st.selectbox(
                        "Layout",
                        options=CHART_LAYOUTS,
                        key="new_graph_layout",
                    )
                
                if st.button("💾 Save Graph", key="save_custom_graph"):
                    if new_graph_name.strip():
                        # Check if name already exists
                        existing_names = [g.get("name", "") for g in st.session_state["custom_graphs"]]
                        if new_graph_name.strip() in existing_names:
                            st.warning(f"A graph named '{new_graph_name.strip()}' already exists. Please choose a different name.")
                        else:
                            new_graph = {
                                "name": new_graph_name.strip(),
                                "metric_key": new_graph_metric,
                                "layout": new_graph_layout,
                            }
                            st.session_state["custom_graphs"].append(new_graph)
                            save_custom_graphs(st.session_state["custom_graphs"])
                            st.success(f"Graph '{new_graph_name.strip()}' saved!")
                            st.rerun()
                    else:
                        st.warning("Please enter a graph name.")
                
                # Delete existing custom graphs
                st.markdown("**Delete custom graphs:**")
                if st.session_state["custom_graphs"]:
                    graphs_to_delete = st.multiselect(
                        "Select graphs to delete",
                        options=[g.get("name", "Unnamed") for g in st.session_state["custom_graphs"]],
                        key="delete_custom_graphs",
                    )
                    if st.button("🗑️ Delete Selected", key="delete_graphs_btn"):
                        if graphs_to_delete:
                            st.session_state["custom_graphs"] = [
                                g for g in st.session_state["custom_graphs"]
                                if g.get("name", "Unnamed") not in graphs_to_delete
                            ]
                            save_custom_graphs(st.session_state["custom_graphs"])
                            st.success(f"Deleted {len(graphs_to_delete)} graph(s).")
                            st.rerun()
                else:
                    st.info("No custom graphs saved yet.")
            
            # Display all saved custom graphs
            if st.session_state["custom_graphs"]:
                st.markdown("---")
                for graph in st.session_state["custom_graphs"]:
                    graph_name = graph.get("name", "Unnamed Graph")
                    graph_metric_key = graph.get("metric_key", "revenue_by_month")
                    graph_layout = graph.get("layout", "Line")
                    
                    st.markdown(f"##### {graph_name}")
                    
                    # Calculate nights available per month for occupancy metric
                    nights_available_per_month_custom = None
                    if graph_metric_key == "occupancy_by_month":
                        nights_available_per_month_custom = {}
                        df_temp = clean_bookings(bookings_filtered.copy())
                        if "Check-in Year" in df_temp.columns and "Check-in Month" in df_temp.columns:
                            df_temp["Year"] = pd.to_numeric(df_temp["Check-in Year"], errors="coerce")
                            df_temp["Month"] = pd.to_numeric(df_temp["Check-in Month"], errors="coerce")
                            df_temp = df_temp.dropna(subset=["Year", "Month"])
                            df_temp["Year"] = df_temp["Year"].astype(int)
                            df_temp["Month"] = df_temp["Month"].astype(int)
                            df_temp["Year-Month"] = pd.to_datetime(
                                df_temp["Year"].astype(str) + "-" + df_temp["Month"].astype(str) + "-01"
                            )
                            for year_month in df_temp["Year-Month"].unique():
                                year = pd.to_datetime(year_month).year
                                month = pd.to_datetime(year_month).month
                                days_in_month = calendar.monthrange(year, month)[1]
                                nights_available_per_month_custom[pd.to_datetime(year_month)] = days_in_month
                    
                    try:
                        # Decide whether this is a time-series metric (CHART_METRIC_KEYS)
                        # or an aggregated KPI metric from metric_info.
                        if graph_metric_key in CHART_METRIC_KEYS:
                            # ----- Time-series metric: use monthly aggregation -----
                            monthly_metric_data_custom = get_monthly_metric_data(
                                bookings_filtered,
                                graph_metric_key,
                                nights_available_per_month_custom,
                            )
                            chart_df_custom = prepare_chart_data(monthly_metric_data_custom, view_mode)
                        else:
                            # ----- Aggregated KPI metric: use current metric_info value -----
                            metric_entry = metric_info.get(graph_metric_key, {})
                            metric_value = metric_entry.get("value", None)
                            if isinstance(metric_value, (int, float)):
                                chart_df_custom = pd.DataFrame({"Value": [float(metric_value)]})
                                chart_df_custom.index = [graph_metric_key]
                            else:
                                chart_df_custom = pd.DataFrame()
                        
                        # Build and display chart
                        if not chart_df_custom.empty:
                            chart_custom = build_altair_chart(
                                chart_df_custom,
                                graph_metric_key,
                                graph_layout,
                                view_mode,
                            )
                            st.altair_chart(chart_custom, use_container_width=True)
                        else:
                            st.info(f"No data available for this custom graph.")
                    except Exception as e:
                        st.error(f"Error generating custom graph '{graph_name}': {e}")

        # ----- Year/Month revenue heatmap -----
        st.markdown("### Year/Month revenue heatmap")

        heat_source = clean_bookings(bookings_filtered.copy())
        if "Platform" in heat_source.columns:
            heat_source["platform_normalized"] = heat_source["Platform"].replace(
                {"Booking": "Booking.com"}
            )
        else:
            heat_source["platform_normalized"] = "Unknown"

        # Respect View mode for heatmap
        if view_mode == "Airbnb":
            heat_source = heat_source[heat_source["platform_normalized"] == "Airbnb"]
        elif view_mode == "Booking.com":
            heat_source = heat_source[heat_source["platform_normalized"] == "Booking.com"]

        if (
            "Check-in Year" in heat_source.columns
            and "Check-in Month" in heat_source.columns
            and "Revenue for stay (€)" in heat_source.columns
            and not heat_source.empty
        ):
            heat_source["Year"] = heat_source["Check-in Year"].astype(int)
            heat_source["Month"] = heat_source["Check-in Month"].astype(int)

            heat_grouped = (
                heat_source.groupby(["Year", "Month"])["Revenue for stay (€)"]
                .sum()
                .reset_index()
            )
            heat_grouped["MonthName"] = heat_grouped["Month"].apply(
                lambda m: calendar.month_abbr[int(m)]
            )
            heat_grouped.rename(columns={"Revenue for stay (€)": "Revenue"}, inplace=True)

            heat_chart = (
                alt.Chart(heat_grouped)
                .mark_rect()
                .encode(
                    x=alt.X("MonthName:O", title="Month"),
                    y=alt.Y("Year:O", title="Year"),
                    color=alt.Color(
                        "Revenue:Q",
                        title="Revenue (€)",
                        scale=alt.Scale(scheme="blues"),
                    ),
                    tooltip=[
                        alt.Tooltip("Year:O", title="Year"),
                        alt.Tooltip("MonthName:O", title="Month"),
                        alt.Tooltip("Revenue:Q", title="Revenue (€)", format=",.2f"),
                    ],
                )
            )
            st.altair_chart(heat_chart, use_container_width=True)
        else:
            st.info("No booking data available to build a heatmap for the selected period.")

    else:
        # ----- COMPARISON VIEW (Airbnb vs Booking.com) -----
        st.markdown("### Airbnb vs Booking.com – comparison")

        monthly_revenue_data = monthly_revenue_by_platform(bookings_filtered)
        comparison_df = monthly_revenue_data[["Airbnb", "Booking.com"]].copy()
        comparison_df["Difference (Airbnb - Booking.com)"] = (
            comparison_df["Airbnb"] - comparison_df["Booking.com"]
        )

        total_airbnb = comparison_df["Airbnb"].sum()
        total_booking_com = comparison_df["Booking.com"].sum()

        col1, col2, col3 = st.columns(3)
        with col1:
            kpi_card("Total revenue – Airbnb (€)", total_airbnb, prefix="€ ", metric_key="Airbnb revenue (€)")
            st.caption("Total revenue generated from Airbnb in the selected period.")
        with col2:
            kpi_card("Total revenue – Booking.com (€)", total_booking_com, prefix="€ ", metric_key="Booking.com revenue (€)")
            st.caption("Total revenue generated from Booking.com in the selected period.")
        with col3:
            kpi_card(
                "Revenue Difference (Airbnb - Booking.com)",
                total_airbnb - total_booking_com,
                prefix="€ ",
                metric_key="Platform Profitability Difference (€)"
            )
            st.caption("Difference in total revenue between Airbnb and Booking.com.")

        st.markdown("#### Monthly revenue comparison")
        st.bar_chart(comparison_df[["Airbnb", "Booking.com"]])

        st.markdown("#### Table view")
        st.dataframe(comparison_df.style.format("{:,.2f}"))

    # -------- REPORTS PAGE --------
elif page == "Reports":
    st.title("📊 Reports")
    
    # Initialize templates in session state
    if "report_templates" not in st.session_state:
        st.session_state["report_templates"] = get_all_report_templates()
    
    # Tab selection: View Reports, Create Custom Report, or Manage Templates
    tab1, tab2, tab3 = st.tabs(["📋 View Reports", "➕ Create Custom Report", "⚙️ Manage Templates"])
    
    with tab1:
        st.markdown("### Select a Report Template")
        
        all_templates = get_all_report_templates()
        template_names = list(all_templates.keys())
        
        selected_template_name = st.selectbox(
            "Choose a report template",
            options=template_names,
            format_func=lambda x: f"{x} {'(Built-in)' if all_templates[x].get('is_builtin') else '(Custom)'}",
        )
        
        if selected_template_name:
            template = all_templates[selected_template_name]
            st.markdown(f"**Description:** {template.get('description', 'No description')}")
            
            # Filter configuration
            st.markdown("### Configure Filters")
            
            col1, col2 = st.columns(2)
            
            with col1:
                period_type = st.selectbox(
                    "Period Type",
                    options=["year", "month_year", "date_range"],
                    index=0,
                    key="report_period_type",
                )
                
                if period_type == "year":
                    available_years = (
                        bookings["Check-in Year"].dropna().astype(int).sort_values().unique()
                        if "Check-in Year" in bookings.columns
                        else []
                    )
                    if len(available_years) > 0:
                        selected_year = st.selectbox("Year", options=available_years, key="report_year")
                    else:
                        selected_year = None
                    filter_params = {"period_type": period_type, "year": int(selected_year) if selected_year else None}
                
                elif period_type == "month_year":
                    available_years = (
                        bookings["Check-in Year"].dropna().astype(int).sort_values().unique()
                        if "Check-in Year" in bookings.columns
                        else []
                    )
                    if len(available_years) > 0:
                        selected_year = st.selectbox("Year", options=available_years, key="report_year_month")
                        selected_month = st.selectbox("Month", options=list(range(1, 13)), format_func=lambda x: calendar.month_name[x], key="report_month")
                    else:
                        selected_year = None
                        selected_month = None
                    filter_params = {
                        "period_type": period_type,
                        "year": int(selected_year) if selected_year else None,
                        "month": selected_month,
                    }
                
                else:  # date_range
                    start_date = st.date_input(
                        "Start Date",
                        key="report_start_date",
                        format="DD-MM-YYYY",
                    )
                    end_date = st.date_input(
                        "End Date",
                        key="report_end_date",
                        format="DD-MM-YYYY",
                    )
                    filter_params = {
                        "period_type": period_type,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
            
            with col2:
                platform = st.selectbox(
                    "Platform",
                    options=["Overall", "Airbnb", "Booking.com"],
                    key="report_platform",
                )
                filter_params["platform"] = platform
            
            # Generate report button
            if st.button("📊 Generate Report", type="primary"):
                if selected_template_name in all_templates:
                    render_report(
                        all_templates[selected_template_name],
                        bookings,
                        monthly_costs,
                        filter_params,
                    )
    
    with tab2:
        st.markdown("### Create Custom Report Template")
        
        # Get all available metrics
        sample_metric_info = calculate_all_metrics(
            bookings,
            monthly_costs,
            "Overall",
            compute_nights_available(bookings, None),
            None,
        )
        all_metric_keys = list(sample_metric_info.keys())
        
        # Report configuration form
        with st.form("custom_report_form"):
            report_name = st.text_input("Report Name *", placeholder="e.g., Q4 Performance Review")
            report_description = st.text_area("Description", placeholder="Brief description of this report")
            
            st.markdown("**Select Metrics**")
            # Group metrics by section for easier selection
            selected_metrics = []
            for section_name, section_metrics in METRIC_SECTIONS.items():
                if section_name == "Custom":
                    continue
                available_in_section = [m for m in section_metrics if m in all_metric_keys]
                if available_in_section:
                    st.markdown(f"##### {SECTION_DISPLAY_NAMES.get(section_name, section_name)}")
                    section_selected = st.multiselect(
                        f"Select from {section_name}",
                        options=available_in_section,
                        key=f"custom_report_{section_name}",
                    )
                    selected_metrics.extend(section_selected)
            
            # Also allow selecting from all metrics
            st.markdown("##### All Metrics")
            additional_metrics = st.multiselect(
                "Or select from all metrics",
                options=[m for m in all_metric_keys if m not in selected_metrics],
                key="custom_report_all",
            )
            selected_metrics.extend(additional_metrics)
            
            # Chart selection
            st.markdown("**Select Charts**")
            chart_options = [
                "monthly_revenue_line",
                "platform_comparison_bar",
                "platform_comparison_table",
                "cost_breakdown_pie",
                "revenue_heatmap",
            ]
            selected_charts = st.multiselect(
                "Choose charts to include",
                options=chart_options,
                key="custom_report_charts",
            )
            
            # Default filters
            st.markdown("**Default Filters**")
            default_period_type = st.selectbox(
                "Default Period Type",
                options=["year", "month_year", "date_range"],
                key="custom_report_period_type",
            )
            default_platform = st.selectbox(
                "Default Platform",
                options=["Overall", "Airbnb", "Booking.com"],
                key="custom_report_platform",
            )
            
            submitted = st.form_submit_button("💾 Save as Template")
            
            if submitted:
                if not report_name.strip():
                    st.error("Report name is required!")
                elif not selected_metrics:
                    st.error("Please select at least one metric!")
                else:
                    # Create template
                    new_template = {
                        "name": report_name.strip(),
                        "description": report_description.strip() if report_description else "",
                        "metrics": selected_metrics,
                        "filters": {
                            "period_type": default_period_type,
                            "platform": default_platform,
                        },
                        "charts": selected_charts,
                        "is_builtin": False,
                    }
                    
                    # Save to file
                    user_templates = load_report_templates()
                    user_templates[report_name.strip()] = new_template
                    save_report_templates(user_templates)
                    
                    # Update session state
                    st.session_state["report_templates"] = get_all_report_templates()
                    
                    st.success(f"✅ Template '{report_name}' saved successfully!")
                    st.info("You can now select this template from the 'View Reports' tab.")
        
    with tab3:
        st.markdown("### ⚙️ Manage Custom Templates")
        st.caption("View, manage, and delete your custom report templates. Built-in templates cannot be deleted.")
        
        user_templates = load_report_templates()
        
        if user_templates:
            st.write(f"You have **{len(user_templates)}** custom template(s):")
            st.markdown("---")
            
            # Create a more organized template management interface
            for idx, (template_name, template_data) in enumerate(user_templates.items()):
                with st.container():
                    col_info, col_action = st.columns([4, 1])
                    
                    with col_info:
                        st.markdown(f"#### 📄 {template_name}")
                        if template_data.get("description"):
                            st.caption(template_data.get("description"))
                        
                        col_meta1, col_meta2, col_meta3 = st.columns(3)
                        with col_meta1:
                            st.write(f"📊 **{len(template_data.get('metrics', []))}** metrics")
                        with col_meta2:
                            st.write(f"📈 **{len(template_data.get('charts', []))}** charts")
                        with col_meta3:
                            period_type = template_data.get('filters', {}).get('period_type', 'N/A')
                            platform = template_data.get('filters', {}).get('platform', 'N/A')
                            st.write(f"🔧 {period_type} | {platform}")
                    
                    with col_action:
                        st.write("")  # Spacing
                        # Use a unique key that includes index to avoid conflicts
                        delete_key = f"delete_template_{idx}_{template_name}"
                        if st.button("🗑️ Delete", key=delete_key, type="secondary"):
                            # Confirm deletion
                            if delete_template(template_name):
                                st.success(f"✅ Template '{template_name}' deleted successfully!")
                                st.session_state["report_templates"] = get_all_report_templates()
                                st.rerun()
                            else:
                                st.error(f"❌ Failed to delete template '{template_name}'")
                    
                    if idx < len(user_templates) - 1:
                        st.divider()
            
            st.markdown("---")
            st.info("💡 **Tip:** Custom templates are saved permanently. You can use them anytime in the 'View Reports' tab.")
        else:
            st.info("📝 No custom templates yet. Create one in the 'Create Custom Report' tab to get started!")
            st.caption("Custom templates are saved permanently and can be reused anytime.")

    # -------- BOOKINGS PAGE --------
elif page == "Bookings":
    st.title("📒 Bookings")

    # ----- Add new booking -----
    st.markdown("---")
    st.markdown("#### ➕ Add New Booking")
    
    # Add new booking form in expandable section (collapsed by default)
    with st.expander("Add a new booking", expanded=False):
        # Helper function to calculate revenue based on platform (commission adjustment)
        def calculate_revenue(platform, user_value):
            """
            Calculate the revenue to be saved based on platform.
            - Airbnb: Save the full value as entered
            - Booking.com: Apply 12% commission deduction (save 88% of user input)
            """
            if platform == "Booking.com":
                return round(user_value * 0.88, 2)
            return user_value
        
        with st.form("new_booking_form", clear_on_submit=False):
            c1, c2 = st.columns(2)

            # ---------------- LEFT COLUMN ----------------
            with c1:
                check_in = st.date_input(
                    "Check-in date *",
                    format="DD-MM-YYYY",
                )
                adults = st.number_input("Adults *", min_value=0, value=2, step=1)
                children = st.number_input("Children *", min_value=0, value=0, step=1)
                platform = st.selectbox("Platform *", ["Airbnb", "Booking.com"])

            # ---------------- RIGHT COLUMN ----------------
            with c2:
                check_out = st.date_input(
                    "Check-out date *",
                    format="DD-MM-YYYY",
                )
                guest_name = st.text_input("Guest Name *")

                # ---- Country dropdown with search + Add country ----
                # session_state за земји додадени во тековната сесија
                if "added_countries" not in st.session_state:
                    st.session_state["added_countries"] = set()

                # земји кои веќе постојат во Bookings sheet
                if "Country" in bookings.columns:
                    existing_countries = (
                        bookings["Country"]
                        .dropna()
                        .astype(str)
                        .str.strip()
                        .replace("", pd.NA)
                        .dropna()
                        .unique()
                        .tolist()
                    )
                else:
                    existing_countries = []

                # неколку најчести земји
                common_countries = [
                    "North Macedonia", "Serbia", "Bulgaria", "Greece", "Albania",
                    "Kosovo", "Turkey", "Germany", "Switzerland", "Italy",
                    "Slovenia", "Croatia", "Austria",
                ]

                add_country_label = "+ Add country"

                # база: common + existing + во сесија додадени
                country_base = sorted(
                    set(common_countries)
                    | set(existing_countries)
                    | set(st.session_state["added_countries"]),
                    key=str.casefold,
                )

                # финална листа: placeholder + земји + "+ Add country"
                country_options = ["Select Country"] + country_base + [add_country_label]

                country_choice = st.selectbox(
                    "Country *",
                    country_options,
                    index=0,          # покажи "Select Country" како default
                    key="country_select",
                )

                # логика за избор/додавање на земја
                if country_choice == "Select Country":
                    country = ""      # невалидно - ќе фатиме во валидација
                elif country_choice == add_country_label:
                    new_country = st.text_input(
                        "Add new country *",
                        key="country_new_input",
                        placeholder="Type country name..."
                    ).strip()

                    if new_country:
                        st.session_state["added_countries"].add(new_country)
                        country = new_country
                    else:
                        country = ""  # уште невалидно додека не внесе нешто
                else:
                    country = country_choice

                # Use text input for revenue to allow clearing placeholder on focus
                # Text input with placeholder - when clicked, placeholder disappears and user can type fresh number
                # Don't use key to avoid session state conflicts - form's clear_on_submit=False handles preservation
                revenue_text = st.text_input(
                    "Revenue for stay (€) *",
                    value="",  # Empty by default - placeholder will show
                    placeholder="0.00",
                    help="Enter the revenue amount (e.g., 120 or 120.50). Click to clear and type."
                )
                
                # Convert to float, defaulting to 0.0 if empty or invalid
                try:
                    revenue = float(revenue_text.strip()) if revenue_text.strip() else 0.0
                except (ValueError, AttributeError):
                    revenue = 0.0

                c3, c4, c5 = st.columns(3)

                with c3:
                    sofa_bed = st.selectbox("Sofa Bed *", ["No", "Yes"])
                    baby_crib = st.selectbox("Baby Crib *", ["No", "Yes"])
                    parking = st.selectbox("Parking *", ["No", "Yes"])

                with c4:
                    transportation_cost = st.number_input(
                        "Transportation Cost *", min_value=0.0, step=1.0, value=5.0
                    )
                    laundry_cost = st.number_input(
                        "Laundry Cost *", min_value=0.0, step=1.0, value=5.0
                    )

                with c5:
                    # Get current consumables total as default value
                    _, default_consumable_cost = get_current_consumables_totals(toiletries)
                    consumable_cost = st.number_input(
                        "Consumable Cost *", min_value=0.0, step=0.01, value=round(default_consumable_cost, 2)
                    )
                    bank_fees = st.number_input(
                        "Bank Fees *", min_value=0.0, step=1.0, value=6.0
                    )

            # Responsive text area - height adapts on mobile
            notes = st.text_area("Notes", height=100)

            submitted = st.form_submit_button("➕ Add booking")

            if submitted:
                missing_fields = []

                # Basic validation (Notes is optional, no validation needed)
                if not guest_name.strip():
                    missing_fields.append("Guest Name")
                if not country:
                    missing_fields.append("Country")
                if revenue <= 0:
                    missing_fields.append("Revenue for stay (€)")

                date_errors = []
                if check_out <= check_in:
                    date_errors.append("Check-out date must be after check-in date.")

                # If there are errors -> don't save anything
                if missing_fields or date_errors:
                    if missing_fields:
                        msg = (
                            "The following required fields are missing: "
                            + ", ".join(missing_fields)
                        )
                        st.error(msg)
                        st.toast(msg, icon="⚠️")

                    for err in date_errors:
                        st.error(err)
                        st.toast(err, icon="⚠️")

                else:
                    # All conditions met -> calculate and save
                    # Auto-format currency fields to 2 decimals
                    user_revenue = round(float(revenue), 2)
                    transportation_cost = round(float(transportation_cost), 2)
                    laundry_cost = round(float(laundry_cost), 2)
                    consumable_cost = round(float(consumable_cost), 2)
                    bank_fees = round(float(bank_fees), 2)
                    
                    # Calculate adjusted revenue based on platform (Booking.com has 12% commission)
                    revenue_for_stay = calculate_revenue(platform, user_revenue)
                    
                    total_guests = adults + children
                    nights = (pd.to_datetime(check_out) - pd.to_datetime(check_in)).days
                    month = check_in.month
                    year = check_in.year

                    per_stay_expenses = round(transportation_cost + laundry_cost + consumable_cost + bank_fees, 2)
                    # Use adjusted revenue for net income calculation
                    net_before_fixed = round(revenue_for_stay - per_stay_expenses, 2)

                    new_row = {
                        "Check-in date": pd.to_datetime(check_in),
                        "Check-out date": pd.to_datetime(check_out),
                        "Guest Name": guest_name,
                        "Country": country,
                        "Adults": adults,
                        "Children": children,
                        "Total guests": total_guests,
                        "Sofa Bed": sofa_bed,
                        "Baby Crib": baby_crib,
                        "Parking": parking,
                        "Platform": "Booking" if platform == "Booking.com" else "Airbnb",
                        "Nights": nights,
                        "Revenue for stay (€)": revenue_for_stay,
                        "Transportation Cost (€)": transportation_cost,
                        "Laundry Cost (€)": laundry_cost,
                        "Consumable Cost (€)": consumable_cost,
                        "Bank Fees (€)": bank_fees,
                        "Per-stay expenses (€)": per_stay_expenses,
                        "Net Income Before Fixed Costs (€)": net_before_fixed,
                        "Check-in Month": month,
                        "Check-in Year": year,
                        "Notes": notes if notes else "",  # Allow empty notes
                    }

                    bookings = pd.concat(
                        [bookings, pd.DataFrame([new_row])], ignore_index=True
                    )
                    save_data(bookings, monthly_costs, toiletries, FILE_PATH)
                    st.success("New booking added and saved ✅")
                    st.toast("Booking successfully saved.", icon="✅")
                    st.rerun()  # Refresh form after successful save

    # ----- Edit & delete existing bookings -----
    st.markdown("#### Edit existing bookings")

    bookings_for_edit = bookings.copy().reset_index(drop=True)
    bookings_for_edit["Delete?"] = False
    
    # Standardize "Guest Supplies Cost (€)" to "Consumable Cost (€)" if old name exists
    if "Guest Supplies Cost (€)" in bookings_for_edit.columns and "Consumable Cost (€)" not in bookings_for_edit.columns:
        bookings_for_edit = bookings_for_edit.rename(columns={"Guest Supplies Cost (€)": "Consumable Cost (€)"})
    elif "Guest Supplies Cost (€)" in bookings_for_edit.columns and "Consumable Cost (€)" in bookings_for_edit.columns:
        # Merge values: prefer Consumable Cost (€), but if empty, use Guest Supplies Cost (€)
        bookings_for_edit["Consumable Cost (€)"] = bookings_for_edit["Consumable Cost (€)"].fillna(
            pd.to_numeric(bookings_for_edit["Guest Supplies Cost (€)"], errors='coerce')
        )
        bookings_for_edit = bookings_for_edit.drop(columns=["Guest Supplies Cost (€)"])
    
    # Remove duplicate "Bank Fees" column if "Bank Fees (€)" exists (standardize to Bank Fees (€))
    if "Bank Fees (€)" in bookings_for_edit.columns and "Bank Fees" in bookings_for_edit.columns:
        # Merge values: prefer Bank Fees (€), but if empty, use Bank Fees
        bookings_for_edit["Bank Fees (€)"] = bookings_for_edit["Bank Fees (€)"].fillna(
            pd.to_numeric(bookings_for_edit["Bank Fees"], errors='coerce')
        )
        bookings_for_edit = bookings_for_edit.drop(columns=["Bank Fees"])

    # Ensure date columns are proper datetime (keep internal values as datetime)
    if "Check-in date" in bookings_for_edit.columns:
        bookings_for_edit["Check-in date"] = pd.to_datetime(
            bookings_for_edit["Check-in date"],
            errors="coerce",
        )
    if "Check-out date" in bookings_for_edit.columns:
        bookings_for_edit["Check-out date"] = pd.to_datetime(
            bookings_for_edit["Check-out date"],
            errors="coerce",
        )
    
    # Add index column as first column (sequential numbers starting from 1)
    bookings_for_edit.insert(0, "#", list(range(1, len(bookings_for_edit) + 1)))

    edited_bookings = st.data_editor(
        bookings_for_edit,
        num_rows="dynamic",
        use_container_width=True,
        key="bookings_editor",
        hide_index=True,
        column_config={
            "#": st.column_config.NumberColumn(
                "#",
                help="Booking row number",
                width="small",
                disabled=True,  # Make index non-editable
            ),
            "Check-in date": st.column_config.DateColumn(
                "Check-in date",
                format="DD-MM-YYYY",
            ),
            "Check-out date": st.column_config.DateColumn(
                "Check-out date",
                format="DD-MM-YYYY",
            ),
            "Delete?": st.column_config.CheckboxColumn(
                "Delete?",
                help="Tick to remove this booking (cancelled / deleted).",
                default=False,
            ),
        },
    )

    if st.button("💾 Save bookings"):
        # Remove index column before saving (it's only for display)
        if "#" in edited_bookings.columns:
            edited_bookings = edited_bookings.drop(columns=["#"])
        
        if "Delete?" in edited_bookings.columns:
            edited_bookings = edited_bookings[~edited_bookings["Delete?"]]
            edited_bookings = edited_bookings.drop(columns=["Delete?"])

        # Convert date columns back to datetime for saving (they were converted to date objects for display)
        if "Check-in date" in edited_bookings.columns:
            edited_bookings["Check-in date"] = pd.to_datetime(edited_bookings["Check-in date"])
        if "Check-out date" in edited_bookings.columns:
            edited_bookings["Check-out date"] = pd.to_datetime(edited_bookings["Check-out date"])

        # Standardize "Guest Supplies Cost (€)" to "Consumable Cost (€)" if old name exists
        if "Guest Supplies Cost (€)" in edited_bookings.columns and "Consumable Cost (€)" not in edited_bookings.columns:
            edited_bookings = edited_bookings.rename(columns={"Guest Supplies Cost (€)": "Consumable Cost (€)"})
        elif "Guest Supplies Cost (€)" in edited_bookings.columns and "Consumable Cost (€)" in edited_bookings.columns:
            # Merge values: prefer Consumable Cost (€), but if empty, use Guest Supplies Cost (€)
            edited_bookings["Consumable Cost (€)"] = edited_bookings["Consumable Cost (€)"].fillna(
                pd.to_numeric(edited_bookings["Guest Supplies Cost (€)"], errors='coerce')
            )
            edited_bookings = edited_bookings.drop(columns=["Guest Supplies Cost (€)"])

        # Remove duplicate "Bank Fees" column if it exists (standardize to Bank Fees (€))
        if "Bank Fees (€)" in edited_bookings.columns and "Bank Fees" in edited_bookings.columns:
            # Merge values: prefer Bank Fees (€), but if empty, use Bank Fees
            edited_bookings["Bank Fees (€)"] = edited_bookings["Bank Fees (€)"].fillna(
                pd.to_numeric(edited_bookings["Bank Fees"], errors='coerce')
            )
            edited_bookings = edited_bookings.drop(columns=["Bank Fees"])
        
        # Optionally fill empty Consumable Cost (€) values with current consumables total
        # Only fill if the value is truly empty/NaN (not overwriting existing historical values)
        if "Consumable Cost (€)" in edited_bookings.columns:
            empty_mask = edited_bookings["Consumable Cost (€)"].isna() | (pd.to_numeric(edited_bookings["Consumable Cost (€)"], errors='coerce').fillna(0) == 0)
            if empty_mask.any():
                _, current_total_eur = get_current_consumables_totals(toiletries)
                edited_bookings.loc[empty_mask, "Consumable Cost (€)"] = current_total_eur

        # Auto-format currency fields to 2 decimals before saving
        currency_columns = [
            "Revenue for stay (€)",
            "Transportation Cost (€)",
            "Laundry Cost (€)",
            "Consumable Cost (€)",  # Updated from Guest Supplies Cost
            "Bank Fees (€)",  # Use standardized column name
            "Per-stay expenses (€)",
            "Net Income Before Fixed Costs (€)",
        ]
        
        for col in currency_columns:
            if col in edited_bookings.columns:
                # Convert to numeric, handling any non-numeric values
                edited_bookings[col] = pd.to_numeric(edited_bookings[col], errors='coerce')
                # Round to 2 decimals
                edited_bookings[col] = edited_bookings[col].round(2)
        
        # Recalculate "Per-stay expenses (€)" and "Net Income Before Fixed Costs (€)" after edits
        # Ensure all required columns exist and are numeric
        required_cost_cols = ["Transportation Cost (€)", "Laundry Cost (€)", "Consumable Cost (€)", "Bank Fees (€)"]
        if all(col in edited_bookings.columns for col in required_cost_cols) and "Revenue for stay (€)" in edited_bookings.columns:
            # Fill NaN with 0 for cost columns
            for col in required_cost_cols:
                edited_bookings[col] = pd.to_numeric(edited_bookings[col], errors='coerce').fillna(0)
            edited_bookings["Revenue for stay (€)"] = pd.to_numeric(edited_bookings["Revenue for stay (€)"], errors='coerce').fillna(0)
            
            # Recalculate Per-stay expenses
            edited_bookings["Per-stay expenses (€)"] = (
                edited_bookings["Transportation Cost (€)"] +
                edited_bookings["Laundry Cost (€)"] +
                edited_bookings["Consumable Cost (€)"] +
                edited_bookings["Bank Fees (€)"]
            ).round(2)
            
            # Recalculate Net Income Before Fixed Costs
            edited_bookings["Net Income Before Fixed Costs (€)"] = (
                edited_bookings["Revenue for stay (€)"] - edited_bookings["Per-stay expenses (€)"]
            ).round(2)
        
        # Ensure Notes field can be empty (fill NaN with empty string)
        if "Notes" in edited_bookings.columns:
            edited_bookings["Notes"] = edited_bookings["Notes"].fillna("")

        save_data(edited_bookings, monthly_costs, toiletries, FILE_PATH)
        st.success("Bookings updated and saved ✅")
        st.toast("Bookings table saved.", icon="✅")


# -------- FIXED COSTS PAGE --------
# -------- EXPENSES PAGE --------
elif page == "Expenses":
    st.title("💸 Expenses")
    
    # Persist active tab in session state
    if "expenses_tab" not in st.session_state:
        st.session_state["expenses_tab"] = "Fixed Costs"
    
    # Create tabs for Fixed Costs and Consumables Costs
    tab_names = ["💸 Fixed Costs", "🧴 Consumables Costs"]
    tab1, tab2 = st.tabs(tab_names)
    
    # Track which tab is being accessed
    # We'll update session_state when each tab context is entered
    
    # -------- TAB 1: Fixed Costs --------
    with tab1:
        # Update session state to track that we're on Fixed Costs tab
        st.session_state["expenses_tab"] = "Fixed Costs"
        st.markdown("#### Add Year")
        with st.form("add_year_form", clear_on_submit=True):
            new_year = st.number_input(
                "Year",
                min_value=2024,
                max_value=2100,
                value=int(pd.Timestamp.today().year),
                step=1,
            )
            add_year_btn = st.form_submit_button("➕ Add Year")

        if add_year_btn:
            existing_years = (
                monthly_costs["Year"].dropna().astype(int).unique()
                if "Year" in monthly_costs.columns
                else []
            )
            if int(new_year) in existing_years:
                st.warning(f"Year {int(new_year)} already exists in the table.")
            else:
                new_rows = []
                for month_number in range(1, 13):
                    row = {}
                    for column in monthly_costs.columns:
                        if column == "Year":
                            row[column] = int(new_year)
                        elif column.lower().startswith("month"):
                            row[column] = month_number
                        else:
                            row[column] = 0
                    new_rows.append(row)

                monthly_costs = pd.concat(
                    [monthly_costs, pd.DataFrame(new_rows)], ignore_index=True
                )
                monthly_costs = recalc_monthly_costs(monthly_costs)
                save_data(bookings, monthly_costs, toiletries, FILE_PATH)
                st.success(f"Year {int(new_year)} added with 12 months ✅")

        st.markdown("#### Edit Fixed Costs")

        edited_costs = st.data_editor(
            monthly_costs,
            num_rows="dynamic",
            use_container_width=True,
            key="costs_editor",
        )

        if st.button("💾 Save Fixed Costs"):
            edited_costs = recalc_monthly_costs(edited_costs)
            save_data(bookings, edited_costs, toiletries, FILE_PATH)
            st.success("Fixed Costs updated and saved ✅")
    
    # -------- TAB 2: Consumables Costs --------
    with tab2:
        # Update session state to track that we're on Consumables Costs tab
        st.session_state["expenses_tab"] = "Consumables Costs"
        
        st.markdown("#### Edit Consumables")
        
        # Initialize consumables DataFrame in session state only once (on first load)
        # This prevents reloading from Excel on every rerun
        if "consumables_df" not in st.session_state:
            # Load initial data from Excel
            toiletries_display = toiletries.copy()
            # Ensure numeric columns are properly converted
            if "Unit Price (MKD)" in toiletries_display.columns:
                toiletries_display["Unit Price (MKD)"] = pd.to_numeric(toiletries_display["Unit Price (MKD)"], errors="coerce").fillna(0)
            if "Units per Stay" in toiletries_display.columns:
                toiletries_display["Units per Stay"] = pd.to_numeric(toiletries_display["Units per Stay"], errors="coerce").fillna(0)
            if "Total (MKD)" in toiletries_display.columns:
                toiletries_display["Total (MKD)"] = pd.to_numeric(toiletries_display["Total (MKD)"], errors="coerce").fillna(0)
            # Recalculate Total (MKD) before storing
            toiletries_display = recalc_toiletries(toiletries_display)
            st.session_state["consumables_df"] = toiletries_display.copy()
        
        # Always use session state DataFrame for editing
        toiletries_to_edit = st.session_state["consumables_df"].copy()
        
        edited_toiletries = st.data_editor(
            toiletries_to_edit,
            num_rows="dynamic",
            use_container_width=True,
            key="toiletries_editor",
        )
        
        # Immediately recalculate Total (MKD) after user edits
        # Ensure numeric columns are converted
        if "Unit Price (MKD)" in edited_toiletries.columns:
            edited_toiletries["Unit Price (MKD)"] = pd.to_numeric(edited_toiletries["Unit Price (MKD)"], errors="coerce").fillna(0)
        if "Units per Stay" in edited_toiletries.columns:
            edited_toiletries["Units per Stay"] = pd.to_numeric(edited_toiletries["Units per Stay"], errors="coerce").fillna(0)
        
        # Recalculate Total (MKD) = Unit Price (MKD) * Units per Stay
        if "Unit Price (MKD)" in edited_toiletries.columns and "Units per Stay" in edited_toiletries.columns:
            edited_toiletries["Total (MKD)"] = (edited_toiletries["Unit Price (MKD)"] * edited_toiletries["Units per Stay"]).round(2)
        
        # Update session state with recalculated values for next render
        # This ensures the recalculated Total (MKD) is visible on the next rerun
        # Streamlit automatically reruns when user edits the data_editor, so the updated
        # Total (MKD) values will be displayed on the next render
        st.session_state["consumables_df"] = edited_toiletries.copy()
        
        # Calculate and display totals using recalculated values
        total_mkd, total_eur = get_current_consumables_totals(edited_toiletries)
        
        # Display totals below the table
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total (MKD)", f"{total_mkd:,.2f}")
        with col2:
            st.metric("Total (EUR)", f"{total_eur:,.2f}")

        if st.button("💾 Save Consumables Costs"):
            # Final recalculation before saving
            edited_toiletries_final = recalc_toiletries(edited_toiletries.copy())
            save_data(bookings, monthly_costs, edited_toiletries_final, FILE_PATH)
            # Reload from Excel after save to sync with disk
            bookings, monthly_costs, toiletries = load_data(FILE_PATH)
            # Prepare fresh data for session state
            toiletries_display = toiletries.copy()
            if "Unit Price (MKD)" in toiletries_display.columns:
                toiletries_display["Unit Price (MKD)"] = pd.to_numeric(toiletries_display["Unit Price (MKD)"], errors="coerce").fillna(0)
            if "Units per Stay" in toiletries_display.columns:
                toiletries_display["Units per Stay"] = pd.to_numeric(toiletries_display["Units per Stay"], errors="coerce").fillna(0)
            if "Total (MKD)" in toiletries_display.columns:
                toiletries_display["Total (MKD)"] = pd.to_numeric(toiletries_display["Total (MKD)"], errors="coerce").fillna(0)
            toiletries_display = recalc_toiletries(toiletries_display)
            # Update session state with fresh data from Excel
            st.session_state["consumables_df"] = toiletries_display.copy()
            # Keep user on Consumables Costs tab
            st.session_state["expenses_tab"] = "Consumables Costs"
            st.success("Consumables Costs updated and saved ✅")
            st.rerun()  # Refresh to show updated totals
