"""
Generate synthetic financial data for Kazakhstani banks.
Creates realistic quarterly reports for Halyk Bank, Kaspi Bank, and ForteBank.
"""
import json
import os
import random
from datetime import datetime


def generate_bank_data(bank_name, base_assets, base_branches, digital_focused=False):
    """
    Generate realistic financial data for a bank across 4 quarters of 2024.
    
    Args:
        bank_name: Name of the bank
        base_assets: Starting total assets in billion KZT
        base_branches: Number of branches
        digital_focused: Whether the bank is primarily digital
    """
    reports = []
    
    # Base growth rates (quarterly)
    asset_growth = 1.02 if not digital_focused else 1.04
    profit_margin = 0.015 if not digital_focused else 0.025
    
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    
    for i, quarter in enumerate(quarters):
        # Calculate growing metrics
        total_assets = base_assets * (asset_growth ** i)
        loans = total_assets * random.uniform(0.55, 0.65)
        deposits = total_assets * random.uniform(0.70, 0.80)
        net_profit = total_assets * profit_margin * random.uniform(0.9, 1.1)
        
        # Ratios
        roe = (net_profit / (total_assets * 0.12)) * 100
        roa = (net_profit / total_assets) * 100
        capital_adequacy = random.uniform(16, 22)
        npl_ratio = random.uniform(3, 8)
        cost_income = random.uniform(35, 45)
        
        # Operational metrics
        branches = base_branches + random.randint(-2, 5) if not digital_focused else base_branches
        atms = branches * random.randint(3, 6)
        employees = branches * random.randint(15, 25)
        active_clients = int(total_assets * random.uniform(100, 300))
        digital_clients = int(active_clients * (0.85 if digital_focused else 0.60))
        
        # Market share
        market_share = random.uniform(15, 25) if bank_name == "Halyk Bank" else random.uniform(10, 20)
        
        # Financial Statement Report
        financial_report = {
            "bank_name": bank_name,
            "quarter": quarter,
            "year": 2024,
            "report_type": "financial_statement",
            "content": f"""
{bank_name} - {quarter} 2024 Financial Statement

BALANCE SHEET HIGHLIGHTS:
- Total Assets: {total_assets:.2f} billion KZT (growth: {((asset_growth ** i - 1) * 100):.1f}% YTD)
- Loans Portfolio: {loans:.2f} billion KZT ({(loans/total_assets*100):.1f}% of total assets)
- Customer Deposits: {deposits:.2f} billion KZT ({(deposits/total_assets*100):.1f}% of total assets)

INCOME STATEMENT:
- Net Profit: {net_profit:.2f} billion KZT
- Return on Equity (ROE): {roe:.2f}%
- Return on Assets (ROA): {roa:.2f}%
- Net Interest Margin: {random.uniform(4.5, 6.5):.2f}%

CAPITAL & RISK METRICS:
- Capital Adequacy Ratio: {capital_adequacy:.2f}% (Basel III requirement: 12.5%)
- Tier 1 Capital Ratio: {capital_adequacy - random.uniform(2, 4):.2f}%
- Non-Performing Loans (NPL) Ratio: {npl_ratio:.2f}%
- Loan Loss Coverage: {random.uniform(85, 120):.1f}%
- Cost-to-Income Ratio: {cost_income:.1f}%

LIQUIDITY:
- Liquidity Coverage Ratio (LCR): {random.uniform(140, 180):.1f}%
- Net Stable Funding Ratio (NSFR): {random.uniform(110, 130):.1f}%
- Loan-to-Deposit Ratio: {(loans/deposits*100):.1f}%

The bank maintains strong capital buffers and healthy liquidity positions, demonstrating robust financial health in {quarter} 2024.
            """.strip()
        }
        
        # Operational Metrics Report
        operational_report = {
            "bank_name": bank_name,
            "quarter": quarter,
            "year": 2024,
            "report_type": "operational_metrics",
            "content": f"""
{bank_name} - {quarter} 2024 Operational Metrics

NETWORK INFRASTRUCTURE:
- Total Branches: {branches} locations nationwide
- ATM Network: {atms} machines
- Self-Service Terminals: {atms + random.randint(100, 300)}
- Employee Count: {employees:,} professionals

CLIENT BASE:
- Total Active Clients: {active_clients:,} customers
- Digital Banking Users: {digital_clients:,} ({(digital_clients/active_clients*100):.1f}% digitalization rate)
- New Clients This Quarter: {int(active_clients * random.uniform(0.02, 0.05)):,}
- Corporate Clients: {int(active_clients * 0.05):,}
- Retail Clients: {int(active_clients * 0.95):,}

DIGITAL BANKING PERFORMANCE:
- Mobile App Downloads: {digital_clients * random.uniform(0.8, 1.2):.0f}
- Active Mobile Users: {int(digital_clients * random.uniform(0.65, 0.85)):,}
- Online Transactions Volume: {random.uniform(5, 15):.1f} million transactions
- Digital Transaction Share: {random.uniform(75, 92):.1f}% of all transactions
- Average Mobile App Rating: {random.uniform(4.3, 4.8):.1f}/5.0

PRODUCT PENETRATION:
- Cards Issued: {int(active_clients * random.uniform(1.2, 1.8)):,} total cards
- Credit Cards: {int(active_clients * random.uniform(0.3, 0.5)):,}
- Debit Cards: {int(active_clients * random.uniform(0.8, 1.2)):,}
- Active Loan Accounts: {int(active_clients * random.uniform(0.15, 0.25)):,}
- Deposit Accounts: {int(active_clients * random.uniform(0.6, 0.9)):,}

EFFICIENCY METRICS:
- Transactions per Employee: {random.randint(200, 400)} per day
- Average Service Time: {random.uniform(3, 7):.1f} minutes
- Customer Satisfaction Score (NPS): {random.randint(35, 65)}
- Employee Productivity Index: {random.uniform(85, 95):.1f}%

{bank_name} continues to expand its digital capabilities while maintaining a strong physical presence across Kazakhstan.
            """.strip()
        }
        
        # Market Analysis Report
        market_report = {
            "bank_name": bank_name,
            "quarter": quarter,
            "year": 2024,
            "report_type": "market_analysis",
            "content": f"""
{bank_name} - {quarter} 2024 Market Analysis & Strategic Overview

MARKET POSITION:
- Market Share by Assets: {market_share:.2f}%
- Market Share by Loans: {market_share * random.uniform(0.9, 1.1):.2f}%
- Market Share by Deposits: {market_share * random.uniform(0.95, 1.05):.2f}%
- Ranking in Kazakhstan: {"#1" if bank_name == "Halyk Bank" else "#2" if bank_name == "Kaspi Bank" else "#3"}

YEAR-OVER-YEAR COMPARISON:
- Asset Growth YoY: {random.uniform(8, 18):.1f}%
- Loan Portfolio Growth YoY: {random.uniform(10, 20):.1f}%
- Deposit Growth YoY: {random.uniform(7, 15):.1f}%
- Net Profit Growth YoY: {random.uniform(5, 25):.1f}%
- Client Base Growth YoY: {random.uniform(8, 15):.1f}%

COMPETITIVE ADVANTAGES:
{"- Leading digital banking platform with 90%+ digitalization" if digital_focused else "- Largest branch network nationwide with comprehensive coverage"}
- Strong capital position exceeding regulatory requirements
- Diversified loan portfolio across retail and corporate segments
- Advanced risk management systems
- High customer satisfaction and retention rates
- {"Innovative fintech ecosystem integration" if digital_focused else "Trusted brand with 25+ years of market presence"}

BUSINESS SEGMENTS PERFORMANCE:
Retail Banking:
- Segment Profit: {net_profit * random.uniform(0.4, 0.6):.2f} billion KZT
- Loans Outstanding: {loans * random.uniform(0.50, 0.65):.2f} billion KZT
- Customer Deposits: {deposits * random.uniform(0.55, 0.70):.2f} billion KZT

Corporate Banking:
- Segment Profit: {net_profit * random.uniform(0.25, 0.40):.2f} billion KZT
- Loans Outstanding: {loans * random.uniform(0.30, 0.45):.2f} billion KZT
- Customer Deposits: {deposits * random.uniform(0.25, 0.40):.2f} billion KZT

SME Banking:
- Segment Profit: {net_profit * random.uniform(0.10, 0.20):.2f} billion KZT
- Loans Outstanding: {loans * random.uniform(0.05, 0.15):.2f} billion KZT
- Active SME Clients: {int(active_clients * random.uniform(0.08, 0.15)):,}

STRATEGIC INITIATIVES {quarter} 2024:
- {"Expansion of digital ecosystem and super-app functionality" if digital_focused else "Network optimization and digital transformation"}
- Enhanced cybersecurity and fraud prevention systems
- {"AI-powered customer service and personalization" if digital_focused else "Customer experience improvement across all channels"}
- Sustainable finance and ESG integration
- Partnership expansion with fintech companies

RISK MANAGEMENT OVERVIEW:
- Credit Risk: Well-diversified portfolio with prudent underwriting
- Market Risk: Limited exposure, effective hedging strategies
- Operational Risk: Robust controls and business continuity plans
- Compliance: Full adherence to Basel III and local regulations

OUTLOOK:
{bank_name} is well-positioned for continued growth in the Kazakhstani banking market, supported by strong fundamentals, 
digital innovation, and commitment to customer value creation.
            """.strip()
        }
        
        reports.extend([financial_report, operational_report, market_report])
    
    return reports


def main():
    """Generate financial data for all banks."""
    print("🏦 Generating synthetic financial data for Kazakhstani banks...")
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    # Bank configurations
    banks_config = {
        "Halyk Bank": {
            "base_assets": 10500,  # billion KZT
            "base_branches": 550,
            "digital_focused": False
        },
        "Kaspi Bank": {
            "base_assets": 8200,
            "base_branches": 85,
            "digital_focused": True
        },
        "ForteBank": {
            "base_assets": 2800,
            "base_branches": 145,
            "digital_focused": False
        }
    }
    
    # Generate data for each bank
    for bank_name, config in banks_config.items():
        print(f"\n📊 Generating reports for {bank_name}...")
        reports = generate_bank_data(
            bank_name=bank_name,
            base_assets=config["base_assets"],
            base_branches=config["base_branches"],
            digital_focused=config["digital_focused"]
        )
        
        # Save to JSON file
        filename = f"data/{bank_name.lower().replace(' ', '_')}_reports.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reports, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Generated {len(reports)} reports")
        print(f"   💾 Saved to {filename}")
    
    print("\n✨ Data generation complete!")
    print(f"   Total reports: {sum(len(generate_bank_data(name, cfg['base_assets'], cfg['base_branches'], cfg['digital_focused'])) for name, cfg in banks_config.items())}")
    print(f"   Location: ./data/")


if __name__ == "__main__":
    main()