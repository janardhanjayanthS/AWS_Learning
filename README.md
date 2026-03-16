# AWS Learning — Backend Developer

A structured AWS learning repo covering core services from fundamentals to production-ready applications, built around the perspective of a backend developer.

---

## Structure

```
.
├── plan/
│   └── 0_study_plan.MD        # Full learning roadmap with resources
├── services/                  # Notes and code per AWS service
│   ├── 01_IAM/
│   ├── 02_EC2/
│   ├── 03_S3/
│   ├── 04_Cloudwatch/
│   ├── 05_Cloudfront/
│   ├── 06_Route53/
│   ├── 07_Lambda/
│   ├── 08_API_Gateway/
│   ├── 09_SAM/
│   ├── 10_Cloudformation/
│   ├── 11_ECS/
│   ├── 12_EKS/
│   ├── 13_DynamoDB/
│   ├── 14_DocumentDB/
│   ├── 15_LoadBalancers/
│   ├── 16_RDS/
│   ├── 17_Opensearch/
│   ├── 18_Elasticache_and_redis/
│   ├── 19_Secretsmanager/
│   ├── 20_Cognito/
│   ├── 21_SimpleQueueService/
│   ├── 22_SimpleNotificationService/
│   ├── 23_SimpleEmailService/
│   ├── 24_VPC/
│   ├── 25_CertificateManager/
│   ├── 26_EventBridge/
│   ├── 27_StepFunctions/
│   ├── 28_Kinesis/
│   └── 29_XRay/
└── project/                   # Capstone project (Multi-Tenant RAG API)
```

---

## Learning Roadmap

Covered in 10 phases — see [`plan/0_study_plan.MD`](plan/0_study_plan.MD) for the full breakdown with resources.

| Phase | Topic |
|-------|-------|
| 1 | AWS Fundamentals & IAM |
| 2 | Core Compute & Storage |
| 3 | Serverless Core & Dev Tooling |
| 4 | Containers |
| 5 | Data & Caching |
| 6 | Networking |
| 7 | Security & Secrets |
| 8 | Events & Orchestration |
| 9 | Observability & Communication |
| 10 | Capstone Project |

---

## Capstone Project - Deployment In-progress

A serverless **Multi-Tenant RAG API** built with FastAPI, PostgreSQL (pgvector), and deployed to AWS Lambda via SAM.

Users register, upload documents (PDFs or web pages), and query their content via an LLM. All data is isolated per user — embeddings, cache, and retrieval are scoped to the authenticated user.

See [`project/README.md`](project/README.md) for full architecture, API docs, and setup instructions.

**Stack:** FastAPI · PostgreSQL · PGVector · LangChain · OpenAI · AWS Lambda · SAM
