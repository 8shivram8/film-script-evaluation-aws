# 🧪 Postman Testing Instructions: Film Script Evaluation API

This guide walks you through testing the Film Script Evaluation Lambda API using Postman.

---

## 🌐 API Endpoint

---

## 📄 Request Configuration

### 🔸 Method:

`POST`

### 🔸 Headers:

| Key          | Value            |
| ------------ | ---------------- |
| Content-Type | application/json |

### 🔸 Body:

1. Go to **Body → raw**.
2. Select **Text**.
3. Paste your `.fdx` file **content** (not the file, but the raw XML/text content of the file).

---

## ✅ Example Request:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FinalDraft DocumentType="Script" Template="Screenplay" Version="1">
  <Content>
    <Paragraph Type="Scene Heading">INT. COFFEE SHOP - DAY</Paragraph>
    <Paragraph Type="Action">A quiet shop filled with morning light.</Paragraph>
    <Paragraph Type="Character">JOHN</Paragraph>
    <Paragraph Type="Dialogue">Another beautiful morning.</Paragraph>
  </Content>
</FinalDraft>








{
  "status": "success",
  "message": "Script analyzed and feedback stored in S3"
}


```
