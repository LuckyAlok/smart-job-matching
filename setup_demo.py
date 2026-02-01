import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:3000"

def print_step(title):
    print(f"\n👉 {title}...")
    time.sleep(0.5)

def run_demo_setup():
    print("🚀 Starting Live Demo Setup 🚀")

    # 1. Register Demo User
    print_step("Creating Demo User Account")
    user_data = {
        "email": "demo_user@example.com",
        "password": "password123",
        "full_name": "Demo User"
    }
    
    # Try register, if exists, login
    resp = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if resp.status_code == 200:
        print("   ✅ User created successfully.")
    elif resp.status_code == 400 and "already exists" in resp.text:
        print("   ℹ️  User already exists, proceeding.")
    else:
        print(f"   ❌ Registration failed: {resp.text}")
        return

    # 2. Login
    print_step("Logging in")
    login_data = {
        "username": "demo_user@example.com",
        "password": "password123"
    }
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if resp.status_code != 200:
        print(f"   ❌ Login failed: {resp.text}")
        return
    
    token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("   ✅ Login successful. Access Token acquired.")

    # 3. Upload Matching Resume
    print_step("Uploading Resume (Frontend Developer Profile)")
    try:
        with open("matching_resume.pdf", "rb") as f:
            files = {"file": ("matching_resume.pdf", f, "application/pdf")}
            resp = requests.post(f"{BASE_URL}/resume/upload", headers=headers, files=files)
            if resp.status_code == 200:
                 print("   ✅ Resume uploaded & parsed.")
                 skills = resp.json()['parsed_data']['skills']
                 print(f"   📄 Extracted Skills: {', '.join(skills)}")
            else:
                 print(f"   ❌ Upload Failed: {resp.status_code} - {resp.text}")
    except FileNotFoundError:
        print("   ❌ matching_resume.pdf not found.")
        return

    # 4. Trigger Match
    print_step("Calculating Job Matches")
    # Get Roles
    resp = requests.get(f"{BASE_URL}/job-roles/", headers=headers)
    roles = resp.json()
    
    frontend_role = next((r for r in roles if r['title'] == "Frontend Developer"), None)
    
    if frontend_role:
        role_id = frontend_role['id']
        resp = requests.post(f"{BASE_URL}/matches/{role_id}", headers=headers)
        if resp.status_code == 200:
            score = resp.json()['score']
            print(f"   🎯 Match Calculated for 'Frontend Developer': {score}%")
            if score > 80:
                print("   🔥 High Match! This candidate is a strong fit.")
        else:
            print(f"   ❌ Match calculation failed: {resp.text}")

    print("\n✨ Demo Data Setup Complete! ✨")
    print("\n--------------------------------------------------------------")
    print(f"Use these credentials to view the dashboard:")
    print(f"📧 Email:    demo_user@example.com")
    print(f"🔑 Password: password123")
    print("--------------------------------------------------------------\n")

if __name__ == "__main__":
    run_demo_setup()
