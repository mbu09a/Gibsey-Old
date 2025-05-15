````markdown
# QDPI External-Org Onboarding Kit
**Onboard your lab (e.g., DSPy) to QDPI’s `POST /foreign_shard` endpoint in under 10 minutes.**  
This quick-start guide includes a Postman collection, sandbox credentials, and a Giftware compliance checklist.

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Setup Postman](#step-1-setup-postman)
4. [Step 2: Configure Environment](#step-2-configure-environment)
5. [Step 3: Test `POST /foreign_shard`](#step-3-test-post-foreign_shard)
6. [Step 4: Compliance Checklist](#step-4-compliance-checklist)
7. [Troubleshooting & FAQs](#troubleshooting--faqs)
8. [Next Steps](#next-steps)

---

## Overview
QDPI supports **external labs** exchanging data via a single endpoint: `POST /foreign_shard`. This guide helps you:
- Get sandbox credentials
- Import our Postman collection
- Send your first shard payload
- Adhere to Giftware obligations

Estimated time to complete: **~10 minutes**.

---

## Prerequisites
- **Postman** installed (latest version recommended).
- Basic understanding of JSON and REST APIs.
- Internet connection and permission to send HTTPS requests.

---

## Step 1: Setup Postman

1. **Download the Postman Collection**  
   **Raw JSON** (copy and save as `QDPI.postman_collection.json`):
   ```json
   {
     "info": {
       "name": "QDPI - Foreign Shard API",
       "_postman_id": "YOUR-UNIQUE-ID",
       "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
     },
     "item": [
       {
         "name": "POST /foreign_shard",
         "request": {
           "method": "POST",
           "header": [
             {
               "key": "Content-Type",
               "value": "application/json"
             },
             {
               "key": "Authorization",
               "value": "Bearer {{SANDBOX_API_KEY}}"
             }
           ],
           "url": {
             "raw": "{{BASE_URL}}/foreign_shard",
             "host": ["{{BASE_URL}}"],
             "path": ["foreign_shard"]
           },
           "body": {
             "mode": "raw",
             "raw": "{\n  \"docId\": \"1234-EXAMPLE\",\n  \"payload\": {\n    \"data\": \"Sample shard payload\"\n  }\n}"
           }
         }
       }
     ]
   }
````

2. **Import into Postman**

   * In Postman, click **Import** (top left).
   * Select **File** and choose `QDPI.postman_collection.json`.
   * You should see a new collection named **QDPI - Foreign Shard API**.

---

## Step 2: Configure Environment

1. **Create Postman Environment**

   * Click the gear icon ⚙️ in the top right of Postman.
   * Create a new environment named `QDPI Sandbox`.

2. **Add Variables**

   * `BASE_URL` = `https://sandbox.qdpi.example.com/api/v1`
   * `SANDBOX_API_KEY` = `SBOX-KEY-12345` (example only; use your assigned key)

3. **Save & Activate**

   * In the environment dropdown, select **QDPI Sandbox** to make these vars active.

---

## Step 3: Test `POST /foreign_shard`

1. In the **QDPI - Foreign Shard API** collection, open the request **POST /foreign\_shard**.
2. Ensure the environment is set to **QDPI Sandbox**.
3. **Send the Request**

   * Verify **Authorization** → `Bearer {{SANDBOX_API_KEY}}`.
   * Click **Send**.
4. **Check the Response**

   * A successful response typically looks like:

     ```json
     {
       "status": "ok",
       "message": "Shard received",
       "docId": "1234-EXAMPLE"
     }
     ```
   * If you see an error (401, 403, etc.), double-check your environment variables or contact QDPI support.

---

## Step 4: Compliance Checklist

QDPI requires compliance with **Giftware** licensing and usage obligations. Before sharing data, verify the following:

1. **Attribution**:

   * Acknowledge all shared code or documentation originates under the QDPI Giftware terms.
   * Retain QDPI’s license info in derivative works.

2. **No Warranty**:

   * Understand that Giftware is provided “as-is” with no warranties or liabilities.

3. **Open-Source Audit**:

   * If you embed QDPI-provided code in your lab’s workflows or repos, maintain a copy of the Giftware License file or link to it in your open-source acknowledgments.

4. **Redistribution**:

   * Any re-distribution of QDPI artifacts must also carry the Giftware disclaimers.

5. **Security**:

   * Protect sandbox keys from public exposure.
   * Comply with QDPI’s data protection policies (details in the **Security** section of QDPI docs).

---

## Troubleshooting & FAQs

1. **Getting 401 Unauthorized**

   * Confirm your `SANDBOX_API_KEY` is correct and not expired.
   * Check for typos in your environment variables.

2. **Timeout / 500 Server Error**

   * Try again after a few seconds.
   * If persistent, contact QDPI support with logs or Postman console output.

3. **Sandbox Key Rotation**

   * If your key is no longer valid, request a fresh **Sandbox Key** from QDPI DevOps.

---

## Next Steps

* **Integrate**: Start integrating `POST /foreign_shard` calls in your codebase once you confirm a successful test in Postman.
* **Production Transition**: Contact QDPI for a production key and endpoint when you are ready to go live.
* **Monitoring**: Implement logs and metrics around your shard submission processes for traceability.

---

**Questions or Issues?**
Contact the QDPI Onboarding Team:
**Email**: [onboarding@qdpi.example.com](mailto:onboarding@qdpi.example.com)
**Slack**: `#qdpi-integration-help`

Happy integrating!

```
```