from celery import shared_task

from .models import Resume, ResumeAnalysis
from .services import PDFTextExtractor, ResumeNLPService


@shared_task
def analyze_resume_task(resume_id, job_profile_id):
    resume = Resume.objects.select_related("candidate").get(id=resume_id)
    job_profile = resume.candidate.recruiter.job_profiles.get(id=job_profile_id)
    resume.status = Resume.Status.PROCESSING
    resume.save(update_fields=["status", "updated_at"])
    try:
        text = PDFTextExtractor.extract(resume.file)
        metrics = ResumeNLPService.analyze(text, job_profile.required_skills)
        resume.raw_text = text
        resume.status = Resume.Status.ANALYZED
        resume.save(update_fields=["raw_text", "status", "updated_at"])
        ResumeAnalysis.objects.create(resume=resume, job_profile=job_profile, summary="Analyse automatique basee sur competences et seniorite.", **metrics)
    except Exception as exc:
        resume.status = Resume.Status.FAILED
        resume.error_message = str(exc)
        resume.save(update_fields=["status", "error_message", "updated_at"])
