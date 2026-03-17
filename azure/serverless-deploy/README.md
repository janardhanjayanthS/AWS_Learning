# FastAPI on Azure Functions (Serverless)

**AWS equivalent:** AWS Lambda + API Gateway, but combined into one service.

Azure Functions runs your code on-demand. You don't manage any server. You're billed only when requests come in (with a generous free tier: 1 million requests/month free).

---

## How it works

Azure Functions supports ASGI apps (like FastAPI) directly via `AsgiFunctionApp`. Your FastAPI app is wrapped and served by the Functions runtime — no Uvicorn needed.

```
HTTP Request → Azure Functions → your FastAPI app → response
```

---

## Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Azure Functions Core Tools v4](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- Python 3.11+

Install Core Tools (Windows):
```bash
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

---

## Run locally first

```bash
pip install -r requirements.txt

func start
```

Visit `http://localhost:7071/` — you should see `{"message":"Hello, World!"}`.

---

## Deploy to Azure

### 1. Login and create resources

```bash
az login

az group create --name fastapi-serverless-rg --location eastus

az storage account create \
  --name fastapistorageacct \
  --location eastus \
  --resource-group fastapi-serverless-rg \
  --sku Standard_LRS
```

A **storage account** is required by Azure Functions to store logs and state. It's cheap (a few cents/month).

### 2. Create the Function App

```bash
az functionapp create \
  --resource-group fastapi-serverless-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name my-fastapi-func \
  --storage-account fastapistorageacct \
  --os-type linux
```

`--consumption-plan-location` means serverless (pay-per-use). No always-on server.

### 3. Deploy your code

```bash
func azure functionapp publish my-fastapi-func
```

### 4. Test it

```bash
az functionapp show \
  --name my-fastapi-func \
  --resource-group fastapi-serverless-rg \
  --query defaultHostName -o tsv
```

Then:
```bash
curl https://<defaultHostName>/
# {"message":"Hello, World!"}
```

---

## Cleanup

```bash
az group delete --name fastapi-serverless-rg --yes
```

---

## VM vs Serverless — quick comparison

| | VM | Azure Functions |
|---|---|---|
| Cost | ~$7/month always | Free up to 1M req/month |
| Cold start | None | ~1-2s on first request |
| You manage | OS, Python, process | Nothing |
| Best for | Long-running apps | Infrequent / event-driven requests |
