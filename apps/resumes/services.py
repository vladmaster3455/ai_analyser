import re

from PyPDF2 import PdfReader


class PDFTextExtractor:
    @staticmethod
    def extract(file_obj):
        reader = PdfReader(file_obj)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()


class ResumeNLPService:
    @staticmethod
    def normalize(text):
        return re.sub(r"\s+", " ", text.lower()).strip()

    @classmethod
    def analyze(cls, text, required_skills):
        normalized = cls.normalize(text)
        matched = [skill for skill in required_skills if skill.lower() in normalized]
        missing = [skill for skill in required_skills if skill not in matched]
        years = cls.estimate_years(normalized)
        skill_score = len(matched) / max(len(required_skills), 1)
        seniority_score = min(years / 8, 1)
        score = round((skill_score * 0.7 + seniority_score * 0.3) * 100, 2)
        return {"score": score, "matched_skills": matched, "missing_skills": missing, "seniority_years": years}

    @staticmethod
    def estimate_years(text):
        values = [int(match) for match in re.findall(r"(\d+)\s*(?:ans|annees|years)", text)]
        return float(max(values) if values else 0)
