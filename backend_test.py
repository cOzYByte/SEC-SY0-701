import requests
import sys
import json
from datetime import datetime

class SecurityPlusAPITester:
    def __init__(self, base_url="https://secplus-prep-1.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_user_email = f"test_user_{datetime.now().strftime('%H%M%S')}@example.com"
        self.test_user_password = "TestPass123!"
        self.test_user_name = "Test User"

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, params=data)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_domains_endpoint(self):
        """Test domains endpoint"""
        return self.run_test("Get Domains", "GET", "domains", 200)

    def test_user_registration(self):
        """Test user registration"""
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data={
                "email": self.test_user_email,
                "password": self.test_user_password,
                "name": self.test_user_name
            }
        )
        if success and 'token' in response:
            self.token = response['token']
            self.user_id = response['user']['id']
            print(f"   Token received: {self.token[:20]}...")
            return True
        return False

    def test_user_login(self):
        """Test user login"""
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data={
                "email": self.test_user_email,
                "password": self.test_user_password
            }
        )
        if success and 'token' in response:
            self.token = response['token']
            self.user_id = response['user']['id']
            print(f"   Login token: {self.token[:20]}...")
            return True
        return False

    def test_get_current_user(self):
        """Test get current user endpoint"""
        if not self.token:
            print("❌ No token available for authentication test")
            return False
        return self.run_test("Get Current User", "GET", "auth/me", 200)[0]

    def test_seed_questions(self):
        """Test seeding questions"""
        return self.run_test("Seed Questions", "POST", "seed-questions", 200)[0]

    def test_get_questions(self):
        """Test get questions endpoint"""
        if not self.token:
            print("❌ No token available for questions test")
            return False
        return self.run_test("Get Questions", "GET", "questions", 200)[0]

    def test_get_practice_questions(self):
        """Test get practice questions"""
        if not self.token:
            print("❌ No token available for practice questions test")
            return False
        success, response = self.run_test(
            "Get Practice Questions", 
            "GET", 
            "questions/practice", 
            200,
            data={"count": 5}
        )
        if success and isinstance(response, list) and len(response) > 0:
            print(f"   Received {len(response)} practice questions")
            return True
        return False

    def test_get_exam_questions(self):
        """Test get exam questions"""
        if not self.token:
            print("❌ No token available for exam questions test")
            return False
        success, response = self.run_test("Get Exam Questions", "GET", "questions/exam", 200)
        if success and isinstance(response, list):
            print(f"   Received {len(response)} exam questions")
            return True
        return False

    def test_get_flashcards(self):
        """Test get flashcards"""
        if not self.token:
            print("❌ No token available for flashcards test")
            return False
        success, response = self.run_test(
            "Get Flashcards", 
            "GET", 
            "questions/flashcards", 
            200,
            data={"count": 10}
        )
        if success and isinstance(response, list):
            print(f"   Received {len(response)} flashcards")
            return True
        return False

    def test_get_progress(self):
        """Test get progress"""
        if not self.token:
            print("❌ No token available for progress test")
            return False
        return self.run_test("Get Progress", "GET", "progress", 200)[0]

    def test_submit_answers(self):
        """Test submit answers"""
        if not self.token:
            print("❌ No token available for submit answers test")
            return False
        
        # First get some practice questions
        success, questions = self.run_test(
            "Get Questions for Submission", 
            "GET", 
            "questions/practice", 
            200,
            data={"count": 2}
        )
        
        if not success or not questions:
            print("❌ Failed to get questions for submission test")
            return False

        # Submit answers for the questions
        submission_data = {
            "answers": [
                {
                    "question_id": questions[0]["id"],
                    "selected_answer": questions[0]["correct_answer"],  # Correct answer
                    "time_taken": 30
                },
                {
                    "question_id": questions[1]["id"],
                    "selected_answer": "a",  # Potentially incorrect answer
                    "time_taken": 45
                }
            ],
            "mode": "practice",
            "total_time": 75
        }
        
        return self.run_test("Submit Answers", "POST", "progress/submit", 200, data=submission_data)[0]

    def test_get_history(self):
        """Test get history"""
        if not self.token:
            print("❌ No token available for history test")
            return False
        return self.run_test("Get History", "GET", "progress/history", 200)[0]

    def test_get_weak_areas(self):
        """Test get weak areas"""
        if not self.token:
            print("❌ No token available for weak areas test")
            return False
        return self.run_test("Get Weak Areas", "GET", "progress/weak-areas", 200)[0]

    def test_invalid_login(self):
        """Test invalid login credentials"""
        success, response = self.run_test(
            "Invalid Login",
            "POST",
            "auth/login",
            401,
            data={
                "email": "invalid@example.com",
                "password": "wrongpassword"
            }
        )
        return success  # Success means we got the expected 401 status

    def test_duplicate_registration(self):
        """Test duplicate user registration"""
        success, response = self.run_test(
            "Duplicate Registration",
            "POST",
            "auth/register",
            400,
            data={
                "email": self.test_user_email,  # Same email as before
                "password": self.test_user_password,
                "name": "Another User"
            }
        )
        return success  # Success means we got the expected 400 status

    def test_unauthorized_access(self):
        """Test accessing protected endpoint without token"""
        original_token = self.token
        self.token = None  # Remove token temporarily
        
        success, response = self.run_test("Unauthorized Access", "GET", "progress", 401)
        
        self.token = original_token  # Restore token
        return success

def main():
    print("🚀 Starting CompTIA Security+ API Tests")
    print("=" * 50)
    
    tester = SecurityPlusAPITester()
    
    # Test sequence
    tests = [
        ("Root API", tester.test_root_endpoint),
        ("Domains", tester.test_domains_endpoint),
        ("Seed Questions", tester.test_seed_questions),
        ("User Registration", tester.test_user_registration),
        ("User Login", tester.test_user_login),
        ("Get Current User", tester.test_get_current_user),
        ("Get Questions", tester.test_get_questions),
        ("Get Practice Questions", tester.test_get_practice_questions),
        ("Get Exam Questions", tester.test_get_exam_questions),
        ("Get Flashcards", tester.test_get_flashcards),
        ("Get Progress", tester.test_get_progress),
        ("Submit Answers", tester.test_submit_answers),
        ("Get History", tester.test_get_history),
        ("Get Weak Areas", tester.test_get_weak_areas),
        ("Invalid Login", tester.test_invalid_login),
        ("Duplicate Registration", tester.test_duplicate_registration),
        ("Unauthorized Access", tester.test_unauthorized_access),
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} - Exception: {str(e)}")
            failed_tests.append(test_name)
    
    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if failed_tests:
        print(f"\n❌ Failed Tests ({len(failed_tests)}):")
        for test in failed_tests:
            print(f"   - {test}")
    else:
        print("\n🎉 All tests passed!")
    
    success_rate = (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0
    print(f"\n📈 Success Rate: {success_rate:.1f}%")
    
    return 0 if len(failed_tests) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())