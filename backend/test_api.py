"""Test script for the Tax Memo Orchestrator API."""
import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"
GENERATE_MEMO_URL = f"{BASE_URL}/generate-memo"

# Test request - minimal example
minimal_request = {
    "company_name": "TechStart Inc",
    "industry": "Software & Technology",
    "entry_goals": ["Hire employees"],
    "selected_legal_topics": ["employment-law"]
}

# Test request - full example (load from file)
try:
    with open("EXAMPLE_REQUEST.json", "r", encoding="utf-8") as f:
        full_request = json.load(f)
except FileNotFoundError:
    full_request = minimal_request

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Is it running?")
        print("Start the server with: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_generate_memo(request_data, use_minimal=True):
    """Test the generate-memo endpoint."""
    request_type = "minimal" if use_minimal else "full"
    print(f"\n{'='*60}")
    print(f"Testing generate-memo with {request_type} request...")
    print(f"{'='*60}")
    
    try:
        print(f"Sending request to: {GENERATE_MEMO_URL}")
        print(f"Company: {request_data.get('company_name')}")
        print(f"Industry: {request_data.get('industry', 'N/A')}")
        
        response = requests.post(
            GENERATE_MEMO_URL,
            json=request_data,
            timeout=120  # 2 minutes timeout for generation
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\nSUCCESS! Memo generated.")
            print(f"\nGenerated Sections:")
            
            # Count non-null sections
            sections_generated = 0
            for section_name, section_data in result.items():
                if section_data is not None:
                    sections_generated += 1
                    print(f"  [OK] {section_name}")
            
            print(f"\nTotal sections generated: {sections_generated}/13")
            
            # Show a sample section
            if result.get("executive_summary"):
                print("\nSample: Executive Summary")
                exec_summary = result["executive_summary"]
                if exec_summary.get("overview"):
                    preview = exec_summary["overview"][:200]
                    print(f"   {preview}...")
            
            return True
        else:
            print(f"ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out (took longer than 2 minutes)")
        return False
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Tax Memo Orchestrator API Test")
    print("="*60)
    
    # Step 1: Health check
    if not test_health_check():
        exit(1)
    
    # Step 2: Test with minimal request
    print("\n" + "="*60)
    print("Step 1: Testing with minimal request")
    print("="*60)
    test_generate_memo(minimal_request, use_minimal=True)
    
    # Step 3: Optional - Test with full request
    print("\n" + "="*60)
    print("Step 2: Testing with full request (optional)")
    print("="*60)
    user_input = input("\nTest with full request? (y/n): ").strip().lower()
    if user_input == 'y':
        test_generate_memo(full_request, use_minimal=False)
    
    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60)
    print("\nTips:")
    print("  - View full API docs at: http://localhost:8000/docs")
    print("  - Use Swagger UI to test different requests interactively")
    print("  - Check the response structure in the generated memo")

