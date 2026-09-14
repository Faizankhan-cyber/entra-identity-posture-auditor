SEVERITY_DEDUCTIONS = {
    "CRITICAL": 25,
    "HIGH": 15,
    "MEDIUM": 8,
    "LOW": 3,
}


def calculate_finding_score(finding):
    """Return the risk deduction for a single finding."""

    severity = finding.get("severity", "LOW")

    return SEVERITY_DEDUCTIONS.get(severity, 0)


def calculate_risk_score(findings):
    """
    Calculate the overall identity security posture score.

    The score starts at 100 and deductions are applied
    based on the severity of detected findings.
    """

    score = 100

    for finding in findings:
        score -= calculate_finding_score(finding)

    return max(score, 0)


def get_posture_status(score):
    """Convert a numeric score into an understandable status."""

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Good"

    if score >= 50:
        return "Needs Improvement"

    return "Poor"


def summarize_findings(findings):
    """Return a count of findings grouped by severity."""

    summary = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for finding in findings:
        severity = finding.get("severity", "LOW")

        if severity in summary:
            summary[severity] += 1

    return summary


def generate_scorecard(findings):
    """Generate the complete security scorecard."""

    score = calculate_risk_score(findings)
    status = get_posture_status(score)
    summary = summarize_findings(findings)

    return {
        "score": score,
        "status": status,
        "total_findings": len(findings),
        "severity_summary": summary,
    }
