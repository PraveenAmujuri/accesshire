import pytest
from app.services.auth_service import AuthService

def test_user_registration_hashes_password(client):
    """Verifies that registration securely hashes passwords with bcrypt and returns JWT token."""
    payload = {
        "name": "Maya Lin",
        "email": "maya@example.com",
        "password": "SuperSecretPassword123!",
        "accessibility_preferences": {
            "simplified_language": True,
            "extended_response_time": True,
            "high_contrast": False
        }
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "maya@example.com"
    assert data["name"] == "Maya Lin"
    assert data["user_id"].startswith("user_")

    # Login to confirm credentials match the stored bcrypt hash
    login_res = client.post("/api/auth/login", json={
        "email": "maya@example.com",
        "password": "SuperSecretPassword123!"
    })
    assert login_res.status_code == 200

    # Wrong password must be rejected by bcrypt comparison
    wrong_res = client.post("/api/auth/login", json={
        "email": "maya@example.com",
        "password": "WrongPassword!"
    })
    assert wrong_res.status_code == 401

def test_registration_duplicate_email_rejected(client):
    """Verifies that registering with an already existing email returns 409 Conflict."""
    payload = {
        "name": "First User",
        "email": "duplicate@example.com",
        "password": "Password123!"
    }
    res1 = client.post("/api/auth/register", json=payload)
    assert res1.status_code == 201

    # Second attempt with same email
    res2 = client.post("/api/auth/register", json=payload)
    assert res2.status_code == 409
    assert "already exists" in res2.json()["detail"]

def test_registration_short_password_rejected(client):
    """Verifies that short passwords (< 6 chars) are rejected with 422."""
    payload = {
        "name": "Weak User",
        "email": "weak@example.com",
        "password": "123"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 422
    assert "at least 6 characters" in res.json()["detail"]

def test_login_success_and_invalid_credentials(client):
    """Verifies login succeeds with correct password and rejects invalid credentials with 401."""
    # 1. Register candidate
    reg_res = client.post("/api/auth/register", json={
        "name": "Ethan Hunt",
        "email": "ethan@imf.org",
        "password": "MissionImpossiblePassword!"
    })
    assert reg_res.status_code == 201

    # 2. Login with correct password
    login_res = client.post("/api/auth/login", json={
        "email": "ethan@imf.org",
        "password": "MissionImpossiblePassword!"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["email"] == "ethan@imf.org"

    # 3. Login with wrong password -> 401
    bad_pw_res = client.post("/api/auth/login", json={
        "email": "ethan@imf.org",
        "password": "WrongPassword!"
    })
    assert bad_pw_res.status_code == 401
    assert "Invalid email or password" in bad_pw_res.json()["detail"]

    # 4. Login with non-existent email -> 401
    bad_email_res = client.post("/api/auth/login", json={
        "email": "ghost@imf.org",
        "password": "MissionImpossiblePassword!"
    })
    assert bad_email_res.status_code == 401
    assert "Invalid email or password" in bad_email_res.json()["detail"]

def test_protected_profile_requires_valid_bearer_token(client):
    """Verifies that protected routes reject unauthenticated requests with 401."""
    # Request without Authorization header
    unauth_res = client.get("/api/users/me")
    assert unauth_res.status_code == 401
    assert "Authentication required" in unauth_res.json()["detail"]

    # Request with invalid/tampered token
    invalid_res = client.get("/api/users/me", headers={"Authorization": "Bearer fake.tampered.token"})
    assert invalid_res.status_code == 401
    assert "Invalid or expired" in invalid_res.json()["detail"]

def test_user_profile_and_preferences_lifecycle(client):
    """Verifies getting profile and updating accessibility preferences."""
    # Register candidate with custom preferences
    reg_res = client.post("/api/auth/register", json={
        "name": "Ada Lovelace",
        "email": "ada@analytics.org",
        "password": "BabbageEngine1842!",
        "accessibility_preferences": {
            "high_contrast": True,
            "simplified_language": True,
            "extended_response_time": True
        }
    })
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch profile
    me_res = client.get("/api/users/me", headers=headers)
    assert me_res.status_code == 200
    profile = me_res.json()
    assert profile["name"] == "Ada Lovelace"
    assert profile["email"] == "ada@analytics.org"
    assert profile["accessibility_preferences"]["high_contrast"] is True
    assert profile["accessibility_preferences"]["simplified_language"] is True

    # Update preferences
    updated_prefs = {
        "high_contrast": False,
        "font_size": "large",
        "voice_mode_enabled": True,
        "speech_rate": 0.85,
        "simplified_language": True,
        "extended_response_time": True
    }
    put_res = client.put("/api/users/preferences", json=updated_prefs, headers=headers)
    assert put_res.status_code == 200
    assert put_res.json()["font_size"] == "large"
    assert put_res.json()["speech_rate"] == 0.85

    # Re-fetch profile to confirm persistence
    me_res2 = client.get("/api/users/me", headers=headers)
    assert me_res2.status_code == 200
    assert me_res2.json()["accessibility_preferences"]["font_size"] == "large"
    assert me_res2.json()["accessibility_preferences"]["speech_rate"] == 0.85
