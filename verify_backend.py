import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_trial():
    print("--- Starting Backend Trial ---")

    # 1. Seed Database
    try:
        resp = requests.get(f"{BASE_URL}/seed")
        print(f"1. Seeding: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"1. Seeding Failed: {e}")
        return

    # 2. Register
    user_data = {
        "email": "trial_test@example.com",
        "password": "password123",
        "full_name": "Trial Tester"
    }
    # Clean up if exists (optional, or just handle 400)
    # Registration
    resp = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if resp.status_code == 200:
        print(f"2. Registration Success: {resp.json()}")
    elif resp.status_code == 400 and "already exists" in resp.text:
        print("2. User already registered, proceeding to login.")
    else:
        print(f"2. Registration Failed: {resp.status_code} - {resp.text}")
        return

    # 3. Login
    login_data = {
        "username": "trial_test@example.com",
        "password": "password123"
    }
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data) # OAuth2 uses form data
    if resp.status_code != 200:
        print(f"3. Login Failed: {resp.status_code} - {resp.text}")
        return
    
    token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("3. Login Success, Token received.")

    # 4. Upload Resume
    try:
        with open("dummy_resume.pdf", "rb") as f:
            files = {"file": ("dummy_resume.pdf", f, "application/pdf")}
            resp = requests.post(f"{BASE_URL}/resume/upload", headers=headers, files=files)
            if resp.status_code == 200:
                 print(f"4. Upload Success: {resp.json()}")
            else:
                 print(f"4. Upload Failed: {resp.status_code} - {resp.text}")
    except FileNotFoundError:
        print("4. Upload Failed: dummy_resume.pdf not found.")

    # 5. Get Job Roles (to get an ID to match)
    resp = requests.get(f"{BASE_URL}/job-roles/", headers=headers)
    if resp.status_code != 200:
        print(f"5. Get Job Roles Failed: {resp.status_code}")
        return
    
    roles = resp.json()
    print(f"5. Found {len(roles)} Job Roles.")

    if roles:
        role_id = roles[0]['id']
        print(f"   Matching against Role ID {role_id} ({roles[0]['title']})...")
        
        # 6. Match
        resp = requests.post(f"{BASE_URL}/matches/{role_id}", headers=headers)
        if resp.status_code == 200:
            match_data = resp.json()
            print(f"6. Match Result: Score {match_data.get('score')}")
            print(f"   Missing Skills: {match_data.get('missing_skills')}")

            # 7. Recommendations
            missing = match_data.get('missing_skills', [])
            if missing:
                skills_query = ",".join(missing)
                resp = requests.get(f"{BASE_URL}/courses/recommendations?skills={skills_query}", headers=headers)
                print(f"7. Recommendations: {resp.status_code}")
                # print(resp.json()) # Verbose
        else:
            print(f"6. Match Failed: {resp.status_code} - {resp.text}")

    print("--- Trial Complete ---")

if __name__ == "__main__":
    run_trial()
