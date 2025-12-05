# Lynx Apartment Dashboard

A comprehensive property management dashboard built with Streamlit for tracking bookings, expenses, revenue, and performance metrics.

## 🚀 Features

- **Dashboard Overview**: Real-time KPIs including reservations, revenue, occupancy, and profit metrics
- **Booking Management**: Track bookings across multiple platforms (Airbnb, Booking.com, Compariso)
- **Expense Tracking**: Monitor per-stay expenses and fixed monthly costs
- **Custom Metrics**: Create and manage custom performance metrics
- **Custom Graphs**: Build and visualize custom data visualizations
- **Report Generation**: Generate and export detailed performance reports
- **Multi-Platform Support**: Compare performance across different booking platforms

## 📋 Requirements

- Python 3.8+
- Streamlit
- pandas
- altair
- openpyxl

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/lynx-apartment-dashboard.git
cd lynx-apartment-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run lynx_app.py
```

## 📁 Project Structure

```
lynx-apartment-dashboard/
├── lynx_app.py                 # Main Streamlit application
├── export_helpers.py           # Export and integration helpers
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .streamlit/
│   └── secrets.toml.example   # Secrets template
├── assets/
│   ├── lynx_logo_dark.png     # Logo for light backgrounds
│   └── lynx_logo_light.png    # Logo for dark backgrounds
├── Lynx Apartment Tracker.xlsx # Main data file
├── lynx_custom_metrics.json    # Custom metrics configuration
├── lynx_custom_graphs.json     # Custom graphs configuration
└── lynx_report_templates.json  # Report templates
```

## ☁️ Deployment to Streamlit Cloud

This project is configured for deployment to Streamlit Cloud. See [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md) for detailed deployment steps.

### Quick Deploy

1. **Prepare for GitHub**:
   ```bash
   # Windows
   deploy_to_github.bat
   
   # Or PowerShell
   .\deploy_to_github.ps1
   ```

2. **Deploy to Streamlit Cloud**:
   - Go to https://share.streamlit.io/
   - Connect your GitHub account
   - Grant access to private repositories
   - Select your repository and deploy

## 🔐 Configuration

### Secrets (Optional)

If you need to configure email, Google Drive, or other integrations:

1. Copy the example secrets file:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml` with your credentials

3. **For Streamlit Cloud**: Add secrets via the Cloud dashboard (Settings → Secrets)

**Note**: Never commit `secrets.toml` to Git. It's already in `.gitignore`.

## 📊 Data File

The app reads data from `Lynx Apartment Tracker.xlsx`. This file should contain:

- **Bookings** sheet: Booking data with dates, platforms, revenue, etc.
- **Monthly_Costs** sheet: Fixed monthly expenses
- **Toiletries** sheet: Toiletries inventory and costs

## 🎯 Key Metrics

- **Reservations**: Number of completed bookings
- **Total Nights**: Sum of booked nights
- **Occupancy (%)**: Percentage of available nights booked
- **Total Revenue (€)**: Total income from bookings
- **Net Profit (€)**: Revenue minus all expenses
- **ADR (Average Daily Rate)**: Average revenue per night
- **RevPAR**: Revenue per available room
- **Profit Margin (%)**: Profit as percentage of revenue

## 🔧 Customization

### Custom Metrics

Create custom metrics by editing `lynx_custom_metrics.json` or using the in-app Custom Metrics manager.

### Custom Graphs

Build custom visualizations by editing `lynx_custom_graphs.json` or using the in-app Custom Graphs manager.

### Report Templates

Define report templates in `lynx_report_templates.json` or use the in-app Report Templates manager.

## 📝 License

This project is private and proprietary.

## 🤝 Support

For issues or questions:
- Check [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md) for deployment help
- Review Streamlit documentation: https://docs.streamlit.io/

## 🔄 Updates

To update the deployed app:
1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description"
   git push
   ```
3. Streamlit Cloud will automatically redeploy

---

**Built with ❤️ using Streamlit**

