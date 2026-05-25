from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer
from .utils import extract_text_from_resume, ai_resume_score, ai_resume_score_all_fields, get_job_recommendations

@api_view(['GET'])
def test_api(request):
    return Response({"message": "API is working"})

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_resume(request):
    try:
        serializer = ResumeSerializer(data=request.data)

        if serializer.is_valid():
            resume = serializer.save()

            file_path = resume.file.path
            text = extract_text_from_resume(file_path)

            if not text:
                raise ValueError("Could not extract text from the uploaded file. Please upload a valid PDF or DOCX.")

            # Get multi-field scores
            ai_result_all_fields = ai_resume_score_all_fields(text)
            
            # Get single field score (for backward compatibility)
            ai_result = ai_resume_score(text)
            
            # Get best fit field's overall score for job recommendations
            best_field = ai_result_all_fields.get("best_fit_fields", [""])[0]
            field_data = ai_result_all_fields.get("field_scores", {})
            best_score = field_data.get(best_field, {}).get("score", ai_result["overall_score"]) if best_field else ai_result["overall_score"]
            
            job_recommendations = get_job_recommendations(text, int(best_score))

            resume.extracted_text = text
            resume.field_scores = ai_result_all_fields
            resume.save()

            return Response({
                "message": "Resume analyzed successfully using AI",
                "resume_id": resume.id,
                "ai_result": ai_result,
                "field_analysis": ai_result_all_fields,
                "job_recommendations": job_recommendations,
                "extracted_text": text[:1500]
            })

        return Response(serializer.errors, status=400)
    except Exception as exc:
        return Response({"error": str(exc)}, status=500)
