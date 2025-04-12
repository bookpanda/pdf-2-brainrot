import time
import boto3
from app.config import settings
from google import genai

textract_client = boto3.client(
    'textract',
    region_name=settings.AWS_REGION,
)
s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    endpoint_url=f"https://s3-{settings.AWS_REGION}.amazonaws.com",
)
gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

def start_text_detection(document):
    response = textract_client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': settings.AWS_BUCKET_NAME,
                'Name': document
            }
        }
    )
    return response['JobId']

def is_job_complete(job_id):
    while True:
        response = textract_client.get_document_text_detection(JobId=job_id)
        status = response['JobStatus']
        print(f"Job status: {status}")
        if status in ['SUCCEEDED', 'FAILED']:
            return response
        time.sleep(5)

def extract_text_from_response(response):
    blocks = response.get("Blocks", [])
    text = ""
    for block in blocks:
        if block["BlockType"] == "LINE":
            text += block["Text"] + "\n"
    return text
def summarize_text(text):
    prompt = "Summarize these sentences into less than one minute of speaking and don't provide any text except the summarisation. "
    prompt += text
    response = gemini_client.models.generate_content(
    model="gemini-2.0-flash-lite", contents=prompt
    )
    return response.text

def get_text_from_pdf(key):
    try:
        job_id = start_text_detection(key)
        response = is_job_complete(job_id)

        if response.get("JobStatus") == "SUCCEEDED":
            text = extract_text_from_response(response)
            text = summarize_text(text)
            return text
        else:
            return "Error"
    except:
        return "Error"