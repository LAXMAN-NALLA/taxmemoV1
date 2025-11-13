"""
Streamlit UI for Tax Memo Generator - V1
Only working fields are shown to avoid confusion
"""
import streamlit as st
import requests
import json
from typing import Dict, Any, List
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Tax Memo Generator - V1",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# V1 Banner
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏷️ Version 1.0")
st.sidebar.markdown("*Core features only. Additional fields coming in V2.*")
st.sidebar.markdown("---")

# API Configuration
API_URL = st.sidebar.text_input(
    "Backend API URL",
    value="https://taxmemov1.onrender.com",
    help="Enter your backend API URL"
)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Step definitions - Reduced to only working steps
TOTAL_STEPS = 5
STEP_NAMES = {
    1: "Company Information",
    2: "Goals & Jurisdiction",
    3: "Tax & Transactions",
    4: "Legal Topics",
    5: "Review & Generate"
}

# Industry options
INDUSTRIES = [
    "Software & Technology",
    "E-commerce & Retail",
    "Manufacturing",
    "Professional Services",
    "Financial Services",
    "Healthcare",
    "Education",
    "Media & Entertainment",
    "Other"
]

# Company size options
COMPANY_SIZES = [
    "Startup (1-10 employees)",
    "Small (11-50 employees)",
    "Medium (51-250 employees)",
    "Large (251+ employees)"
]

# Entry goals options
ENTRY_GOALS = [
    "Sell products/services",
    "Hire employees",
    "Establish physical presence",
    "Access new customer segments",
    "Tax optimization",
    "Regulatory compliance",
    "EU funding opportunities"
]

# Timeline options
TIMELINES = [
    "ASAP (within 1 month)",
    "Short-term (1-3 months)",
    "Medium-term (3-6 months)",
    "Long-term (6+ months)",
    "Just researching for now"
]

# Company types (simplified - only working ones)
COMPANY_TYPES = [
    "",
    "Holding Company",
    "Corporation",
    "LLC"
]

# Tax queries
TAX_QUERIES = [
    "Corporate income tax implications",
    "Value-added tax (VAT) registration and compliance",
    "Withholding tax on dividends, interest, and royalties",
    "Transfer pricing requirements",
    "Permanent establishment risks",
    "Tax treaty benefits and limitations",
    "Substance requirements",
    "Payroll tax obligations",
    "Double taxation prevention",
    "Participation exemption"
]

# Transaction types
TRANSACTION_TYPES = [
    "Sale of goods",
    "Provision of services",
    "Software licensing",
    "IP transfers",
    "Intra-group financing",
    "Management services",
    "Employee secondment",
    "Real estate",
    "E-commerce"
]

# Legal topics
LEGAL_TOPICS = {
    "corporate-law": "Corporate Law",
    "employment-law": "Employment Law",
    "contract-law": "Contract Law",
    "intellectual-property": "Intellectual Property",
    "data-protection": "Data Protection",
    "licensing-permits": "Licensing & Permits",
    "banking-payments": "Banking & Payments",
    "immigration": "Immigration",
    "real-estate": "Real Estate",
    "dispute-resolution": "Dispute Resolution",
    "environmental-law": "Environmental Law",
    "social-security": "Social Security & Insurance"
}

def generate_id():
    """Generate a unique ID"""
    return f"{int(datetime.now().timestamp() * 1000)}"

def step_1_company_info():
    """Step 1: Company Information"""
    st.header("📊 Company Information")
    st.markdown("Tell us about your company")
    
    # Company Name (Required)
    business_name = st.text_input(
        "Company Name *",
        value=st.session_state.form_data.get("businessName", ""),
        help="Enter your company name (required)",
        placeholder="e.g., Tech Solutions Inc"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        industry = st.selectbox(
            "Industry",
            options=[""] + INDUSTRIES,
            index=0 if not st.session_state.form_data.get("industry") else INDUSTRIES.index(st.session_state.form_data.get("industry", "")) + 1,
            help="Select your primary industry"
        )
        
        company_size = st.selectbox(
            "Company Size",
            options=[""] + COMPANY_SIZES,
            index=0 if not st.session_state.form_data.get("companySize") else COMPANY_SIZES.index(st.session_state.form_data.get("companySize", "")) + 1,
            help="Select your company size"
        )
    
    with col2:
        company_type = st.selectbox(
            "Company Type",
            options=COMPANY_TYPES,
            index=0 if not st.session_state.form_data.get("companyType") else COMPANY_TYPES.index(st.session_state.form_data.get("companyType", "")) if st.session_state.form_data.get("companyType") in COMPANY_TYPES else 0,
            help="Select your company type (optional)"
        )
        
        timeline = st.selectbox(
            "Timeline",
            options=[""] + TIMELINES,
            index=0 if not st.session_state.form_data.get("timeline") else TIMELINES.index(st.session_state.form_data.get("timeline", "")) + 1,
            help="When do you plan to enter the market?"
        )
    
    # Revenue (Optional)
    st.subheader("Revenue Information (Optional)")
    col1, col2 = st.columns(2)
    with col1:
        current_revenue = st.number_input(
            "Current Annual Revenue (€)",
            min_value=0.0,
            value=float(st.session_state.form_data.get("currentRevenue", 0)) if st.session_state.form_data.get("currentRevenue") else 0.0,
            step=10000.0,
            help="Your current annual revenue"
        )
    with col2:
        projected_revenue = st.number_input(
            "Projected Revenue in Target Market (€)",
            min_value=0.0,
            value=float(st.session_state.form_data.get("projectedRevenue", 0)) if st.session_state.form_data.get("projectedRevenue") else 0.0,
            step=10000.0,
            help="Expected revenue in the target market"
        )
    
    # Save to session state
    st.session_state.form_data["businessName"] = business_name
    st.session_state.form_data["industry"] = industry
    st.session_state.form_data["companySize"] = company_size
    st.session_state.form_data["companyType"] = company_type
    st.session_state.form_data["timeline"] = timeline
    st.session_state.form_data["currentRevenue"] = current_revenue if current_revenue > 0 else None
    st.session_state.form_data["projectedRevenue"] = projected_revenue if projected_revenue > 0 else None

def step_2_goals_jurisdiction():
    """Step 2: Goals & Jurisdiction"""
    st.header("🎯 Goals & Jurisdiction")
    st.markdown("What are your goals and where do you want to operate?")
    
    # Entry Goals
    entry_goals = st.multiselect(
        "Entry Goals",
        options=ENTRY_GOALS,
        default=st.session_state.form_data.get("entryGoals", []),
        help="Select all that apply. Note: 'Hire employees' triggers specialized employment law research."
    )
    
    # Primary Jurisdiction
    st.subheader("Target Jurisdiction")
    primary_jurisdiction = st.selectbox(
        "Primary Jurisdiction",
        options=["", "Netherlands"],
        index=0 if not st.session_state.form_data.get("primaryJurisdiction") else 1,
        help="V1 currently supports Netherlands. Additional countries coming in V2."
    )
    
    if primary_jurisdiction != "Netherlands":
        st.info("ℹ️ V1 focuses on Netherlands market entry. Other jurisdictions will be available in future versions.")
    
    # Save to session state
    st.session_state.form_data["entryGoals"] = entry_goals
    st.session_state.form_data["primaryJurisdiction"] = primary_jurisdiction or "Netherlands"

def step_3_tax_transactions():
    """Step 3: Tax & Transactions"""
    st.header("💰 Tax & Transactions")
    st.markdown("Tell us about your tax concerns and transaction types")
    
    # Tax Queries
    tax_queries = st.multiselect(
        "Tax Queries",
        options=TAX_QUERIES,
        default=st.session_state.form_data.get("taxQueries", []),
        help="Select all relevant tax queries. Note: 'Participation exemption' triggers holding company research."
    )
    
    # Custom tax query
    custom_tax_query = st.text_input(
        "Custom Tax Query (optional)",
        value="",
        help="Add a custom tax query if needed"
    )
    
    if custom_tax_query:
        tax_queries.append(f"Custom: {custom_tax_query}")
    
    # Transaction Types
    transaction_types = st.multiselect(
        "Transaction Types",
        options=TRANSACTION_TYPES,
        default=st.session_state.form_data.get("transactionTypes", []),
        help="Select transaction types relevant to your business"
    )
    
    # Specific Concerns
    specific_concerns = st.text_area(
        "Specific Concerns or Questions",
        value=st.session_state.form_data.get("specificConcerns", ""),
        help="Any specific tax concerns, questions, or additional context?",
        height=150,
        placeholder="e.g., We want to understand R&D tax credits and minimize our tax burden while maintaining full compliance."
    )
    
    # Save to session state
    st.session_state.form_data["taxQueries"] = tax_queries
    st.session_state.form_data["transactionTypes"] = transaction_types
    st.session_state.form_data["specificConcerns"] = specific_concerns

def step_4_legal_topics():
    """Step 4: Legal Topics"""
    st.header("⚖️ Legal Topics")
    st.markdown("Select legal topics relevant to your business")
    
    selected_topics = st.multiselect(
        "Legal Topics",
        options=list(LEGAL_TOPICS.keys()),
        format_func=lambda x: LEGAL_TOPICS[x],
        default=st.session_state.form_data.get("selectedLegalTopics", []),
        help="Select all relevant legal topics. Topic-specific questions will be available in V2."
    )
    
    if selected_topics:
        st.info(f"✅ Selected {len(selected_topics)} legal topic(s). These will be included in your memo analysis.")
    
    # Save to session state
    st.session_state.form_data["selectedLegalTopics"] = selected_topics

def step_5_review_and_generate():
    """Step 5: Review & Generate"""
    st.header("📋 Review & Generate")
    st.markdown("Review your inputs and generate your tax memo")
    
    # Memo name
    memo_name = st.text_input(
        "Memo Name (optional)",
        value=st.session_state.form_data.get("memoName", ""),
        help="Give your memo a name for easy reference",
        placeholder="e.g., Netherlands Market Entry Strategy"
    )
    st.session_state.form_data["memoName"] = memo_name
    
    # Validation
    if not st.session_state.form_data.get("businessName"):
        st.error("❌ Company Name is required. Please go back to Step 1.")
        return
    
    # Show summary
    st.subheader("📝 Input Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Company Information**")
        st.write(f"- **Name:** {st.session_state.form_data.get('businessName', 'N/A')}")
        st.write(f"- **Industry:** {st.session_state.form_data.get('industry', 'Not specified')}")
        st.write(f"- **Size:** {st.session_state.form_data.get('companySize', 'Not specified')}")
        st.write(f"- **Type:** {st.session_state.form_data.get('companyType', 'Not specified')}")
        st.write(f"- **Timeline:** {st.session_state.form_data.get('timeline', 'Not specified')}")
        
        if st.session_state.form_data.get('currentRevenue'):
            st.write(f"- **Current Revenue:** €{st.session_state.form_data.get('currentRevenue'):,.0f}")
        if st.session_state.form_data.get('projectedRevenue'):
            st.write(f"- **Projected Revenue:** €{st.session_state.form_data.get('projectedRevenue'):,.0f}")
    
    with col2:
        st.markdown("**Goals & Jurisdiction**")
        entry_goals = st.session_state.form_data.get('entryGoals', [])
        if entry_goals:
            for goal in entry_goals:
                st.write(f"- {goal}")
        else:
            st.write("- No goals specified")
        st.write(f"- **Jurisdiction:** {st.session_state.form_data.get('primaryJurisdiction', 'Not specified')}")
        
        st.markdown("**Tax & Transactions**")
        tax_queries = st.session_state.form_data.get('taxQueries', [])
        if tax_queries:
            st.write(f"- {len(tax_queries)} tax query/queries selected")
        transaction_types = st.session_state.form_data.get('transactionTypes', [])
        if transaction_types:
            st.write(f"- {len(transaction_types)} transaction type(s) selected")
        
        legal_topics = st.session_state.form_data.get('selectedLegalTopics', [])
        if legal_topics:
            st.write(f"- {len(legal_topics)} legal topic(s) selected")
    
    # Special features indicator
    st.markdown("---")
    st.markdown("### ✨ Special Features Activated")
    
    special_features = []
    if st.session_state.form_data.get('industry') == "Software & Technology":
        special_features.append("🔬 **WBSO & Innovation Box Research** - Automatic research for R&D tax credits")
    if "Hire employees" in st.session_state.form_data.get('entryGoals', []):
        special_features.append("👥 **Employment Law Research** - Automatic research for payroll tax and employment contracts")
    if st.session_state.form_data.get('companyType') == "Holding Company" or any("participation exemption" in str(q).lower() for q in st.session_state.form_data.get('taxQueries', [])):
        special_features.append("🏢 **Holding Company Path** - Specialized research for participation exemption and BV structure")
    
    if special_features:
        for feature in special_features:
            st.success(feature)
    else:
        st.info("ℹ️ Standard research path will be used. Select 'Software & Technology' industry or 'Hire employees' goal to activate specialized research.")
    
    # Generate button
    st.markdown("---")
    if st.button("🚀 Generate Memo", type="primary", use_container_width=True):
        generate_memo()

def map_frontend_to_backend(frontend_data: Dict[str, Any]) -> Dict[str, Any]:
    """Map frontend field names to backend field names"""
    backend_data = {}
    
    # Required field
    if frontend_data.get("businessName"):
        backend_data["companyName"] = frontend_data["businessName"]
    
    # Direct mappings
    if frontend_data.get("entryGoals"):
        backend_data["entryGoals"] = frontend_data["entryGoals"]
    
    if frontend_data.get("primaryJurisdiction"):
        backend_data["primaryJurisdiction"] = frontend_data["primaryJurisdiction"]
    
    if frontend_data.get("taxQueries"):
        backend_data["taxConsiderations"] = frontend_data["taxQueries"]
    
    if frontend_data.get("selectedLegalTopics"):
        backend_data["selectedLegalTopics"] = frontend_data["selectedLegalTopics"]
    
    # Handle companySize -> employeeCount conversion
    if frontend_data.get("companySize"):
        size_map = {
            "Startup (1-10 employees)": 5,
            "Small (11-50 employees)": 25,
            "Medium (51-250 employees)": 100,
            "Large (251+ employees)": 500
        }
        if frontend_data["companySize"] in size_map:
            backend_data["employeeCount"] = size_map[frontend_data["companySize"]]
    
    # Handle industry
    if frontend_data.get("industry"):
        backend_data["industry"] = frontend_data["industry"]
    
    # Handle companyType
    if frontend_data.get("companyType"):
        backend_data["companyType"] = frontend_data["companyType"]
    
    # Handle additional context - combine multiple sources
    additional_context_parts = []
    
    if frontend_data.get("specificConcerns"):
        additional_context_parts.append(frontend_data["specificConcerns"])
    
    # Add transaction types to context if provided
    if frontend_data.get("transactionTypes"):
        transaction_str = f"Transaction types: {', '.join(frontend_data['transactionTypes'])}"
        additional_context_parts.append(transaction_str)
    
    if additional_context_parts:
        backend_data["additionalContext"] = ". ".join(additional_context_parts)
    
    # Handle timeline
    if frontend_data.get("timeline"):
        backend_data["timelinePreference"] = frontend_data["timeline"]
    
    # Handle revenue
    if frontend_data.get("currentRevenue"):
        backend_data["currentRevenue"] = frontend_data["currentRevenue"]
    if frontend_data.get("projectedRevenue"):
        backend_data["projectedRevenue"] = frontend_data["projectedRevenue"]
    
    return backend_data

def generate_memo():
    """Generate memo by calling backend API"""
    # Map frontend data to backend format
    backend_request = map_frontend_to_backend(st.session_state.form_data)
    
    # Show request being sent
    with st.spinner("🔄 Generating your memo... This may take 30-60 seconds."):
        try:
            response = requests.post(
                f"{API_URL}/generate-memo",
                json=backend_request,
                timeout=180
            )
            
            if response.status_code == 200:
                memo = response.json()
                st.session_state.memo_result = memo
                st.success("✅ Memo generated successfully!")
                st.rerun()
            else:
                st.error(f"❌ Error: {response.status_code}")
                try:
                    error_detail = response.json()
                    st.json(error_detail)
                except:
                    st.write(response.text)
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Could not connect to API at {API_URL}")
            st.info("💡 Make sure your backend server is running!")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The memo generation is taking longer than expected.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def display_memo():
    """Display the generated memo in a clear, readable format"""
    if "memo_result" not in st.session_state:
        return
    
    memo = st.session_state.memo_result
    
    st.header("📄 Your Generated Tax Memo")
    st.markdown("---")
    
    # Executive Summary
    if memo.get("executiveSummary"):
        st.subheader("📊 Executive Summary")
        exec_sum = memo["executiveSummary"]
        
        if exec_sum.get("overview"):
            st.write(exec_sum["overview"])
        
        if exec_sum.get("keyRecommendations"):
            st.markdown("**✅ Key Recommendations:**")
            for rec in exec_sum["keyRecommendations"]:
                st.markdown(f"• {rec}")
        
        if exec_sum.get("criticalConsiderations"):
            st.markdown("**⚠️ Critical Considerations:**")
            for cons in exec_sum["criticalConsiderations"]:
                st.markdown(f"• {cons}")
        
        st.markdown("---")
    
    # Tax Considerations
    if memo.get("taxConsiderations"):
        st.subheader("💰 Tax Considerations")
        tax = memo["taxConsiderations"]
        
        if tax.get("corporateTaxRate"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Corporate Tax Rate", tax["corporateTaxRate"])
        
        if tax.get("taxObligations"):
            st.markdown("**📋 Tax Obligations:**")
            for obl in tax["taxObligations"]:
                st.markdown(f"• {obl}")
        
        if tax.get("taxOptimizationStrategies"):
            st.markdown("**💡 Tax Optimization Strategies:**")
            for strat in tax["taxOptimizationStrategies"]:
                st.markdown(f"• {strat}")
        
        if tax.get("specialRegimes"):
            st.markdown("**🎯 Special Tax Regimes:**")
            for regime in tax["specialRegimes"]:
                st.markdown(f"• {regime}")
        
        st.markdown("---")
    
    # Market Entry Options
    if memo.get("marketEntryOptions"):
        st.subheader("🚪 Market Entry Options")
        entry = memo["marketEntryOptions"]
        
        if entry.get("recommendedOption"):
            st.success(f"**Recommended:** {entry['recommendedOption']}")
        
        if entry.get("optionComparison"):
            st.markdown("**Options Comparison:**")
            for i, opt in enumerate(entry["optionComparison"], 1):
                with st.expander(f"Option {i}: {opt.get('option', 'Option')}", expanded=(i == 1)):
                    st.write(opt.get("description", ""))
        
        if entry.get("prosAndCons"):
            st.markdown("**Pros & Cons:**")
            for option_key, items in entry["prosAndCons"].items():
                st.markdown(f"**{option_key}:**")
                for item in items:
                    st.markdown(f"  • {item}")
        
        st.markdown("---")
    
    # Implementation Timeline
    if memo.get("implementationTimeline"):
        st.subheader("📅 Implementation Timeline")
        timeline = memo["implementationTimeline"]
        
        if timeline.get("estimatedDuration"):
            st.metric("Estimated Duration", timeline["estimatedDuration"])
        
        if timeline.get("phases"):
            st.markdown("**Phases:**")
            for i, phase in enumerate(timeline["phases"], 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Phase {i}: {phase.get('phase', 'Phase')}**")
                    if phase.get("description"):
                        st.write(phase["description"])
                    elif phase.get("details"):
                        st.write(phase["details"])
                with col2:
                    st.markdown(f"**Duration:** {phase.get('duration', 'N/A')}")
        
        if timeline.get("milestones"):
            st.markdown("**🎯 Key Milestones:**")
            for milestone in timeline["milestones"]:
                st.markdown(f"• {milestone}")
        
        st.markdown("---")
    
    # Business Structure
    if memo.get("businessStructure"):
        st.subheader("🏢 Business Structure")
        struct = memo["businessStructure"]
        if struct.get("recommendedStructure"):
            st.write(f"**Recommended Structure:** {struct['recommendedStructure']}")
        if struct.get("structureRationale"):
            st.write(f"**Rationale:** {struct['structureRationale']}")
        st.markdown("---")
    
    # Legal Deep Dive
    if memo.get("legalDeepDive"):
        st.subheader("⚖️ Legal Deep Dive")
        legal = memo["legalDeepDive"]
        if legal.get("detailedAnalysis"):
            st.write(legal["detailedAnalysis"])
        st.markdown("---")
    
    # Download and Full JSON
    col1, col2 = st.columns(2)
    with col1:
        json_str = json.dumps(memo, indent=2)
        st.download_button(
            label="📥 Download Memo (JSON)",
            data=json_str,
            file_name=f"tax_memo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    with col2:
        with st.expander("🔍 View Full JSON Response"):
            st.json(memo)

def main():
    """Main application"""
    st.title("📋 Tax Memo Generator")
    st.markdown("### Version 1.0 - Netherlands Market Entry")
    st.markdown("*Generate comprehensive tax and legal memos for market entry*")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Step navigation
    for step_num in range(1, TOTAL_STEPS + 1):
        step_name = STEP_NAMES[step_num]
        if st.sidebar.button(f"Step {step_num}: {step_name}", key=f"nav_{step_num}", use_container_width=True):
            st.session_state.current_step = step_num
            st.rerun()
    
    st.sidebar.divider()
    
    # Progress indicator
    progress = st.session_state.current_step / TOTAL_STEPS
    st.sidebar.progress(progress)
    st.sidebar.caption(f"Step {st.session_state.current_step} of {TOTAL_STEPS}")
    
    # Main content area
    if st.session_state.current_step == 1:
        step_1_company_info()
    elif st.session_state.current_step == 2:
        step_2_goals_jurisdiction()
    elif st.session_state.current_step == 3:
        step_3_tax_transactions()
    elif st.session_state.current_step == 4:
        step_4_legal_topics()
    elif st.session_state.current_step == 5:
        step_5_review_and_generate()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.session_state.current_step > 1:
            if st.button("◀ Previous", use_container_width=True):
                st.session_state.current_step -= 1
                st.rerun()
    
    with col2:
        if st.session_state.current_step < TOTAL_STEPS:
            if st.button("Next ▶", use_container_width=True, type="primary"):
                st.session_state.current_step += 1
                st.rerun()
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.form_data = {}
            st.session_state.current_step = 1
            if "memo_result" in st.session_state:
                del st.session_state.memo_result
            st.rerun()
    
    # Display memo if generated
    if "memo_result" in st.session_state:
        st.divider()
        display_memo()

if __name__ == "__main__":
    main()
