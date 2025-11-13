"""Direct test of RAG engine to diagnose empty response issue."""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

from app.services.rag_engine import RAGEngine
from app.core.orchestrator import Orchestrator, TaskPlan
from app.models.request import TaxMemoRequest

def test_rag_engine():
    """Test RAG engine directly."""
    print("=" * 80)
    print("Testing RAG Engine Directly")
    print("=" * 80)
    
    # Initialize
    print("\n1. Initializing RAG Engine...")
    try:
        rag_engine = RAGEngine()
        print("   ✓ RAG Engine initialized")
    except Exception as e:
        print(f"   ✗ Failed to initialize RAG Engine: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test a simple query
    print("\n2. Testing Qdrant search...")
    try:
        search_results = rag_engine.qdrant_service.search("Netherlands corporate income tax rates 2025")
        print(f"   ✓ Found {len(search_results)} search results")
        if search_results:
            print(f"   First result score: {search_results[0].get('score', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Qdrant search failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test section generation
    print("\n3. Testing section generation...")
    try:
        user_context = {
            "company_name": "SaaS Innovators Inc.",
            "industry": "Software & Technology",
            "entry_goals": ["Establish physical presence", "Tax optimization"]
        }
        
        result = rag_engine.generate_section(
            section_name="tax_considerations",
            search_query="Netherlands corporate income tax rates WBSO R&D tax credit 2025",
            user_context=user_context
        )
        
        if result:
            print(f"   ✓ Section generated successfully")
            print(f"   Result type: {type(result)}")
            print(f"   Result keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
            print(f"   Result preview: {str(result)[:200]}...")
        else:
            print("   ✗ Section generation returned None")
    except Exception as e:
        print(f"   ✗ Section generation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test full memo generation
    print("\n4. Testing full memo generation...")
    try:
        orchestrator = Orchestrator()
        request = TaxMemoRequest(
            company_name="SaaS Innovators Inc.",
            industry="Software & Technology",
            entry_goals=["Establish physical presence", "Tax optimization"],
            primary_jurisdiction="Netherlands",
            tax_considerations=["Corporate income tax implications"]
        )
        
        tasks = orchestrator.plan_tasks(request)
        print(f"   ✓ Planned {len(tasks)} tasks")
        
        user_context = {
            "company_name": request.company_name,
            "industry": request.industry,
            "entry_goals": request.entry_goals or []
        }
        
        sections = rag_engine.generate_memo_sections(tasks, user_context)
        print(f"   ✓ Generated {len(sections)} sections")
        print(f"   Section keys: {list(sections.keys())}")
        
        for key, value in sections.items():
            print(f"   - {key}: {type(value).__name__}")
            if isinstance(value, dict):
                print(f"     Keys: {list(value.keys())}")
        
    except Exception as e:
        print(f"   ✗ Full memo generation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 80)
    print("Test Complete!")
    print("=" * 80)

if __name__ == "__main__":
    test_rag_engine()

