"""Test script to run all test scenarios against the API."""
import requests
import json
import time
from pathlib import Path

# Load test scenarios
scenarios_file = Path(__file__).parent / "TEST_SCENARIOS.json"
with open(scenarios_file, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

API_URL = "http://localhost:8000/generate-memo"

def test_scenario(scenario_name, request_data, index, total):
    """Test a single scenario."""
    print(f"\n{'='*80}")
    print(f"TEST {index}/{total}: {scenario_name}")
    print(f"{'='*80}")
    print(f"Request: {json.dumps(request_data, indent=2)}")
    print(f"\nSending request to {API_URL}...")
    
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=request_data, timeout=180)
        elapsed_time = time.time() - start_time
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Time: {elapsed_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            
            # Count non-null sections
            non_null_sections = sum(1 for v in result.values() if v is not None)
            total_sections = len(result)
            
            print(f"\n✅ SUCCESS!")
            print(f"   Sections populated: {non_null_sections}/{total_sections}")
            
            # Show which sections have data
            populated = [k for k, v in result.items() if v is not None]
            print(f"   Populated sections: {', '.join(populated)}")
            
            # Show preview of key sections
            if result.get("executiveSummary"):
                overview = result["executiveSummary"].get("overview", "N/A")
                if overview:
                    print(f"\n   Executive Summary Preview: {overview[:100]}...")
            
            if result.get("taxConsiderations"):
                tax_rate = result["taxConsiderations"].get("corporateTaxRate", "N/A")
                print(f"   Corporate Tax Rate: {tax_rate}")
            
            return True
        else:
            print(f"\n❌ ERROR: Status {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: Could not connect to API at {API_URL}")
        print("   Make sure the server is running: uvicorn app.main:app --reload")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ ERROR: Request timed out after 180 seconds")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

def main():
    """Run all test scenarios."""
    print("="*80)
    print("TAX MEMO API - TEST SCENARIOS")
    print("="*80)
    print(f"\nTesting API at: {API_URL}")
    print("Make sure the server is running before starting tests!")
    print("\nPress Ctrl+C to stop at any time...")
    time.sleep(2)
    
    results = []
    
    # Test all scenarios
    scenarios = test_data["scenarios"]
    for i, scenario in enumerate(scenarios, 1):
        success = test_scenario(
            scenario["name"],
            scenario["request"],
            i,
            len(scenarios)
        )
        results.append((scenario["name"], success))
        time.sleep(1)  # Small delay between requests
    
    # Test minimal request
    print(f"\n{'='*80}")
    print("MINIMAL TEST")
    print(f"{'='*80}")
    minimal_success = test_scenario(
        test_data["minimal_test"]["name"],
        test_data["minimal_test"]["request"],
        len(scenarios) + 1,
        len(scenarios) + 2
    )
    results.append((test_data["minimal_test"]["name"], minimal_success))
    
    # Summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    print("\nDetailed Results:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {name}")

if __name__ == "__main__":
    main()

