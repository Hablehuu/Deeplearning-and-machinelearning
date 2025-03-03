from google.api_core.client_options import ClientOptions
from google.cloud import documentai, translate

import os
#this code is from the Google tutorial for the OCR AI
#https://codelabs.developers.google.com/codelabs/docai-ocr-python
PROJECT_ID = "" #your google cloud project id
LOCATION = "eu"  # Format is 'us' or 'eu'
PROCESSOR_ID = ""  # Create processor in Cloud Console
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./key.json" #the key file given by google cloud
PARENT = f"projects/{PROJECT_ID}"
# The local file in your current working directory
FILE_PATH = "handwriting.jpg"
# Refer to https://cloud.google.com/document-ai/docs/file-types
# for supported file types
MIME_TYPE = "image/jpeg"

# Instantiates a client
docai_client = documentai.DocumentProcessorServiceClient(
    client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
)

# The full resource name of the processor, e.g.:
# projects/project-id/locations/location/processor/processor-id
# You must create new processors in the Cloud Console first
RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

# Read the file into memory
with open(FILE_PATH, "rb") as image:
    image_content = image.read()

# Load Binary Data into Document AI RawDocument Object
raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)

# Configure the process request
request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

# Use the Document AI client to process the sample form
result = docai_client.process_document(request=request)

document_object = result.document

client = translate.TranslationServiceClient()

response = client.translate_text(
    parent=PARENT,
    contents=[document_object.text],
    target_language_code="fr",
    )



print("Document processing complete.")
print(f"Text: {response.translations[0]}")
