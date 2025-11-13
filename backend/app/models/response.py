"""Pydantic models for the 13-section memo response."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


def to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase for frontend compatibility."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


# Base config for all response models
_base_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


# Section-specific models
class ExecutiveSummary(BaseModel):
    """Executive summary section."""
    model_config = _base_config
    overview: Optional[str] = None
    key_recommendations: Optional[List[str]] = None
    critical_considerations: Optional[List[str]] = None


class BusinessProfileSection(BaseModel):
    """Business profile section."""
    model_config = _base_config
    company_description: Optional[str] = None
    industry_analysis: Optional[str] = None
    market_position: Optional[str] = None


class JurisdictionsSection(BaseModel):
    """Jurisdictions and treaties section."""
    model_config = _base_config
    primary_jurisdiction: Optional[str] = None
    relevant_treaties: Optional[List[str]] = None
    treaty_benefits: Optional[str] = None


class StructureSection(BaseModel):
    """Business structure section."""
    model_config = _base_config
    recommended_structure: Optional[str] = None
    structure_alternatives: Optional[List[str]] = None
    structure_rationale: Optional[str] = None


class TaxSection(BaseModel):
    """Tax considerations section."""
    model_config = _base_config
    corporate_tax_rate: Optional[str] = None
    tax_obligations: Optional[List[str]] = None
    tax_optimization_strategies: Optional[List[str]] = None
    special_regimes: Optional[List[str]] = None


class LegalOverviewSection(BaseModel):
    """Legal topics overview section."""
    model_config = _base_config
    key_legal_areas: Optional[List[str]] = None
    regulatory_requirements: Optional[List[str]] = None
    compliance_overview: Optional[str] = None


class LegalDeepDiveSection(BaseModel):
    """Legal deep dive section."""
    model_config = _base_config
    detailed_analysis: Optional[str] = None
    specific_regulations: Optional[Dict[str, Any]] = None
    case_studies: Optional[List[str]] = None


class EntryOptionsSection(BaseModel):
    """Market entry options section."""
    model_config = _base_config
    recommended_option: Optional[str] = None
    option_comparison: Optional[List[Dict[str, Any]]] = None
    pros_and_cons: Optional[Dict[str, List[str]]] = None


class TimelineSection(BaseModel):
    """Implementation timeline section."""
    model_config = _base_config
    phases: Optional[List[Dict[str, Any]]] = None
    estimated_duration: Optional[str] = None
    milestones: Optional[List[str]] = None


class BudgetSection(BaseModel):
    """Resource and budget section."""
    model_config = _base_config
    estimated_costs: Optional[Dict[str, Any]] = None
    cost_breakdown: Optional[List[Dict[str, Any]]] = None
    budget_recommendations: Optional[str] = None


class RiskSection(BaseModel):
    """Risk assessment section."""
    model_config = _base_config
    identified_risks: Optional[List[Dict[str, Any]]] = None
    risk_mitigation: Optional[List[str]] = None
    risk_level: Optional[str] = None


class ActionPlanSection(BaseModel):
    """Next steps and action plan section."""
    model_config = _base_config
    immediate_actions: Optional[List[str]] = None
    short_term_steps: Optional[List[str]] = None
    long_term_considerations: Optional[List[str]] = None


class AppendixSection(BaseModel):
    """Appendix section."""
    model_config = _base_config
    references: Optional[List[str]] = None
    additional_resources: Optional[List[str]] = None
    glossary: Optional[Dict[str, str]] = None
    data_sources: Optional[List[str]] = None


class MemoResponse(BaseModel):
    """The complete 13-section memo response."""
    model_config = _base_config
    executive_summary: Optional[ExecutiveSummary] = None
    business_profile: Optional[BusinessProfileSection] = None
    jurisdictions_treaties: Optional[JurisdictionsSection] = None
    business_structure: Optional[StructureSection] = None
    tax_considerations: Optional[TaxSection] = None
    legal_topics_overview: Optional[LegalOverviewSection] = None
    legal_deep_dive: Optional[LegalDeepDiveSection] = None
    market_entry_options: Optional[EntryOptionsSection] = None
    implementation_timeline: Optional[TimelineSection] = None
    resource_budget: Optional[BudgetSection] = None
    risk_assessment: Optional[RiskSection] = None
    next_steps: Optional[ActionPlanSection] = None
    appendix: Optional[AppendixSection] = None

