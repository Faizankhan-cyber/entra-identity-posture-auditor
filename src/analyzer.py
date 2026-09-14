from datetime import datetime, timezone


PRIVILEGED_ROLES = {
    "Global Administrator",
    "Privileged Role Administrator",
    "Security Administrator",
    "User Administrator",
}


def parse_datetime(value):
    """Convert an ISO 8601 timestamp into a timezone-aware datetime."""
    if not value:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def analyze_mfa(users, mfa_registration, role_assignments):
    """Find privileged users who have not registered MFA."""

    mfa_by_user = {
        item["userId"]: item
        for item in mfa_registration
    }

    privileged_users = {
        role["userId"]: role
        for role in role_assignments
        if role["roleName"] in PRIVILEGED_ROLES
    }

    findings = []

    for user in users:
        user_id = user["id"]

        if user_id not in privileged_users:
            continue

        mfa_info = mfa_by_user.get(user_id)

        if not mfa_info or not mfa_info.get("isMfaRegistered", False):
            findings.append({
                "type": "privileged_user_without_mfa",
                "severity": "HIGH",
                "userId": user_id,
                "userPrincipalName": user["userPrincipalName"],
                "role": privileged_users[user_id]["roleName"],
                "title": "Privileged user without MFA registration",
                "description": (
                    "A privileged user does not have MFA registered."
                ),
                "recommendation": (
                    "Review the user's authentication methods and "
                    "verify that appropriate MFA controls are enforced."
                ),
            })

    return findings


def analyze_stale_accounts(users, stale_days=90):
    """Find enabled accounts with no recent sign-in activity."""

    now = datetime.now(timezone.utc)
    findings = []

    for user in users:
        if not user.get("accountEnabled", False):
            continue

        last_sign_in = parse_datetime(user.get("lastSignInDateTime"))

        if not last_sign_in:
            continue

        inactive_days = (now - last_sign_in).days

        if inactive_days >= stale_days:
            findings.append({
                "type": "stale_account",
                "severity": "MEDIUM",
                "userId": user["id"],
                "userPrincipalName": user["userPrincipalName"],
                "title": "Stale user account",
                "description": (
                    f"User has not signed in for approximately "
                    f"{inactive_days} days."
                ),
                "inactive_days": inactive_days,
                "recommendation": (
                    "Review the account and disable it if it is no longer "
                    "required."
                ),
            })

    return findings


def analyze_privileged_access(role_assignments):
    """Identify potentially excessive Global Administrator assignments."""

    global_admins = [
        role
        for role in role_assignments
        if role["roleName"] == "Global Administrator"
    ]

    findings = []

    if len(global_admins) > 3:
        findings.append({
            "type": "excessive_global_admins",
            "severity": "HIGH",
            "title": "High number of Global Administrators",
            "description": (
                f"The tenant has {len(global_admins)} Global Administrators."
            ),
            "count": len(global_admins),
            "recommendation": (
                "Review Global Administrator assignments and reduce "
                "permanent privileged access where appropriate."
            ),
        })

    return findings


def analyze_failed_signins(sign_in_logs, failure_threshold=3):
    """Detect repeated failed sign-ins for a user."""

    failures = {}

    for log in sign_in_logs:
        if log.get("status") != "failure":
            continue

        user_id = log["userId"]

        if user_id not in failures:
            failures[user_id] = {
                "userPrincipalName": log["userPrincipalName"],
                "count": 0,
            }

        failures[user_id]["count"] += 1

    findings = []

    for user_id, data in failures.items():
        if data["count"] >= failure_threshold:
            findings.append({
                "type": "repeated_failed_signins",
                "severity": "MEDIUM",
                "userId": user_id,
                "userPrincipalName": data["userPrincipalName"],
                "title": "Repeated failed sign-ins",
                "description": (
                    f"{data['count']} failed sign-in attempts were "
                    "detected for this user."
                ),
                "failure_count": data["count"],
                "recommendation": (
                    "Investigate the sign-in activity and verify whether "
                    "the attempts are legitimate."
                ),
            })

    return findings


def analyze(users, mfa_registration, role_assignments, sign_in_logs):
    """Run all security-analysis rules."""

    findings = []

    findings.extend(
        analyze_mfa(
            users,
            mfa_registration,
            role_assignments,
        )
    )

    findings.extend(
        analyze_stale_accounts(users)
    )

    findings.extend(
        analyze_privileged_access(role_assignments)
    )

    findings.extend(
        analyze_failed_signins(sign_in_logs)
    )

    return findings
