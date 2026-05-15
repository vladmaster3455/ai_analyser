from apps.resumes.services import ResumeNLPService


def test_resume_scoring_detects_required_skills():
    result = ResumeNLPService.analyze("Developpeur Python Django avec 5 ans experience Docker", ["Python", "Django", "Kubernetes"])
    assert result["score"] > 50
    assert "Python" in result["matched_skills"]
    assert "Kubernetes" in result["missing_skills"]
