# 🎬 Film Script Evaluation using AWS (Lambda + S3 + Bedrock)

This project evaluates `.fdx` (Final Draft) film scripts using AWS services in a serverless architecture.

## 🚀 Objective

Automatically evaluate film scripts using a Bedrock model and return expert feedback.

---

## 🛠️ Technologies & Services Used

- **Amazon S3** – Store uploaded scripts and feedback.
- **AWS Lambda** – Convert `.fdx` to JSON and analyze using Bedrock.
- **Amazon Bedrock** – Used `amazon.titan-text-express-v1` model.
- **API Gateway** – Expose HTTP endpoint to trigger Lambda.
- **IAM** – Custom policy to allow S3 + Bedrock access.

---

## 🔄 Workflow

1. Upload `.fdx` file to API Gateway via Postman.
2. Lambda function:
   - Converts to JSON
   - Sends to Bedrock
   - Stores result in S3
3. Check output JSON in your S3 bucket.

---

## 🧪 Testing via Postman

**Endpoint:**
---------------------------------------------------------------------------------------------
