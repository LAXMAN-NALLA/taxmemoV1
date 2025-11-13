"""Test script using sample inputs from SAMPLE_TEST_INPUTS.json."""
import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
GENERATE_MEMO_URL = f"{BASE_URL}/generate-memo"

def load_test_cases() -> list:
    """Load test cases from JSON file."""
    try:
        with open("SAMPLE_TEST_INPUTS.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("test_cases", [])
    except FileNotFoundError:
        print("ERROR: SAMPLE_TEST_INPUTS.json not found!")
        return []

def test_health_check() -> bool:
    """Test if server is running."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_test_case(test_case: Dict[str, Any], index: int, total: int) -> bool:
    """Run a single test case."""
    name = test_case.get("name", f"Test {index}")
    description = test_case.get("description", "")
    request_data = test_case.get("request", {})
    expected_triggers = test_case.get("expected_triggers", [])
    
    print("\n" + "="*80)
    print(f"TEST {index}/{total}: {name}")
    print("="*80)
    print(f"Description: {description}")
    print(f"\nRequest:")
    print(json.dumps(request_data, indent=2))
    
    if expected_triggers:
        print(f"\nExpected Triggers:")
        for trigger in expected_triggers:
            print(f"  - {trigger}")
    
    try:
        print(f"\nSending request to {GENERATE_MEMO_URL}...")
        start_time = time.time()
        
        response = requests.post(
            GENERATE_MEMO_URL,
            json=request_data,
            timeout=180  # 3 minutes timeout
        )
        
        elapsed_time = time.time() - start_time
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Time: {elapsed_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            
            # Count generated sections
            sections_generated = sum(1 for v in result.values() if v is not None)
            print(f"\nSUCCESS! Generated {sections_generated}/13 sections")
            
            # Show which sections were generated
            print("\nGenerated Sections:")
            for section_name, section_data in result.items():
                if section_data is not None:
                    print(f"  [OK] {section_name}")
                else:
                    print(f"  [--] {section_name} (not generated)")
            
            # Show sample content from first non-null section
            for section_name, section_data in result.items():
                if section_data is not None:
                    print(f"\nSample Content - {section_name}:")
                    if isinstance(section_data, dict):
                        # Show first few keys
                        keys = list(section_data.keys())[:3]
                        for key in keys:
                            value = section_data.get(key)
                            if isinstance(value, str):
                                preview = value[:150] + "..." if len(value) > 150 else value
                                print(f"  {key}: {preview}")
                            elif isinstance(value, list) and value:
                                print(f"  {key}: [{len(value)} items]")
                            else:
                                print(f"  {key}: {value}")
                    break
            
            return True
        else:
            print(f"\nERROR: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print("\nERROR: Request timed out (> 3 minutes)")
        return False
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to server")
        print("Make sure the server is running: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return False

def main():
    """Main test runner."""
    print("="*80)
    print("Tax Memo Orchestrator API - Sample Test Runner")
    print("="*80)
    
    # Check if server is running
    print("\nChecking server health...")
    if not test_health_check():
        print("ERROR: Server is not running!")
        print("Start the server with: uvicorn app.main:app --reload")
        return
    print("Server is running!")
    
    # Load test cases
    print("\nLoading test cases...")
    test_cases = load_test_cases()
    
    if not test_cases:
        print("No test cases found!")
        return
    
    print(f"Loaded {len(test_cases)} test cases")
    
    # Ask user which tests to run
    print("\n" + "="*80)
    print("Test Selection:")
    print("="*80)
    print("1. Run all tests")
    print("2. Run specific test by number")
    print("3. Run first 3 tests (quick test)")
    print("4. Exit")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"   {i}. {test_case.get('name', 'Unnamed Test')}")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Run all tests
        selected_tests = test_cases
    elif choice == "2":
        # Run specific test
        test_num = input(f"Enter test number (1-{len(test_cases)}): ").strip()
        try:
            idx = int(test_num) - 1
            if 0 <= idx < len(test_cases):
                selected_tests = [test_cases[idx]]
            else:
                print("Invalid test number!")
                return
        except ValueError:
            print("Invalid input!")
            return
    elif choice == "3":
        # Run first 3
        selected_tests = test_cases[:3]
    elif choice == "4":
        return
    else:
        print("Invalid choice!")
        return
    
    # Run selected tests
    print(f"\nRunning {len(selected_tests)} test(s)...")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(selected_tests, 1):
        if run_test_case(test_case, i, len(selected_tests)):
            passed += 1
        else:
            failed += 1
        
        # Ask if user wants to continue after each test
        if i < len(selected_tests):
            continue_choice = input("\nPress Enter to continue to next test, or 'q' to quit: ").strip().lower()
            if continue_choice == 'q':
                break
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {len(selected_tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("="*80)

if __name__ == "__main__":
    main()

