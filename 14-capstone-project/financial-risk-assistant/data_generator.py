"""Generate synthetic financial data for RAG and testing."""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set seed for reproducible test case generation
random.seed(42)


def generate_synthetic_risk_patterns(num_patterns: int = 100) -> list:
    """Generate realistic historical AML/fraud patterns for RAG corpus."""
    patterns = []

    risk_definitions = [
        {
            "type": "structuring",
            "name": "Structuring (Smurfing)",
            "description": "Multiple deposits or transfers just below CTR threshold ($10k) to avoid reporting requirements. Often involves multiple individuals depositing cash into same account or rapid onboarding of related accounts.",
            "indicators": [
                "Series of transactions in $9,500-$9,999 range",
                "Multiple deposits by different individuals to single account",
                "Rapid account openings followed by immediate deposits",
                "Pattern repeats monthly or weekly with mathematical precision",
                "Deposits followed by immediate wire transfers to third parties",
            ],
            "severity": "high",
            "regulatory_basis": "Bank Secrecy Act (BSA), FinCEN Guidance on Structuring, FATF Recommendation 10",
        },
        {
            "type": "layering",
            "name": "Layering & Obfuscation",
            "description": "Complex movement of funds through multiple accounts, entities, and jurisdictions to obscure the origin and ultimate beneficial owner. Involves trade-based ML, invoice manipulation, and shell company networks.",
            "indicators": [
                "Funds flow through 5+ intermediaries before final destination",
                "Involvement of multiple shell companies in different jurisdictions",
                "Mismatched invoice amounts vs. actual shipment values",
                "Multiple wire transfers within same business day",
                "Use of trade finance for non-existent or phantom shipments",
            ],
            "severity": "high",
            "regulatory_basis": "FATF 40 Recommendations, FinCEN Typology Reports, Basel AML Index",
        },
        {
            "type": "unusual_velocity",
            "name": "Unusual Transaction Velocity",
            "description": "Sudden spike in transaction frequency or volume that deviates significantly from customer's historical baseline. Indicator of account compromise, sudden business expansion, or illicit activity.",
            "indicators": [
                "Account with average 2 txns/month suddenly shows 20+ txns/day",
                "Outbound velocity increases >500% month-over-month",
                "High-value transactions originating from previously inactive customer",
                "Geolocation changes concurrent with velocity spike",
                "New payee introduction with high-value transfers",
            ],
            "severity": "medium",
            "regulatory_basis": "OFAC Guidance, FinCEN SAR Filing Guidelines, ABA BSA/AML Handbook",
        },
        {
            "type": "round_amounts",
            "name": "Round Amount Patterns",
            "description": "Consistent use of exact round numbers (e.g., $10,000 flat) in transactions, suggesting deliberate avoidance of scrutiny or mathematical manipulation. Often combined with structuring.",
            "indicators": [
                "All transactions exactly $10,000 or multiples thereof",
                "No variation in transaction amounts over 20+ txns",
                "Round amounts to specific jurisdictions but varied domestically",
                "Amounts just below reporting thresholds",
            ],
            "severity": "medium",
            "regulatory_basis": "FinCEN Structuring Guidance, CTR Filing Requirements",
        },
        {
            "type": "cross_border_spike",
            "name": "Unexpected Cross-Border Activity",
            "description": "Sudden initiation of international transfers to high-risk jurisdictions, especially when customer has no documented business or personal ties. May indicate sanctions evasion or trade-based ML.",
            "indicators": [
                "First wire transfer to high-risk country within 30 days of account opening",
                "Domestic customer suddenly sends 10+ wires to FATF Grey List jurisdictions",
                "Transfers to sanctioned country entities or sanctioned individuals",
                "Use of informal value transfer systems (IVTS) or hawala networks",
                "Multiple transfers to same international beneficiary within hours",
            ],
            "severity": "high",
            "regulatory_basis": "OFAC Sanctions Programs, FATF Black/Grey List, Hawala Guidance",
        },
        {
            "type": "dormant_account_activation",
            "name": "Dormant Account Activation",
            "description": "Sudden high-value activity on previously dormant account (no activity for 6+ months). Classic indicator of account takeover, credential compromise, or money laundering using shell accounts.",
            "indicators": [
                "Account dormant >12 months then $250k+ wire within 48 hours",
                "Geolocation login from new jurisdiction preceded by high outbound transfer",
                "Email/password changed immediately prior to large withdrawal",
                "Multiple dormant accounts activated simultaneously by same initiator",
                "Immediate transfer to newly added beneficiary",
            ],
            "severity": "high",
            "regulatory_basis": "Fraud Detection Standards, Account Security Guidelines",
        },
        {
            "type": "negative_news",
            "name": "Adverse Media & Reputational Risk",
            "description": "Customer appears in news articles, sanctions lists, PEP databases, or adverse media related to fraud, corruption, sanctions violations, or criminal activity.",
            "indicators": [
                "Customer name matches OFAC SDN list entry",
                "Politically Exposed Person (PEP) status identified in media",
                "News articles connecting customer to sanctions violations",
                "Links to organized crime, terrorism financing, or drug trafficking",
                "Business partner or related entity in adverse media",
            ],
            "severity": "critical",
            "regulatory_basis": "OFAC List Checking, PEP Database Screening, Sanctions Regulations",
        },
        {
            "type": "beneficial_owner_mismatch",
            "name": "Beneficial Owner Mismatch",
            "description": "Transaction parties or control patterns don't align with declared beneficial ownership or corporate structure. Suggests use of intermediaries or false documentation.",
            "indicators": [
                "Account funded by entity A but controlled transactions to entity C",
                "Director listed as beneficial owner but funds flow patterns show different party in control",
                "Funds pass through company but don't align with stated business operations",
                "Beneficial owner changes shortly before high-value transactions",
                "Related party transactions at unfavorable rates",
            ],
            "severity": "high",
            "regulatory_basis": "CDD/EDD Requirements, BO Identification Rules, FATF Recommendation 24",
        },
        {
            "type": "trade_based_ml",
            "name": "Trade-Based Money Laundering",
            "description": "Use of international trade to move value and obscure illicit proceeds. Involves over/under-invoicing, phantom shipments, or inconsistent trade flows.",
            "indicators": [
                "Invoice amount 2-3x higher than comparable market rates",
                "Consistent pattern of invoice mismatches (90%+ variance)",
                "Shipments to high-risk jurisdictions with no established trade relationship",
                "Imports of high-value luxury goods with immediate re-export at discount",
                "Services invoiced without corresponding documentation",
            ],
            "severity": "high",
            "regulatory_basis": "FATF Trade-Based ML Report, FinCEN Typology Guidance, ICC UCP 600",
        },
    ]

    # Generate multiple instances of each pattern type for diversity
    for i in range(num_patterns):
        base_pattern = random.choice(risk_definitions)
        pattern = {
            "id": f"pattern_{i+1:04d}",
            "risk_type": base_pattern["type"],
            "risk_name": base_pattern["name"],
            "description": base_pattern["description"],
            "indicators": base_pattern["indicators"],
            "historical_outcome": random.choice(
                [
                    "confirmed_fraud",
                    "sanctions_violation",
                    "aml_red_flag",
                    "escalated",
                    "false_positive",
                ]
            ),
            "severity": base_pattern["severity"],
            "regulatory_basis": base_pattern["regulatory_basis"],
            "case_count": random.randint(10, 200),
            "detection_rate": round(random.uniform(0.65, 0.95), 2),
            "created_at": (datetime.now() - timedelta(days=random.randint(30, 730))).isoformat(),
        }
        patterns.append(pattern)

    return patterns


def generate_policy_documents(num_docs: int = 50) -> list:
    """Generate realistic internal compliance policies and guidelines."""
    policies = []

    policy_templates = [
        {
            "type": "aml_policy",
            "title": "Group Anti-Money Laundering (AML) Policy and Compliance Framework",
            "content": "This policy establishes the Bank's commitment to combating money laundering, terrorist financing, and sanctions violations in accordance with the Bank Secrecy Act (BSA), AML Act, OFAC regulations, and FATF Recommendations. All employees must complete annual AML training. Suspicious activities must be reported via SAR within 30 days. Transaction monitoring systems screen all deposits >$10k, wire transfers >$5k, and unusual patterns. Enhanced due diligence (EDD) required for PEPs, high-risk jurisdictions, and beneficial owners from countries on OFAC/FATF lists.",
            "thresholds": {
                "sar_filing": "$10,000+",
                "ctr_reporting": "$10,000+",
                "cdd_review": "All new accounts",
            },
            "update_frequency": "Annual",
        },
        {
            "type": "kyc_guidelines",
            "title": "Enhanced Know Your Customer (KYC) & Customer Due Diligence (CDD) Standards",
            "content": "All customers undergo KYC verification before account opening. For individuals: government-issued ID, address verification, beneficial ownership confirmation. For entities: corporate registration, bylaws, beneficial owner list (BO certification), source of funds documentation. Enhanced Due Diligence (EDD) required for: PEPs (Politically Exposed Persons), customers from high-risk jurisdictions (FATF grey/black list), cash-intensive businesses, high net worth individuals (>$5M). Ongoing monitoring: quarterly review of high-risk customers, annual review of medium-risk, biennial review of low-risk.",
            "acceptable_docs": [
                "Passport",
                "Driver's License",
                "National ID",
                "Corporate Registration",
            ],
            "update_frequency": "Quarterly",
        },
        {
            "type": "transaction_limits",
            "title": "Transaction Amount and Frequency Thresholds",
            "content": "Domestic transfers: Individual limit $100k/day, $500k/month unless enhanced verification provided. Wire transfers: $50k+ requires management approval, >$250k requires C-level approval and EDD. International wires to high-risk jurisdictions: $10k+ limit, all subject to OFAC screening. ATM withdrawals: $5k/day limit, daily aggregate $20k. Multiple transactions in 24hrs totaling >$50k trigger structuring review. Round amounts >3 times in 30 days trigger compliance alert.",
            "limits": {
                "domestic_daily": "$100k",
                "international_daily": "$25k",
                "atm_daily": "$5k",
            },
            "update_frequency": "Monthly",
        },
        {
            "type": "high_risk_jurisdictions",
            "title": "High-Risk Jurisdiction Watchlist and Country-Based Screening",
            "content": "Countries classified as high-risk require enhanced screening and monitoring: FATF Black List (North Korea, Iran), FATF Grey List (actively monitored countries), OFAC SDN countries (Russia, Syria, Cuba). Additional scrutiny for: countries with weak AML/CFT regimes, countries with significant corruption, countries known for sanctions evasion. Transactions involving these jurisdictions: mandatory EDD, management override required, SAR filing if proceeds suspected illicit. Monthly review of new additions to sanctions lists.",
            "blacklist_countries": ["KP", "IR", "CU", "SY"],
            "greylist_countries": ["RU", "BY", "VZ"],
            "update_frequency": "Daily (automated OFAC sync)",
        },
        {
            "type": "escalation_procedures",
            "title": "Case Escalation Decision Framework and Approval Workflows",
            "content": "Risk scores 0.0-0.3: APPROVE (standard processing). Risk scores 0.3-0.6: MANUAL_REVIEW (escalate to Risk Committee). Risk scores 0.6-1.0: BLOCK/SAR FILE (escalate to Compliance Officer, notify OFAC). Hard gates override: Sanctions hits = BLOCK immediately, CTR >$100k = mandatory SAR, Structuring pattern = BLOCK + SAR. Approval authority: Risk Analyst (escalate), Risk Committee (>$50k or >0.5 risk), Compliance Officer (SAR decisions), Legal Counsel (regulatory exposure >$1M). All blocks documented within 2 business days.",
            "risk_thresholds": {
                "approve": "0.0-0.3",
                "manual_review": "0.3-0.6",
                "block": "0.6-1.0",
            },
            "update_frequency": "Quarterly",
        },
        {
            "type": "sanctions_policy",
            "title": "OFAC Sanctions Screening & Compliance Program",
            "content": "All customers, beneficiaries, and related parties screened against OFAC SDN list at account opening and daily during active periods. Screening includes: exact name match, phonetic match (90%+ threshold), name variants, common aliases. Hits require manual review: confirm false positive or initiate blocking. Confirmed sanctions hits: block transaction immediately, freeze account, file Blocking Report within 10 days. Monthly OFAC list updates downloaded and integrated into screening database. Staff training on OFAC compliance required annually.",
            "screening_threshold": "90% name match confidence",
            "false_positive_resolution": "Within 48 hours",
            "update_frequency": "Weekly (OFAC sync)",
        },
    ]

    for i in range(num_docs):
        template = random.choice(policy_templates)
        policy = {
            "id": f"policy_{i+1:03d}",
            "type": template["type"],
            "title": template["title"],
            "content": template["content"],
            "effective_date": (
                datetime.now() - timedelta(days=random.randint(90, 730))
            ).isoformat(),
            "last_reviewed": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
            "version": f"v{random.randint(2, 4)}.{random.randint(0, 3)}",
            "regulatory_references": [
                "FinCEN Guidance",
                "OFAC Regulations",
                "FATF Recommendations",
                "OMB Guidance",
            ],
            "key_thresholds": template.get("thresholds") or template.get("limits") or {},
            "severity_level": (
                "critical" if template["type"] in ["aml_policy", "sanctions_policy"] else "warning"
            ),
        }
        policies.append(policy)

    return policies


def generate_investigation_playbooks(num_playbooks: int = 20) -> list:
    """Generate realistic investigation playbooks based on AML scenarios."""
    playbooks = []

    playbook_scenarios = [
        {
            "scenario": "Structuring Detection",
            "steps": [
                "1. Verify transaction amounts are consistently below $10k CTR threshold",
                "2. Check if deposits follow mathematical pattern (e.g., $9,900 repeated)",
                "3. Identify source of funds via ID verification and beneficiary documentation",
                "4. Review account for multiple related depositors or rapid account openings",
                "5. Check if funds immediately transferred out to third parties",
                "6. Pull transaction timeline for past 90-180 days to establish pattern",
                "7. Interview account holder regarding deposit source and beneficiaries",
                "8. File SAR if structuring intent confirmed (Recommendation 10 violation)",
            ],
            "indicators": [
                "Round amounts",
                "Multiple depositors",
                "Immediate transfers out",
                "CTR avoidance pattern",
            ],
            "approval_authority": "Compliance Officer",
            "escalation_trigger": "Pattern of 5+ transactions in 30 days below threshold",
        },
        {
            "scenario": "Sanctions List Hit",
            "steps": [
                "1. Confirm name match confidence level (90%+ vs manual review)",
                "2. Cross-reference with multiple OFAC lists (SDN, HQ, Blocked List)",
                "3. Check for exact name match vs. phonetic/potential false positive",
                "4. Verify account opening date and historical transactions",
                "5. Block account immediately to prevent further transactions",
                "6. Freeze all assets and segregate into suspense account",
                "7. File OFAC Blocking Report within 10 calendar days",
                "8. Notify customer if account blocked (after legal review)",
                "9. Report to FinCEN SAR within 30 days if proceeds involved",
            ],
            "indicators": ["OFAC SDN match", "High-risk jurisdiction origin", "PEP identification"],
            "approval_authority": "Legal/Compliance Officer",
            "escalation_trigger": "Sanctions list match = immediate block",
        },
        {
            "scenario": "High-Value Wire to High-Risk Jurisdiction",
            "steps": [
                "1. Verify beneficiary identity and jurisdiction (check FATF black/grey list)",
                "2. Confirm legitimate business purpose with customer (obtain written explanation)",
                "3. Review invoice/documentation supporting claimed transaction purpose",
                "4. Cross-reference beneficiary against OFAC/PEP databases",
                "5. Assess account history for consistency with stated business",
                "6. Verify beneficiary bank is not on high-risk institution list",
                "7. Implement Enhanced Due Diligence (EDD) including source of funds verification",
                "8. Obtain senior management approval for wire >$100k",
                "9. Document decision with full file memo",
                "10. Monitor beneficiary account for suspicious onward transfers",
            ],
            "indicators": [
                "Wire >$50k",
                "High-risk destination",
                "No prior history",
                "Mismatched business purpose",
            ],
            "approval_authority": "VP Risk Management",
            "escalation_trigger": "Wire >$250k to grey/black list country",
        },
        {
            "scenario": "Dormant Account Activation",
            "steps": [
                "1. Confirm account has been dormant >6 months with no transactions",
                "2. Review login patterns for geolocation changes immediately prior to withdrawal",
                "3. Verify if credentials were reset or email address changed recently",
                "4. Check for new beneficiaries added to account within 30 days of reactivation",
                "5. Assess if transaction amount is anomalous relative to historical avg",
                "6. Contact account holder to confirm legitimate business purpose",
                "7. If unable to verify ownership, implement re-KYC process",
                "8. Flag for fraud investigation if indicators of account compromise detected",
                "9. If confirmed fraud, freeze account and report to law enforcement",
            ],
            "indicators": [
                "6+ months inactivity",
                "Geolocation anomaly",
                "New beneficiary",
                "Large withdrawal",
            ],
            "approval_authority": "Fraud Investigation Team",
            "escalation_trigger": "Any withdrawal >$50k after 12+ month dormancy",
        },
        {
            "scenario": "Trade-Based Money Laundering Suspicion",
            "steps": [
                "1. Compare invoice amount with market rates for similar goods/services",
                "2. Identify if invoice >2x comparable market value (over-invoicing)",
                "3. Verify if shipment actually occurred (tracking, customs documentation)",
                "4. Confirm exporter/importer legitimate business history",
                "5. Review payment terms for consistency with industry standards",
                "6. Assess if goods appropriate for receiving country's economy/development",
                "7. Verify bill of lading matches invoice and actual goods shipped",
                "8. Check if similar invoicing pattern exists with other trading partners",
                "9. If >30% invoice variance confirmed, file SAR for trade-based ML",
                "10. Coordinate with OFAC/FinCEN if sanctioned country involvement",
            ],
            "indicators": [
                "Invoice mismatch >30%",
                "High-value goods to low-dev country",
                "Multiple intermediaries",
            ],
            "approval_authority": "Trade Finance Compliance",
            "escalation_trigger": "Any invoice variance >25% for international transactions >$100k",
        },
        {
            "scenario": "Unusual Transaction Velocity",
            "steps": [
                "1. Establish baseline: calculate average transactions/month for past 12 months",
                "2. Identify spike: current velocity vs. baseline (flag if >300% increase)",
                "3. Categorize transaction types: are new types appearing (e.g., international)?",
                "4. Review beneficiary patterns: new payees appearing? Concentration vs. diversification?",
                "5. Assess account funding: any new deposit patterns or large inbound transfers?",
                "6. Check if velocity spike correlates with account changes (new signers, owner changes)",
                "7. Contact account holder for business explanation of activity increase",
                "8. If business explanation inconsistent with account activity, escalate",
                "9. Implement enhanced monitoring: daily alert thresholds",
                "10. Document findings and risk assessment in file",
            ],
            "indicators": [
                "500%+ velocity increase",
                "New transaction types",
                "Geolocation changes",
                "New beneficiaries",
            ],
            "approval_authority": "Risk Committee",
            "escalation_trigger": ">1000% velocity spike month-over-month",
        },
    ]

    for i in range(num_playbooks):
        scenario = random.choice(playbook_scenarios)
        playbook = {
            "id": f"playbook_{i+1:03d}",
            "scenario": scenario["scenario"],
            "investigation_steps": scenario["steps"],
            "key_indicators": scenario["indicators"],
            "escalation_threshold": scenario["escalation_trigger"],
            "approval_authority": scenario["approval_authority"],
            "estimated_investigation_hours": random.randint(4, 16),
            "created_date": (datetime.now() - timedelta(days=random.randint(60, 365))).isoformat(),
            "sar_filing_likelihood": round(random.uniform(0.4, 0.95), 2),
        }
        playbooks.append(playbook)

    return playbooks


def generate_test_cases() -> list:
    """Generate realistic and diverse test transaction cases."""
    test_cases = []

    # Low-risk routine cases
    low_risk_templates = [
        # Salary deposits
        {
            "customer_id": "emp_john_smith",
            "amount": 4500,
            "type": "transfer",
            "channel": "online",
            "location": "US",
            "account_age": 1460,
            "txn_count": 156,
            "monthly_avg": 9000,
        },
        {
            "customer_id": "emp_maria_garcia",
            "amount": 3800,
            "type": "transfer",
            "channel": "online",
            "location": "US",
            "account_age": 2190,
            "txn_count": 312,
            "monthly_avg": 7600,
        },
        # Utility/household payments
        {
            "customer_id": "cust_emily_davis",
            "amount": 250,
            "type": "payment",
            "channel": "mobile_app",
            "location": "US",
            "account_age": 730,
            "txn_count": 78,
            "monthly_avg": 1200,
        },
        {
            "customer_id": "cust_robert_wilson",
            "amount": 450,
            "type": "payment",
            "channel": "online",
            "location": "UK",
            "account_age": 1095,
            "txn_count": 234,
            "monthly_avg": 1800,
        },
        # ATM withdrawals
        {
            "customer_id": "cust_lisa_anderson",
            "amount": 500,
            "type": "withdrawal",
            "channel": "atm",
            "location": "US",
            "account_age": 548,
            "txn_count": 92,
            "monthly_avg": 2000,
        },
        {
            "customer_id": "cust_james_brown",
            "amount": 300,
            "type": "withdrawal",
            "channel": "atm",
            "location": "DE",
            "account_age": 2920,
            "txn_count": 445,
            "monthly_avg": 1500,
        },
    ]

    # Medium-risk escalation cases
    medium_risk_templates = [
        # Business payments - higher amounts for manual_review trigger
        {
            "customer_id": "biz_acme_corp",
            "amount": 20000,
            "type": "transfer",
            "channel": "online",
            "location": "US",
            "account_age": 365,
            "txn_count": 23,
            "monthly_avg": 45000,
        },
        {
            "customer_id": "biz_tech_solutions",
            "amount": 15000,
            "type": "payment",
            "channel": "online",
            "location": "US",
            "account_age": 180,
            "txn_count": 12,
            "monthly_avg": 28000,
        },
        # International but moderate amount
        {
            "customer_id": "traveler_david_lee",
            "amount": 8000,
            "type": "transfer",
            "channel": "online",
            "location": "UK",
            "account_age": 1095,
            "txn_count": 156,
            "monthly_avg": 3500,
        },
    ]

    # High-risk flagged cases (should trigger BLOCK)
    high_risk_templates = [
        # Structuring pattern - large amounts to trigger block threshold
        {
            "customer_id": "struct_user_001",
            "amount": 55000,
            "type": "transfer",
            "channel": "online",
            "location": "US",
            "account_age": 45,
            "txn_count": 3,
            "monthly_avg": 12000,
        },
        # Sanctioned entity
        {
            "customer_id": "bashar al-assad",
            "amount": 50000,
            "type": "transfer",
            "channel": "wire_transfer",
            "location": "SY",
            "account_age": 60,
            "txn_count": 2,
            "monthly_avg": 0,
        },
        # Large international to high-risk
        {
            "customer_id": "biz_middleman_corp",
            "amount": 250000,
            "type": "transfer",
            "channel": "wire_transfer",
            "location": "RU",
            "account_age": 30,
            "txn_count": 1,
            "monthly_avg": 0,
        },
        # Dormant activation spike
        {
            "customer_id": "cust_dormant_2019",
            "amount": 120000,
            "type": "withdrawal",
            "channel": "wire_transfer",
            "location": "IR",
            "account_age": 2190,
            "txn_count": 0,
            "monthly_avg": 0,
        },
        # Velocity spike
        {
            "customer_id": "cust_sudden_trader",
            "amount": 65000,
            "type": "transfer",
            "channel": "international",
            "location": "KP",
            "account_age": 90,
            "txn_count": 8,
            "monthly_avg": 500,
        },
    ]

    case_id = 1

    # Generate 12 low-risk cases (expected_decision: approve)
    for _ in range(12):
        template = random.choice(low_risk_templates)
        test_cases.append(
            {
                "case_id": f"test_approve_{case_id:03d}",
                "customer_id": template["customer_id"],
                "transaction_amount": template["amount"] + random.randint(-200, 500),
                "transaction_type": template["type"],
                "channel": template["channel"],
                "device_location": template["location"],
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
                "customer_profile": {
                    "account_age_days": template["account_age"],
                    "avg_monthly_volume": template["monthly_avg"],
                    "previous_txn_count": template["txn_count"],
                    "country_of_residence": template["location"],
                },
                "expected_decision": "approve",
            }
        )
        case_id += 1

    # Generate 5 medium-risk cases (expected_decision: manual_review)
    for _ in range(5):
        template = random.choice(medium_risk_templates)
        test_cases.append(
            {
                "case_id": f"test_review_{case_id:03d}",
                "customer_id": template["customer_id"],
                "transaction_amount": template["amount"] + random.randint(-500, 1000),
                "transaction_type": template["type"],
                "channel": template["channel"],
                "device_location": template["location"],
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                "customer_profile": {
                    "account_age_days": template["account_age"],
                    "avg_monthly_volume": template["monthly_avg"],
                    "previous_txn_count": template["txn_count"],
                    "country_of_residence": template["location"],
                },
                "expected_decision": "manual_review",
            }
        )
        case_id += 1

    # Generate 8 high-risk cases (expected_decision: block)
    for _ in range(8):
        template = random.choice(high_risk_templates)
        test_cases.append(
            {
                "case_id": f"test_block_{case_id:03d}",
                "customer_id": template["customer_id"],
                "transaction_amount": template["amount"] + random.randint(-2000, 2000),
                "transaction_type": template["type"],
                "channel": template["channel"],
                "device_location": template["location"],
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat(),
                "customer_profile": {
                    "account_age_days": template["account_age"],
                    "avg_monthly_volume": template["monthly_avg"],
                    "previous_txn_count": template["txn_count"],
                    "country_of_residence": template["location"],
                },
                "expected_decision": "block",
            }
        )
        case_id += 1

    return test_cases


def generate_edge_test_cases() -> list:
    """Generate deterministic edge-case scenarios for robustness testing."""
    now = datetime.now().isoformat()
    return [
        {
            "case_id": "edge_001_zero_amount",
            "customer_id": "cust_zero_amount",
            "transaction_amount": 0.0,
            "transaction_type": "payment",
            "channel": "online",
            "device_location": "US",
            "timestamp": now,
            "customer_profile": {
                "account_age_days": 365,
                "avg_monthly_volume": 500,
                "previous_txn_count": 90,
                "country_of_residence": "US",
            },
            "expected_decision": "approve",
            "edge_case_tag": "zero_amount",
        },
        {
            "case_id": "edge_002_missing_customer_id",
            "customer_id": None,
            "transaction_amount": 1500.0,
            "transaction_type": "transfer",
            "channel": "online",
            "device_location": "US",
            "timestamp": now,
            "customer_profile": {
                "account_age_days": 120,
                "avg_monthly_volume": 3000,
                "previous_txn_count": 40,
                "country_of_residence": "US",
            },
            "expected_decision": "manual_review",
            "edge_case_tag": "missing_required_field",
        },
        {
            "case_id": "edge_003_negative_amount",
            "customer_id": "cust_negative_amount",
            "transaction_amount": -10.0,
            "transaction_type": "payment",
            "channel": "mobile_app",
            "device_location": "US",
            "timestamp": now,
            "customer_profile": {
                "account_age_days": 400,
                "avg_monthly_volume": 800,
                "previous_txn_count": 150,
                "country_of_residence": "US",
            },
            "expected_decision": "manual_review",
            "edge_case_tag": "invalid_amount",
        },
        {
            "case_id": "edge_004_invalid_channel",
            "customer_id": "cust_invalid_channel",
            "transaction_amount": 750.0,
            "transaction_type": "transfer",
            "channel": "chatbot",
            "device_location": "DE",
            "timestamp": now,
            "customer_profile": {
                "account_age_days": 210,
                "avg_monthly_volume": 2600,
                "previous_txn_count": 65,
                "country_of_residence": "DE",
            },
            "expected_decision": "manual_review",
            "edge_case_tag": "invalid_channel",
        },
        {
            "case_id": "edge_005_large_amount_hard_gate",
            "customer_id": "cust_large_amount",
            "transaction_amount": 250000.0,
            "transaction_type": "transfer",
            "channel": "wire_transfer",
            "device_location": "US",
            "timestamp": now,
            "customer_profile": {
                "account_age_days": 10,
                "avg_monthly_volume": 400,
                "previous_txn_count": 2,
                "country_of_residence": "US",
            },
            "expected_decision": "block",
            "edge_case_tag": "hard_gate_amount",
        },
        {
            "case_id": "edge_006_high_risk_country",
            "customer_id": "cust_high_risk_geo",
            "transaction_amount": 12000.0,
            "transaction_type": "transfer",
            "channel": "international",
            "device_location": "IR",
            "timestamp": now,
            "customer_profile": {
                "account_age_days": 20,
                "avg_monthly_volume": 900,
                "previous_txn_count": 3,
                "country_of_residence": "IR",
            },
            "expected_decision": "manual_review",
            "edge_case_tag": "high_risk_country",
        },
    ]


def save_synthetic_data(output_dir: str = "data"):
    """Generate and save all synthetic data to JSON files."""
    Path(output_dir).mkdir(exist_ok=True)

    print("Generating synthetic data...")

    patterns = generate_synthetic_risk_patterns(100)
    with open(f"{output_dir}/risk_patterns.json", "w", encoding="utf-8") as f:
        json.dump(patterns, f, indent=2)
        print(f"[OK] Generated {len(patterns)} risk patterns")

    policies = generate_policy_documents(50)
    with open(f"{output_dir}/policies.json", "w", encoding="utf-8") as f:
        json.dump(policies, f, indent=2)
        print(f"[OK] Generated {len(policies)} policy documents")

    playbooks = generate_investigation_playbooks(20)
    with open(f"{output_dir}/playbooks.json", "w", encoding="utf-8") as f:
        json.dump(playbooks, f, indent=2)
        print(f"[OK] Generated {len(playbooks)} investigation playbooks")

    test_cases = generate_test_cases()
    with open(f"{output_dir}/test_cases.json", "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2)
        print(f"[OK] Generated {len(test_cases)} test cases")

    edge_cases = generate_edge_test_cases()
    with open(f"{output_dir}/edge_test_cases.json", "w", encoding="utf-8") as f:
        json.dump(edge_cases, f, indent=2)
        print(f"[OK] Generated {len(edge_cases)} edge test cases")

    print(f"All synthetic data saved to {output_dir}/")


if __name__ == "__main__":
    save_synthetic_data()
