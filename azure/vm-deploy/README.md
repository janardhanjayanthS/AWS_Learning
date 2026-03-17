# FastAPI on Azure VM

**AWS equivalent:** EC2 instance.

An Azure VM is a full Linux server you manage. You install dependencies, run your app, and keep it alive yourself.

---

## Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed
- An Azure account (free tier works)

---

## Steps

### 1. Login and create a resource group

```bash
az login

az group create --name fastapi-rg --location eastus
```

A **resource group** is just a folder that holds related Azure resources. Similar concept to an AWS region/project grouping.

---

### 2. Create the VM

```bash
az vm create \
  --resource-group fastapi-rg \
  --name fastapi-vm \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys
```

- `Standard_B1s` is the cheapest general-purpose size (~$7/month, free tier eligible).
- Azure auto-generates and saves SSH keys for you.

---

### 3. Open port 8000

```bash
az vm open-port --port 8000 --resource-group fastapi-rg --name fastapi-vm
```

---

### 4. SSH into the VM

```bash
# Get the public IP first
az vm show -d -g fastapi-rg -n fastapi-vm --query publicIps -o tsv

ssh azureuser@<PUBLIC_IP>
```

---

### 5. Install Python and run the app

On the VM:

```bash
sudo apt update && sudo apt install -y python3-pip

pip3 install fastapi "uvicorn[standard]"
```

Copy your `main.py` to the VM (run this locally):

```bash
scp main.py azureuser@<PUBLIC_IP>:~/
```

Then on the VM, start the server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

### 6. Test it

```bash
curl http://<PUBLIC_IP>:8000/
# {"message":"Hello, World!"}
```

---

### 7. Keep it running after disconnect (optional)

```bash
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

Or use `systemd` for a proper service setup.

---

## Cleanup

```bash
az group delete --name fastapi-rg --yes
```

This deletes the VM and everything inside the resource group.
