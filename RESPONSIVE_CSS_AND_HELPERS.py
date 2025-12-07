"""
Responsive CSS and Helper Functions for Mobile Support
Add this code to your lynx_app.py file

USAGE:
1. Copy the inject_responsive_css() function and call it at app startup
2. Copy the get_responsive_columns() helper function
3. Use get_responsive_columns() instead of st.columns() throughout your app
"""

import streamlit as st


def inject_responsive_css():
    """
    Inject comprehensive responsive CSS for mobile devices.
    Specifically optimized for iPhone 16 Pro and other mobile devices.
    Call this function once at app startup (after st.set_page_config).
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


def get_responsive_columns(num_columns: int, ratios: list = None):
    """
    Create responsive columns that adapt to screen size.
    
    Args:
        num_columns: Number of columns desired (will be 1 on mobile)
        ratios: Optional list of ratios for columns (e.g., [2, 1])
    
    Returns:
        List of column objects (single column on mobile, multiple on desktop)
    
    Usage:
        # Instead of: cols = st.columns(3)
        # Use:
        cols = get_responsive_columns(3)
        with cols[0]:
            kpi_card(...)
        
        # Instead of: col1, col2 = st.columns([2, 1])
        # Use:
        col1, col2 = get_responsive_columns(2, [2, 1])
    """
    # Detect mobile using JavaScript (runs client-side)
    # We'll use a simpler approach: always create columns, CSS will handle responsiveness
    # But for better control, we can check screen size via session state
    
    # Check if we have screen size in session state (set by JavaScript)
    is_mobile = st.session_state.get("is_mobile", False)
    
    # On mobile, return single column wrapped in a list
    if is_mobile and num_columns > 1:
        # Return a list with one column that takes full width
        return [st.container() for _ in range(num_columns)]
    
    # On desktop, return normal columns
    if ratios:
        return st.columns(ratios)
    else:
        return st.columns(num_columns)


def inject_screen_size_detector():
    """
    Inject JavaScript to detect screen size and set session state.
    This helps Python code make responsive decisions.
    Call this once at app startup.
    """
    st.markdown("""
    <script>
    function updateScreenSize() {
        const width = window.innerWidth;
        const isMobile = width < 768;
        
        // Send to Streamlit via window.parent.postMessage
        if (window.parent && window.parent.postMessage) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: { is_mobile: isMobile, width: width }
            }, '*');
        }
        
        // Also set a CSS variable for pure CSS solutions
        document.documentElement.style.setProperty('--viewport-width', width + 'px');
    }
    
    // Update on load and resize
    updateScreenSize();
    window.addEventListener('resize', updateScreenSize);
    window.addEventListener('orientationchange', function() {
        setTimeout(updateScreenSize, 100);
    });
    </script>
    """, unsafe_allow_html=True)

