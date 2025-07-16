import boto3
import json
import xml.etree.ElementTree as ET
import logging
import os  # For environment variables (best practice for bucket name)

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Adjust log level as needed

# Initialize clients (outside handler for reuse - optimization)
s3 = boto3.client('s3')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# Best practice: Use environment variables for sensitive data (like bucket name)
BUCKET_NAME = os.environ.get('SCRIPT_BUCKET_NAME')
if not BUCKET_NAME:
    raise ValueError("SCRIPT_BUCKET_NAME environment variable not set")


def parse_fdx_to_json(fdx_content):
    # ... (Your existing parse_fdx_to_json function - it's good)
    pass  # Replace with your existing functionimport boto3
import json
import xml.etree.ElementTree as ET
import logging
import os  # For environment variables

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# Best practice: Use environment variables for sensitive data
BUCKET_NAME = os.environ.get('SCRIPT_BUCKET_NAME')
if not BUCKET_NAME:
    raise ValueError("SCRIPT_BUCKET_NAME environment variable not set")


def parse_fdx_to_json(fdx_content):
    """Your existing FDX to JSON parsing function."""
    # ... (Your parsing logic here)
    pass


def analyze_script_with_bedrock(script_text):
    """Calls the Bedrock model to analyze the script."""
    # ... (Your Bedrock interaction logic)
    pass


def lambda_handler(event, context):
    try:
        # 1. Get the .fdx file from API Gateway
        # When using AWS Lambda Proxy, the body is in event['body']
        fdx_content = event['body']
        if not fdx_content:
            raise ValueError("No script content provided in request body")

        logger.info("Successfully retrieved script content from API Gateway")

        # 2. Convert .fdx to JSON
        parsed_script = parse_fdx_to_json(fdx_content)

        # 3. Handle Large Scripts (if needed)
        script_text = json.dumps(parsed_script, indent=2)
        # ... (Your chunking logic, adjusted if needed)

        # 4. Analyze script with Bedrock
        final_result = analyze_script_with_bedrock(script_text)

        # 5. Save feedback to S3
        # Use a filename that includes a timestamp or request ID to avoid collisions
        output_file_name = f'Script_Feedback_{context.aws_request_id}.json'
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=output_file_name,
            Body=json.dumps(final_result, indent=2),
            ContentType='application/json'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Script analysis completed'}, indent=2),
            'headers': {'Content-Type': 'application/json'}
        }

    except ValueError as e:
        logger.error(f"Value Error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        logger.error(f"Error processing script: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Script processing failed'}),
            'headers': {'Content-Type': 'application/json'}
        }

def analyze_script_with_bedrock(script_text):
    """
    Calls the Bedrock model to analyze the script.
    Handles the Bedrock interaction.
    """

    prompt = f"""You are a film script expert. Analyze the following film script and give detailed feedback:

{script_text}

Focus on plot, characters, structure, and originality."""

    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 513,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    try:
        bedrock_response = bedrock_runtime.invoke_model(
            modelId="amazon.titan-text-express-v1",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )
        result = json.loads(bedrock_response['body'].read())
        return result
    except Exception as e:
        logger.error(f"Error calling Bedrock: {e}")
        raise  # Re-raise to be caught in lambda_handler


def lambda_handler(event, context):
    try:
        # 1. Get the .fdx file from S3
        # Assuming the event contains bucket and key (e.g., from S3 trigger or API Gateway)
        # For testing, you might hardcode these or pass them in the event.
        bucket_name = BUCKET_NAME  # Use the environment variable
        fdx_key = event.get('fdx_key', 'sample_script.fdx')  # Get key from event

        logger.info(f"Retrieving script from S3: {bucket_name}/{fdx_key}")
        response = s3.get_object(Bucket=bucket_name, Key=fdx_key)
        fdx_content = response['Body'].read().decode('utf-8')

        # 2. Convert .fdx to JSON
        parsed_script = parse_fdx_to_json(fdx_content)

        # 3. Prepare script text for analysis
        #  ---  HANDLE LARGE SCRIPTS BETTER HERE ---
        script_text = json.dumps(parsed_script, indent=2)
        #  ---  Example: Simple chunking (Illustrative) ---
        #  ---  This is a basic example; you'll need more sophisticated logic ---
        #  ---  to avoid splitting in the middle of dialogue, etc.        ---
        MAX_INPUT_LENGTH = 10000
        if len(script_text) > MAX_INPUT_LENGTH:
            chunks = [script_text[i:i+MAX_INPUT_LENGTH] for i in range(0, len(script_text), MAX_INPUT_LENGTH)]
            all_results = []
            for chunk in chunks:
                chunk_result = analyze_script_with_bedrock(chunk)
                all_results.append(chunk_result)
            #  ---  Combine results here (this is complex and depends on your needs) ---
            final_result = {"analysis": all_results}  # Placeholder
        else:
            final_result = analyze_script_with_bedrock(script_text)


        # 4. Analyze script with Bedrock
        # result = analyze_script_with_bedrock(script_text) # Moved to chunking logic

        # 5. Save feedback to S3
        output_file_name = f'Script_Feedback_{os.path.splitext(fdx_key)[0]}_{context.aws_request_id}.json'
        logger.info(f"Saving feedback to S3: {bucket_name}/{output_file_name}")
        s3.put_object(
            Bucket=bucket_name,
            Key=output_file_name,
            Body=json.dumps(final_result, indent=2),
            ContentType='application/json'
        )

        return {
            'statusCode': 200,
            'body': 'Script analyzed and feedback saved to S3!'
        }

    except Exception as e:
        logger.error(f"Error processing script: {e}")
        return {
            'statusCode': 500,
            'body': f'Error processing script: {e}'
        }