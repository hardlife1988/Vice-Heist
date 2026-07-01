#!/usr/bin/env python3
"""
Test runner for Vice-heist game.
Runs all tests and generates a detailed report.
"""

import sys
import os
import unittest
from io import StringIO
import json
from datetime import datetime

# Add math directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'math'))

def run_tests():
    """
    Run all tests and generate report.
    
    Returns:
        dict: Test results
    """
    # Load test module
    loader = unittest.TestLoader()
    suite = loader.discover('math/tests', pattern='test_*.py')
    
    # Run tests with detailed output
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    # Extract results
    output = stream.getvalue()
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "game": "Vice-heist",
        "summary": {
            "total_tests": result.testsRun,
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "failed": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped),
        },
        "success": result.wasSuccessful(),
        "output": output,
    }
    
    # Add failure details
    if result.failures:
        test_results["failures"] = []
        for test, traceback in result.failures:
            test_results["failures"].append({
                "test": str(test),
                "traceback": traceback,
            })
    
    # Add error details
    if result.errors:
        test_results["errors"] = []
        for test, traceback in result.errors:
            test_results["errors"].append({
                "test": str(test),
                "traceback": traceback,
            })
    
    return test_results

def print_report(results):
    """
    Print formatted test report.
    
    Args:
        results: Test results dict
    """
    summary = results["summary"]
    
    print("\n" + "="*60)
    print("VICE-HEIST TEST REPORT")
    print("="*60 + "\n")
    
    print(f"Timestamp: {results['timestamp']}")
    print(f"Game: {results['game']}\n")
    
    print("Test Summary:")
    print(f"  Total Tests:    {summary['total_tests']}")
    print(f"  ✅ Passed:      {summary['passed']}")
    print(f"  ❌ Failed:      {summary['failed']}")
    print(f"  ⚠️  Errors:      {summary['errors']}")
    print(f"  ⊘ Skipped:      {summary['skipped']}\n")
    
    if results["success"]:
        print("✅ ALL TESTS PASSED!\n")
    else:
        print("❌ TESTS FAILED\n")
        
        if "failures" in results:
            print("Failures:")
            for failure in results["failures"]:
                print(f"  • {failure['test']}")
                print(f"    {failure['traceback'][:200]}...\n")
        
        if "errors" in results:
            print("Errors:")
            for error in results["errors"]:
                print(f"  • {error['test']}")
                print(f"    {error['traceback'][:200]}...\n")
    
    print("\nDetailed Output:")
    print("-"*60)
    print(results["output"])
    print("-"*60 + "\n")
    
    return results["success"]

if __name__ == "__main__":
    print("Running Vice-heist test suite...")
    results = run_tests()
    success = print_report(results)
    
    # Save results to file
    with open('math/library/publish_files/test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Test results saved to: math/library/publish_files/test_results.json\n")
    
    sys.exit(0 if success else 1)
