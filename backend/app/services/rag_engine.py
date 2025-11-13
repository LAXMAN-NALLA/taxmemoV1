"""RAG Engine: Handles retrieval and LLM generation."""
from typing import Optional, Dict, Any
from openai import OpenAI
from app.core.config import settings
from app.services.qdrant import QdrantService
from app.utils.persona import MASTER_SYSTEM_PROMPT
import json
import re


class RAGEngine:
    """Retrieval-Augmented Generation engine."""
    
    def __init__(self):
        """Initialize RAG engine with OpenAI and Qdrant."""
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.qdrant_service = QdrantService()
        self.model = "gpt-4o"  # Preferred model for complex synthesis
    
    def _build_task_constraints(self, task_name: Optional[str], section_name: str, search_query: str) -> str:
        """
        Build task-specific constraints to prevent LLM from overriding task instructions.
        
        This enforces "Stay in Your Lane" - the LLM must stick to the specific task,
        not override it with user context preferences.
        """
        if not task_name:
            return ""
        
        task_lower = task_name.lower()
        query_lower = search_query.lower()
        
        constraints = []
        
        # CRITICAL RULE: STICK TO THE TASK
        constraints.append("CRITICAL RULE: STICK TO THE TASK")
        constraints.append(f'Your current task is: "{task_name}"')
        constraints.append("")
        
        # Rule 1: BV Tasks - MUST recommend BV
        if "bv" in task_lower or "bv" in query_lower or "b.v" in query_lower:
            constraints.append("1. This task is about researching BV (Besloten Vennootschap) structure.")
            constraints.append("   - You MUST recommend a BV structure.")
            constraints.append("   - Do NOT recommend a Branch Office, even if the user mentions urgency or speed.")
            constraints.append("   - If user context mentions 'urgent' or 'short-term', explain how to set up a BV quickly, but still recommend BV.")
            constraints.append("")
        
        # Rule 2: Branch Office Tasks - MUST recommend Branch
        if "branch" in task_lower or "branch" in query_lower:
            constraints.append("2. This task is about researching Branch Office structure.")
            constraints.append("   - You MUST recommend a Branch Office structure.")
            constraints.append("   - Do NOT mention notary requirements (Branch Offices don't need notaries).")
            constraints.append("   - Focus on speed and simplicity of Branch Office setup.")
            constraints.append("")
        
        # Rule 3: Holding Company Tasks - MUST focus on Holding/BV
        if "holding" in task_lower or "holding" in query_lower:
            constraints.append("3. This task is about Holding Company structures.")
            constraints.append("   - You MUST recommend a BV structure (required for participation exemption).")
            constraints.append("   - Do NOT recommend a Branch Office for holding companies.")
            constraints.append("   - Focus on Participation Exemption benefits.")
            constraints.append("   - Do NOT include Innovation Box or WBSO (these are for R&D companies, not financial holdings).")
            constraints.append("")
        
        # Rule 4: Tech/R&D Tasks - Only for Tech companies
        if "wbso" in task_lower or "innovation box" in task_lower or "r&d" in task_lower:
            constraints.append("4. This task is about R&D tax incentives (WBSO/Innovation Box).")
            constraints.append("   - Only include these if the company is in Software & Technology or R&D industries.")
            constraints.append("   - Do NOT include these for Financial Services or Holding companies.")
            constraints.append("")
        
        # Rule 5: Participation Exemption Tasks - Only for Holdings
        if "participation exemption" in task_lower or "deelnemingsvrijstelling" in query_lower:
            constraints.append("5. This task is about Participation Exemption.")
            constraints.append("   - This applies ONLY to Holding Companies.")
            constraints.append("   - Do NOT include this for regular operating companies.")
            constraints.append("")
        
        # General Rule: Ignore conflicting user context
        constraints.append("GENERAL RULE: The Task is the Source of Truth")
        constraints.append("   - The task name and search query define what you MUST research and recommend.")
        constraints.append("   - User context (like 'urgent timeline' or 'speed preference') is ONLY for personalization, NOT for changing the structure.")
        constraints.append("   - If the task says 'Research BV' but user context says 'urgent timeline',")
        constraints.append("     you MUST still recommend BV (you can mention 'fast-track BV setup' but recommend BV, not Branch).")
        constraints.append("   - If the task says 'Research Branch Office' but user context mentions 'BV',")
        constraints.append("     you MUST still recommend Branch Office (the task defines the structure, not user preferences).")
        constraints.append("   - Use ONLY the provided Context Documents. Do not use outside knowledge to override the task.")
        constraints.append("")
        constraints.append("REMEMBER: Do not think. Just write what the task requires based on the context provided.")
        constraints.append("")
        
        return "\n".join(constraints)
    
    def clean_json_response(self, text: str) -> str:
        """
        CRITICAL FIX: Strip Markdown code blocks and extract JSON from LLM response.
        
        LLMs often return JSON wrapped in ```json ... ``` blocks or with explanatory text.
        This function extracts the JSON portion.
        
        Args:
            text: Raw response text from LLM
        
        Returns:
            Cleaned text ready for JSON parsing
        """
        # Remove markdown code blocks (```json ... ``` or ``` ... ```)
        text = re.sub(r'```json\s*\n?', '', text)
        text = re.sub(r'```\s*\n?', '', text)
        text = text.strip()
        
        # Try to extract JSON object if there's explanatory text before it
        # Look for first { and last } to extract JSON object
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
        
        # Remove any leading/trailing whitespace
        return text.strip()
    
    def generate_section(
        self,
        section_name: str,
        search_query: str,
        user_context: Optional[Dict[str, Any]] = None,
        task_name: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a memo section using RAG.
        
        Args:
            section_name: Name of the section to generate
            search_query: Query to search the knowledge base
            user_context: Additional user context from request
        
        Returns:
            Generated section as dictionary, or None if generation fails
        """
        try:
            # Step 1: Retrieve relevant context from Qdrant
            print(f"  Searching Qdrant with query: {search_query}")
            search_results = self.qdrant_service.search(query=search_query)
            print(f"  Found {len(search_results)} search results")
            context = self.qdrant_service.format_context(search_results)
            
            # Step 2: Build user context string if provided
            user_context_str = ""
            if user_context:
                user_context_str = f"\n\nUSER CONTEXT:\n"
                user_context_str += f"Company: {user_context.get('company_name', 'N/A')}\n"
                user_context_str += f"Industry: {user_context.get('industry', 'N/A')}\n"
                user_context_str += f"Entry Goals: {', '.join(user_context.get('entry_goals', []))}\n"
            
            # Step 3: Generate prompt using MASTER_SYSTEM_PROMPT
            full_context = context + user_context_str
            
            # Define expected schema based on section name
            schema_examples = {
                "executive_summary": {
                    "overview": "Brief overview text",
                    "key_recommendations": ["Recommendation 1", "Recommendation 2"],
                    "critical_considerations": ["Consideration 1", "Consideration 2"]
                },
                "tax_considerations": {
                    "corporate_tax_rate": "25.8% for 2025",
                    "tax_obligations": ["Obligation 1", "Obligation 2"],
                    "tax_optimization_strategies": ["Strategy 1", "Strategy 2"],
                    "special_regimes": ["Participation Exemption (deelnemingsvrijstelling)", "Innovation Box", "WBSO R&D tax credit"]
                },
                "market_entry_options": {
                    "recommended_option": "Recommended option description",
                    "option_comparison": [{"option": "Option 1", "description": "..."}],
                    "pros_and_cons": {"option1": ["Advantage 1", "Advantage 2"], "option2": ["Advantage 1", "Advantage 2"]}
                },
                "implementation_timeline": {
                    "phases": [{"phase": "Phase 1", "duration": "..."}],
                    "estimated_duration": "3-6 months",
                    "milestones": ["Milestone 1", "Milestone 2"]
                }
            }
            
            schema_example = schema_examples.get(section_name, {})
            schema_json = json.dumps(schema_example, indent=2) if schema_example else "{}"
            
            # Build task-specific constraints
            task_constraints = self._build_task_constraints(task_name, section_name, search_query)
            
            prompt = f"""{MASTER_SYSTEM_PROMPT}

TASK: Generate the "{section_name}" section of a Market Entry Memo for the Netherlands.

{task_constraints}

CONTEXT FROM KNOWLEDGE BASE:
{full_context}

EXPECTED JSON STRUCTURE:
{schema_json}

INSTRUCTIONS:
1. Extract relevant information from the context above.
2. Write the {section_name} section in a direct, actionable style.
3. If information is missing, state that clearly rather than guessing.
4. Return ONLY valid JSON matching the structure above. Use the exact key names shown.
5. Do NOT wrap the JSON in the section name. Return the object directly.
6. Do NOT include any explanatory text before or after the JSON.
7. Be practical and focus on what the company can actually do.
8. IMPORTANT for tax_considerations: If the context mentions participation exemption, holding companies, or deelnemingsvrijstelling, you MUST include "Participation Exemption (deelnemingsvrijstelling)" in the special_regimes array.
9. IMPORTANT for tax_considerations: Include ALL relevant special tax regimes mentioned in the context (WBSO, Innovation Box, Participation Exemption, etc.).

Return your response as pure JSON only.
"""
            
            # Step 4: Call OpenAI
            print(f"  Calling OpenAI API with model: {self.model}")
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Generate the {section_name} section now."}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Step 5: Parse response
            content = response.choices[0].message.content
            print(f"  Received response from OpenAI (length: {len(content)} chars)")
            
            # CRITICAL FIX: Clean JSON response before parsing
            cleaned_content = self.clean_json_response(content)
            
            # Try to parse as JSON, fallback to text
            try:
                parsed = json.loads(cleaned_content)
                print(f"  Successfully parsed JSON response")
                return parsed
            except json.JSONDecodeError as e:
                print(f"  WARNING: Could not parse as JSON: {str(e)}")
                print(f"  Response preview: {cleaned_content[:200]}...")
                # If not JSON, return as text content
                return {"content": cleaned_content}
        
        except Exception as e:
            import traceback
            print(f"ERROR: RAG generation error for {section_name}: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return None
    
    def generate_memo_sections(
        self,
        tasks: list,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate all memo sections based on task plan.
        
        Args:
            tasks: List of TaskPlan objects
            user_context: User context from request
        
        Returns:
            Dictionary mapping section names to generated content
        """
        sections = {}
        
        for task in tasks:
            section_name = task.section_name
            search_query = task.search_query
            task_name = task.task_name
            
            print(f"Generating section: {section_name} (Task: {task_name})")
            generated = self.generate_section(
                section_name=section_name,
                search_query=search_query,
                user_context=user_context,
                task_name=task_name
            )
            
            if generated:
                sections[section_name] = generated
        
        return sections

