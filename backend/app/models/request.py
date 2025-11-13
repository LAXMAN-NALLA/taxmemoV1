"""Pydantic models for input JSON request."""
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


def to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase for frontend compatibility."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


class TaxMemoRequest(BaseModel):
    """Input model for tax memo generation request (23 fields)."""
    
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    
    # Company Information (5 fields)
    company_name: str = Field(..., description="Name of the company")
    industry: Optional[str] = Field(None, description="Industry sector (e.g., 'Software & Technology')")
    company_type: Optional[str] = Field(None, description="Type of company (e.g., 'LLC', 'Corporation')")
    founding_year: Optional[int] = Field(None, description="Year the company was founded")
    headquarters_location: Optional[str] = Field(None, description="Current headquarters location")
    
    # Jurisdiction & Entry (4 fields)
    primary_jurisdiction: Optional[str] = Field(None, description="Primary jurisdiction (defaults to Netherlands)")
    target_markets: Optional[List[str]] = Field(default_factory=list, description="Target markets for expansion")
    entry_goals: Optional[List[str]] = Field(default_factory=list, description="List of entry goals")
    selected_legal_topics: Optional[List[str]] = Field(default_factory=list, description="Selected legal topics (e.g., ['employment-law'])")
    
    # Financial Information (4 fields)
    current_revenue: Optional[float] = Field(None, description="Current annual revenue")
    projected_revenue: Optional[float] = Field(None, description="Projected revenue in target market")
    budget_range: Optional[str] = Field(None, description="Budget range for market entry")
    funding_status: Optional[str] = Field(None, description="Funding status (e.g., 'Bootstrapped', 'VC-backed')")
    
    # Operational Information (4 fields)
    employee_count: Optional[int] = Field(None, description="Current number of employees")
    planned_employees: Optional[int] = Field(None, description="Planned number of employees in target market")
    current_operations: Optional[List[str]] = Field(default_factory=list, description="Current operations/activities")
    key_products_services: Optional[List[str]] = Field(default_factory=list, description="Key products or services")
    
    # Timeline & Planning (3 fields)
    timeline_preference: Optional[str] = Field(None, description="Preferred timeline (e.g., '3 months', '6 months')")
    urgency_level: Optional[str] = Field(None, description="Urgency level (e.g., 'High', 'Medium', 'Low')")
    preferred_structure: Optional[str] = Field(None, description="Preferred business structure (e.g., 'BV', 'Branch')")
    
    # Additional Context (3 fields)
    tax_considerations: Optional[List[str]] = Field(default_factory=list, description="Specific tax considerations")
    compliance_priorities: Optional[List[str]] = Field(default_factory=list, description="Compliance priorities")
    additional_context: Optional[str] = Field(None, description="Any additional context or requirements")

