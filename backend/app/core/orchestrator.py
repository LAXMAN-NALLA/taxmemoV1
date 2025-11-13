"""Orchestrator that plans research tasks based on input."""
from typing import List, Dict, Any, Optional
from app.models.request import TaxMemoRequest


class TaskPlan:
    """Represents a planned research task."""
    def __init__(self, task_name: str, search_query: str, section_name: str, priority: int = 1):
        self.task_name = task_name
        self.search_query = search_query
        self.section_name = section_name
        self.priority = priority
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_name": self.task_name,
            "search_query": self.search_query,
            "section_name": self.section_name,
            "priority": self.priority
        }


class Orchestrator:
    """
    Master Orchestrator that enforces strict logic paths to prevent 
    hallucinations and context conflicts.
    
    Key Features:
    - Prevents "B.V." name trap: Forces BV if name contains "B.V."
    - Prevents "Holding" conflict: Strict isolation for holding companies
    - Prevents "Notary" hallucination: Explicit "no notary" in Branch queries
    - Prevents "Ghost" tax credits: Only searches Innovation Box/WBSO for Tech
    """
    
    # V1: Hardcode to Netherlands
    DEFAULT_JURISDICTION = "Netherlands"
    
    def __init__(self):
        self.jurisdiction = self.DEFAULT_JURISDICTION
    
    def plan_tasks(self, request: TaxMemoRequest) -> List[TaskPlan]:
        """
        Generate a list of research tasks based on the input.
        
        Uses strict mutually exclusive paths to prevent context bleed-over:
        - PATH 1: Holding Company (strict isolation, no R&D/Branch)
        - PATH 2: Operating Company with sub-paths:
          - 2A: Force BV (if name contains "B.V." or explicit BV request)
          - 2B: Speed/Branch (only if NOT forced to BV)
          - 2C: Default comparison
        """
        tasks: List[TaskPlan] = []
        
        # 1. ANALYZE & CLASSIFY THE INPUT
        # ---------------------------------------------------------
        company_name = (request.company_name or "").lower()
        industry = (request.industry or "").lower()
        company_type = (request.company_type or "").lower()
        goals = [g.lower() for g in (request.entry_goals or [])]
        tax_considerations = [str(tc).lower() for tc in (request.tax_considerations or [])]
        timeline = (request.timeline_preference or "").lower()
        additional_context = (request.additional_context or "").lower()
        
        # Combine all tax-related text for detection
        all_tax_text = " ".join(tax_considerations) + " " + additional_context
        
        # A. Detect Holding Company Intent
        # Triggers: Explicit type, specific tax goals (participation exemption), or "holding" in name
        # CRITICAL: Must be checked BEFORE must_be_bv to ensure proper isolation
        is_holding = (
            (company_type and "holding" in company_type) or 
            (company_name and "holding" in company_name) or
            "participation exemption" in all_tax_text or
            "deelnemingsvrijstelling" in all_tax_text or
            ("dividend" in all_tax_text and "holding" in all_tax_text)
        )
        
        # B. Detect "Must be B.V." Constraint
        # CRITICAL: Only force BV for EXPLICIT Dutch entity intent, not generic foreign terms
        # Triggers: User explicitly named it "B.V." or explicitly selected Dutch entity type, or it is a Holding
        must_be_bv = (
            # Only force BV if they explicitly name the DUTCH entity "B.V."
            "b.v" in company_name or 
            "bv" in company_name or 
            "b.v." in company_name or
            company_name.endswith(".bv") or
            company_name.endswith(".b.v") or
            company_name.endswith(".b.v.") or
            # Or if they explicitly ask for the specific Dutch entity type
            "besloten vennootschap" in company_type or
            # Or if it is a Holding (which usually needs BV for treaties)
            is_holding  # Holding companies almost always require a BV structure for tax treaties
        )
        # NOTE: "LLC", "Corporation", "Limited Liability" are REMOVED
        # These are foreign terms and don't necessarily mean the user wants a Dutch BV.
        # If user wants speed, they should get Branch Office, not forced BV.
        
        # C. Detect Tech/R&D Intent
        # Triggers: Software, Technology, BioTech, Engineering, etc.
        # CRITICAL: Must NOT be Financial Services (to prevent ghost R&D credits)
        is_tech = (
            ("software" in industry or "technology" in industry) and
            "financial services" not in industry
        ) or (
            "biotech" in industry or 
            "engineering" in industry or
            "r&d" in " ".join(goals) or
            "research" in " ".join(goals)
        )
        
        # D. Detect Speed Preference
        prioritizes_speed = (
            "short" in timeline or 
            "fast" in timeline or 
            "urgent" in timeline or
            "asap" in timeline or
            "1 month" in timeline
        )
        
        # 2. BUILD THE TASK PLAN (MUTUALLY EXCLUSIVE PATHS)
        # ---------------------------------------------------------
        
        # DEBUG: Log detection results (remove in production)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Orchestrator Detection - is_holding: {is_holding}, must_be_bv: {must_be_bv}, is_tech: {is_tech}, prioritizes_speed: {prioritizes_speed}")
        
        # --- PATH 1: THE HOLDING COMPANY (Strict Isolation) ---
        # CRITICAL: This path must RETURN EARLY to prevent any fall-through
        if is_holding:
            # Executive Summary for Holding
            tasks.append(TaskPlan(
                task_name="Holding Company Executive Summary",
                search_query="Netherlands holding company benefits executive summary participation exemption dividend withholding 2025",
                section_name="executive_summary",
                priority=1
            ))
            
            # Critical Tax Benefit: Participation Exemption
            tasks.append(TaskPlan(
                task_name="Participation Exemption Deep Dive",
                search_query="Netherlands participation exemption deelnemingsvrijstelling requirements 5% ownership motive test dividends capital gains 2025",
                section_name="tax_considerations",
                priority=2
            ))
            
            # Entity Structure: FORCE B.V. (Ignore Branch)
            tasks.append(TaskPlan(
                task_name="Holding Structure (BV)",
                search_query="Netherlands BV incorporation requirements for holding company notary deed timeline 2025",
                section_name="business_structure",
                priority=3
            ))
            
            # Corporate Tax for Holdings
            tasks.append(TaskPlan(
                task_name="Corporate Tax for Holding Companies",
                search_query="Netherlands corporate income tax 2025 treaty network holding company tax benefits 2025",
                section_name="tax_considerations",
                priority=4
            ))
            
            # Compliance
            tasks.append(TaskPlan(
                task_name="Holding Company Compliance",
                search_query="Netherlands holding company substance requirements compliance filing obligations 2025",
                section_name="implementation_timeline",
                priority=5
            ))
            
            # CRITICAL: RETURN EARLY - Do not let holding companies fall through to operating company logic
            # This prevents Innovation Box, Branch Office, and other irrelevant tasks
            tasks.sort(key=lambda x: x.priority)
            return tasks
        
        # --- PATH 2: THE OPERATING COMPANY (Tech/General) ---
        # This path only runs if NOT a holding company
        else:
            # Sub-path 2A: FORCE B.V. (If name is B.V. or LLC)
            # CRITICAL: This check MUST happen BEFORE prioritizes_speed check
            # Name constraint (B.V.) wins over speed preference
            if must_be_bv:
                tasks.append(TaskPlan(
                    task_name="BV Executive Summary",
                    search_query="Netherlands BV private limited company benefits liability protection executive summary 2025",
                    section_name="executive_summary",
                    priority=1
                ))
                
                tasks.append(TaskPlan(
                    task_name="BV Incorporation Process",
                    search_query="Netherlands BV incorporation timeline notary requirements bank account opening KvK registration 2025",
                    section_name="business_structure",
                    priority=2
                ))
                
                tasks.append(TaskPlan(
                    task_name="BV Tax and Compliance",
                    search_query="Netherlands BV corporate income tax VAT registration obligations 2025",
                    section_name="tax_considerations",
                    priority=3
                ))
                
                tasks.append(TaskPlan(
                    task_name="BV Implementation Timeline",
                    search_query="Netherlands BV setup timeline notarization KvK registration bank account duration 2025",
                    section_name="implementation_timeline",
                    priority=4
                ))
            
            # Sub-path 2B: SPEED / BRANCH (Only if NOT forced to BV)
            elif prioritizes_speed:
                tasks.append(TaskPlan(
                    task_name="Branch Office Executive Summary",
                    search_query="Netherlands Branch Office market entry speed benefits vs BV quick setup 2025",
                    section_name="executive_summary",
                    priority=1
                ))
                
                # CRITICAL: Explicit "no notary" in query to prevent hallucination
                tasks.append(TaskPlan(
                    task_name="Branch Registration (No Notary)",
                    search_query="Netherlands Branch Office registration Chamber of Commerce KvK no notary required timeline fast setup 2025",
                    section_name="business_structure",
                    priority=2
                ))
                
                tasks.append(TaskPlan(
                    task_name="Branch Tax and Compliance",
                    search_query="Netherlands Branch Office tax obligations VAT registration corporate income tax 2025",
                    section_name="tax_considerations",
                    priority=3
                ))
                
                tasks.append(TaskPlan(
                    task_name="Branch Implementation Timeline",
                    search_query="Netherlands Branch Office setup timeline KvK registration no notary fast entry 2025",
                    section_name="implementation_timeline",
                    priority=4
                ))
            
            # Sub-path 2C: Default Comparison (If unclear)
            else:
                tasks.append(TaskPlan(
                    task_name="Market Entry Comparison",
                    search_query="Netherlands BV vs Branch Office comparison tax liability speed setup requirements 2025",
                    section_name="market_entry_options",
                    priority=1
                ))
                
                tasks.append(TaskPlan(
                    task_name="Executive Summary Research",
                    search_query="Netherlands market entry overview corporate tax business structure 2025",
                    section_name="executive_summary",
                    priority=2
                ))
                
                tasks.append(TaskPlan(
                    task_name="Tax Overview Research",
                    search_query="Netherlands corporate income tax rates VAT obligations tax overview 2025",
                    section_name="tax_considerations",
                    priority=3
                ))
                
                tasks.append(TaskPlan(
                    task_name="Implementation Timeline Research",
                    search_query="Netherlands company registration timeline BV branch office setup duration 2025",
                    section_name="implementation_timeline",
                    priority=4
                ))
            
            # --- OPERATING TAX INCENTIVES (Add-ons) ---
            # These only apply to operating companies (NOT holding companies)
            
            # 1. Tech Incentives (Only for Tech industries - NOT Financial Services)
            # CRITICAL: This prevents "Ghost R&D Credits" for Financial Services
            if is_tech:
                tasks.append(TaskPlan(
                    task_name="R&D Incentives (WBSO & Innovation Box)",
                    search_query="Netherlands WBSO R&D tax credit requirements and Innovation Box 9% rate conditions software technology 2025",
                    section_name="tax_considerations",
                    priority=5
                ))
            
            # 2. General Corporate Tax (For everyone in operating path)
            # Only add if not already added in sub-paths
            if not must_be_bv and not prioritizes_speed:
                tasks.append(TaskPlan(
                    task_name="General Corporate Tax",
                    search_query="Netherlands corporate income tax rate 2025 VAT registration payroll tax obligations 2025",
                    section_name="tax_considerations",
                    priority=5
                ))
            
            # 3. Staffing (If hiring)
            if "hire" in " ".join(goals) or "employees" in " ".join(goals):
                tasks.append(TaskPlan(
                    task_name="30% Ruling & Payroll",
                    search_query="Netherlands 30% ruling for foreign employees payroll tax requirements employment contracts 2025",
                    section_name="legal_deep_dive",
                    priority=6
                ))
        
        # Sort tasks by priority
        tasks.sort(key=lambda x: x.priority)
        
        return tasks
