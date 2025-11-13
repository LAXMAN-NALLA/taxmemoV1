"""FastAPI entrypoint for Tax Memo Orchestrator."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.request import TaxMemoRequest
from app.models.response import (
    MemoResponse,
    ExecutiveSummary,
    BusinessProfileSection,
    JurisdictionsSection,
    StructureSection,
    TaxSection,
    LegalOverviewSection,
    LegalDeepDiveSection,
    EntryOptionsSection,
    TimelineSection,
    BudgetSection,
    RiskSection,
    ActionPlanSection,
    AppendixSection
)
from app.core.orchestrator import Orchestrator
from app.services.rag_engine import RAGEngine
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Tax Memo Orchestrator API",
    description="Generate comprehensive market entry memos using RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
orchestrator = Orchestrator()
rag_engine = RAGEngine()


def map_sections_to_response(sections: Dict[str, Any], request: TaxMemoRequest) -> MemoResponse:
    """
    Map generated sections to the MemoResponse model.
    
    This function takes the raw generated sections and maps them to the
    structured response model. For V1, we do basic mapping.
    """
    response = MemoResponse()
    
    # Helper function to unwrap nested section structures
    def unwrap_section(section_name: str, data: Any) -> Any:
        """Unwrap nested structures where section name appears as a key."""
        if isinstance(data, dict):
            # If the section name is a key in the dict, unwrap it
            if section_name in data:
                return data[section_name]
            # If there's only one key and it's similar to section name, unwrap it
            if len(data) == 1:
                key = list(data.keys())[0]
                if section_name.replace("_", "") in key.replace("_", "") or key.replace("_", "") in section_name.replace("_", ""):
                    return data[key]
        return data
    
    # Map executive_summary
    if "executive_summary" in sections:
        exec_data = unwrap_section("executive_summary", sections["executive_summary"])
        if isinstance(exec_data, dict):
            # Try multiple possible key names
            overview = (exec_data.get("overview") or 
                      exec_data.get("content") or 
                      exec_data.get("summary") or
                      exec_data.get("executive_summary") or
                      str(exec_data) if len(exec_data) == 1 else None)
            
            key_recommendations = (exec_data.get("key_recommendations") or 
                                  exec_data.get("recommendations") or
                                  exec_data.get("key_recommendations", []))
            if not isinstance(key_recommendations, list):
                key_recommendations = []
            
            critical_considerations = (exec_data.get("critical_considerations") or
                                      exec_data.get("considerations") or
                                      exec_data.get("critical_considerations", []))
            if not isinstance(critical_considerations, list):
                critical_considerations = []
            
            response.executive_summary = ExecutiveSummary(
                overview=overview,
                key_recommendations=key_recommendations,
                critical_considerations=critical_considerations
            )
    
    # Map market_entry_options
    if "market_entry_options" in sections:
        entry_data = unwrap_section("market_entry_options", sections["market_entry_options"])
        if isinstance(entry_data, dict):
            # Handle nested structure (e.g., {"market_entry_options": [...]})
            if "market_entry_options" in entry_data and isinstance(entry_data["market_entry_options"], list):
                options_list = entry_data["market_entry_options"]
                recommended_option = options_list[0].get("option") if options_list else None
                option_comparison = options_list
            else:
                recommended_option = (entry_data.get("recommended_option") or 
                                    entry_data.get("content") or
                                    entry_data.get("recommended"))
                option_comparison = entry_data.get("option_comparison") or entry_data.get("options") or []
                if not isinstance(option_comparison, list):
                    option_comparison = []
            
            pros_and_cons_raw = entry_data.get("pros_and_cons") or entry_data.get("prosAndCons") or {}
            pros_and_cons = {}
            
            # Transform nested structure {option: {pros: [], cons: []}} to {option: [combined list]}
            if isinstance(pros_and_cons_raw, dict):
                for key, value in pros_and_cons_raw.items():
                    if isinstance(value, dict):
                        # Handle nested structure: combine pros and cons into a single list
                        pros = value.get("pros", []) if isinstance(value.get("pros"), list) else []
                        cons = value.get("cons", []) if isinstance(value.get("cons"), list) else []
                        # Ensure all items are strings
                        pros = [str(item) for item in pros if item]
                        cons = [str(item) for item in cons if item]
                        # Combine pros and cons, prefixing cons with "Cons: "
                        combined = pros + [f"Cons: {item}" for item in cons]
                        pros_and_cons[key] = combined
                    elif isinstance(value, list):
                        # Already in the correct format - ensure all items are strings
                        pros_and_cons[key] = [str(item) for item in value if item]
                    else:
                        # Convert to list if it's a string or other type
                        pros_and_cons[key] = [str(value)] if value else []
            
            response.market_entry_options = EntryOptionsSection(
                recommended_option=recommended_option,
                option_comparison=option_comparison,
                pros_and_cons=pros_and_cons
            )
    
    # Map implementation_timeline
    if "implementation_timeline" in sections:
        timeline_data = unwrap_section("implementation_timeline", sections["implementation_timeline"])
        if isinstance(timeline_data, dict):
            phases = timeline_data.get("phases") or timeline_data.get("phase") or []
            if not isinstance(phases, list):
                phases = []
            
            estimated_duration = (timeline_data.get("estimated_duration") or 
                                timeline_data.get("estimatedDuration") or
                                timeline_data.get("duration") or
                                timeline_data.get("content"))
            
            milestones = timeline_data.get("milestones") or timeline_data.get("milestone") or []
            if not isinstance(milestones, list):
                milestones = []
            
            response.implementation_timeline = TimelineSection(
                phases=phases,
                estimated_duration=estimated_duration,
                milestones=milestones
            )
    
    # Map business_structure
    if "business_structure" in sections:
        structure_data = sections["business_structure"]
        if isinstance(structure_data, dict):
            response.business_structure = StructureSection(
                recommended_structure=structure_data.get("recommended_structure") or structure_data.get("content"),
                structure_alternatives=structure_data.get("structure_alternatives", []),
                structure_rationale=structure_data.get("structure_rationale")
            )
    
    # Map tax_considerations
    if "tax_considerations" in sections:
        tax_data = unwrap_section("tax_considerations", sections["tax_considerations"])
        if isinstance(tax_data, dict):
            corporate_tax_rate = (tax_data.get("corporate_tax_rate") or 
                                 tax_data.get("corporateTaxRate") or
                                 tax_data.get("tax_rate"))
            
            tax_obligations = tax_data.get("tax_obligations") or tax_data.get("taxObligations") or []
            if not isinstance(tax_obligations, list):
                tax_obligations = []
            
            tax_optimization_strategies = (tax_data.get("tax_optimization_strategies") or 
                                         tax_data.get("taxOptimizationStrategies") or
                                         tax_data.get("optimization_strategies") or
                                         tax_data.get("strategies") or [])
            if not isinstance(tax_optimization_strategies, list):
                tax_optimization_strategies = []
            
            special_regimes = (tax_data.get("special_regimes") or 
                             tax_data.get("specialRegimes") or
                             tax_data.get("regimes") or [])
            if not isinstance(special_regimes, list):
                special_regimes = []
            
            response.tax_considerations = TaxSection(
                corporate_tax_rate=corporate_tax_rate,
                tax_obligations=tax_obligations,
                tax_optimization_strategies=tax_optimization_strategies,
                special_regimes=special_regimes
            )
    
    # Map legal_topics_overview
    if "legal_topics_overview" in sections:
        legal_data = sections["legal_topics_overview"]
        if isinstance(legal_data, dict):
            response.legal_topics_overview = LegalOverviewSection(
                key_legal_areas=legal_data.get("key_legal_areas", []),
                regulatory_requirements=legal_data.get("regulatory_requirements", []),
                compliance_overview=legal_data.get("compliance_overview") or legal_data.get("content")
            )
    
    # Map legal_deep_dive
    if "legal_deep_dive" in sections:
        deep_dive_data = sections["legal_deep_dive"]
        if isinstance(deep_dive_data, dict):
            response.legal_deep_dive = LegalDeepDiveSection(
                detailed_analysis=deep_dive_data.get("detailed_analysis") or deep_dive_data.get("content"),
                specific_regulations=deep_dive_data.get("specific_regulations", {}),
                case_studies=deep_dive_data.get("case_studies", [])
            )
    
    # Map business_profile
    if "business_profile" in sections:
        profile_data = sections["business_profile"]
        if isinstance(profile_data, dict):
            response.business_profile = BusinessProfileSection(
                company_description=profile_data.get("company_description") or profile_data.get("content"),
                industry_analysis=profile_data.get("industry_analysis"),
                market_position=profile_data.get("market_position")
            )
    
    # Map jurisdictions_treaties
    if "jurisdictions_treaties" in sections:
        jurisdictions_data = sections["jurisdictions_treaties"]
        if isinstance(jurisdictions_data, dict):
            response.jurisdictions_treaties = JurisdictionsSection(
                primary_jurisdiction=jurisdictions_data.get("primary_jurisdiction"),
                relevant_treaties=jurisdictions_data.get("relevant_treaties", []),
                treaty_benefits=jurisdictions_data.get("treaty_benefits") or jurisdictions_data.get("content")
            )
    
    # Map resource_budget
    if "resource_budget" in sections:
        budget_data = sections["resource_budget"]
        if isinstance(budget_data, dict):
            response.resource_budget = BudgetSection(
                estimated_costs=budget_data.get("estimated_costs", {}),
                cost_breakdown=budget_data.get("cost_breakdown", []),
                budget_recommendations=budget_data.get("budget_recommendations") or budget_data.get("content")
            )
    
    # Map risk_assessment
    if "risk_assessment" in sections:
        risk_data = sections["risk_assessment"]
        if isinstance(risk_data, dict):
            response.risk_assessment = RiskSection(
                identified_risks=risk_data.get("identified_risks", []),
                risk_mitigation=risk_data.get("risk_mitigation", []),
                risk_level=risk_data.get("risk_level")
            )
    
    # Map next_steps
    if "next_steps" in sections:
        steps_data = sections["next_steps"]
        if isinstance(steps_data, dict):
            response.next_steps = ActionPlanSection(
                immediate_actions=steps_data.get("immediate_actions", []),
                short_term_steps=steps_data.get("short_term_steps", []),
                long_term_considerations=steps_data.get("long_term_considerations", [])
            )
    
    # Map appendix
    if "appendix" in sections:
        appendix_data = sections["appendix"]
        if isinstance(appendix_data, dict):
            response.appendix = AppendixSection(
                references=appendix_data.get("references", []),
                additional_resources=appendix_data.get("additional_resources", []),
                glossary=appendix_data.get("glossary", {}),
                data_sources=appendix_data.get("data_sources", [])
            )
    
    return response


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Tax Memo Orchestrator API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/generate-memo", response_model=MemoResponse)
async def generate_memo(request: TaxMemoRequest) -> MemoResponse:
    """
    Generate a comprehensive market entry memo.
    
    This endpoint:
    1. Accepts a TaxMemoRequest with company details
    2. Orchestrates research tasks based on input
    3. Queries Qdrant vector DB for relevant information
    4. Generates a 13-section memo using OpenAI GPT-4
    
    Args:
        request: TaxMemoRequest with company and entry details
    
    Returns:
        MemoResponse with 13 sections of market entry analysis
    """
    try:
        logger.info(f"Generating memo for company: {request.company_name}")
        
        # Step 1: Plan research tasks
        tasks = orchestrator.plan_tasks(request)
        logger.info(f"Planned {len(tasks)} research tasks")
        
        # Step 2: Prepare user context
        user_context = {
            "company_name": request.company_name,
            "industry": request.industry,
            "company_type": request.company_type,
            "entry_goals": request.entry_goals or [],
            "selected_legal_topics": request.selected_legal_topics or [],
            "current_revenue": request.current_revenue,
            "projected_revenue": request.projected_revenue,
            "employee_count": request.employee_count,
            "planned_employees": request.planned_employees,
            "timeline_preference": request.timeline_preference,
            "budget_range": request.budget_range,
            "preferred_structure": request.preferred_structure,
            "key_products_services": request.key_products_services or []
        }
        
        # Step 3: Generate all sections using RAG
        logger.info(f"Starting RAG generation for {len(tasks)} tasks...")
        sections = rag_engine.generate_memo_sections(tasks, user_context)
        logger.info(f"Generated {len(sections)} sections")
        logger.info(f"Section keys: {list(sections.keys())}")
        
        # Debug: Log section structures with full content
        for key, value in sections.items():
            if isinstance(value, dict):
                logger.info(f"Section '{key}': keys={list(value.keys())}")
                logger.info(f"Section '{key}' content preview: {str(value)[:500]}")
            else:
                logger.info(f"Section '{key}': type={type(value).__name__}, value={str(value)[:200]}")
        
        # Step 4: Map to response model
        logger.info("Mapping sections to response model...")
        response = map_sections_to_response(sections, request)
        logger.info("Response mapping complete")
        
        return response
    
    except Exception as e:
        logger.error(f"Error generating memo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate memo: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

