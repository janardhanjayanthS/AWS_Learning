# RDS (Relational Database Service)

AWS's managed SQL database. You get PostgreSQL, MySQL, MariaDB, Oracle, or SQL Server — AWS handles backups, patching, failover, and replication. You just connect and query.

**When to use it:** Your data is relational, you need complex queries/joins, or you're migrating an existing SQL app.
**When NOT to use it:** Simple key-value lookups, massive scale with predictable access patterns → use DynamoDB instead.

---

## 1. RDS vs. DynamoDB — Which One?

| | RDS | DynamoDB |
|--|-----|----------|
| **Data model** | Tables with rows, columns, foreign keys | Key-value / document |
| **Queries** | Full SQL — joins, aggregations, transactions | Query by PK/SK only |
| **Schema** | Fixed — define columns upfront | Flexible |
| **Scaling** | Vertical (bigger instance) + read replicas | Horizontal, virtually unlimited |
| **Best for** | Complex relational data, existing SQL apps | High-scale, simple access patterns |

**Choose RDS when:**
- Your data has real relationships (users → orders → products)
- You need complex queries, joins, or GROUP BY
- You're migrating an existing MySQL/PostgreSQL app to AWS

**Choose DynamoDB when:**
- Access patterns are simple and known upfront
- You need massive scale with single-digit millisecond latency
- You want fully serverless with zero connection management

---

## 2. Instance Types and Storage

### Instance Types
RDS instances follow the same naming as EC2 — `db.t3.micro`, `db.m6g.large`, etc.

| Class | Use |
|-------|-----|
| `db.t3` / `db.t4g` | Dev/test, low traffic — burstable CPU |
| `db.m6g` / `db.m7g` | General purpose production workloads |
| `db.r6g` / `db.r7g` | Memory-intensive workloads (large datasets in RAM) |

> Start with `db.t3.micro` (free tier eligible). Scale up when you see CPU/memory pressure in CloudWatch.

### Storage Types

| Type | Use |
|------|-----|
| **General Purpose (gp3)** | Default. Good for most workloads. Up to 16,000 IOPS. |
| **Provisioned IOPS (io1/io2)** | High-throughput production DBs. You set exact IOPS. More expensive. |
| **Magnetic** | Legacy. Don't use for new DBs. |

Storage auto-scales — enable **Storage Autoscaling** and RDS will grow the disk automatically when you're running low.

---

## 3. Multi-AZ — High Availability

Multi-AZ keeps a **synchronous standby replica** in a different Availability Zone. If the primary fails, RDS automatically promotes the standby. Your connection string doesn't change.

```mermaid
graph TD
    App["Your App"] -->|reads + writes| Primary["Primary DB\n(AZ: us-east-1a)"]
    Primary -->|synchronous replication| Standby["Standby DB\n(AZ: us-east-1b)"]

    Fail["Primary fails"] -->|automatic failover ~60s| Standby
    Standby -->|promoted to primary| NewPrimary["New Primary"]
```

- **Failover time:** ~60 seconds
- **Standby is NOT readable** — it only exists for failover
- Adds ~2x cost — only enable for production

---

## 4. Read Replicas — Scale Read Traffic

Read replicas are **asynchronous** copies of your DB you can actually query. Use them to offload heavy read traffic from the primary.

```mermaid
graph LR
    App["Your App"]

    App -->|writes| Primary["Primary DB"]
    App -->|reads| RR1["Read Replica 1"]
    App -->|reads| RR2["Read Replica 2"]

    Primary -->|async replication| RR1
    Primary -->|async replication| RR2
```

- Up to **5 read replicas** per primary
- Replicas have their own endpoints — your app must explicitly point read queries at them
- Small replication lag — reads may be slightly stale
- A read replica can be promoted to a standalone DB (useful for migrations)

> Multi-AZ = availability (failover). Read replicas = performance (scale reads). They serve different purposes.

---

## 5. RDS vs. Aurora — When Aurora Is Worth It

Aurora is AWS's own database engine, fully compatible with PostgreSQL and MySQL but rebuilt for the cloud.

| | RDS PostgreSQL/MySQL | Aurora |
|--|---------------------|--------|
| **Storage** | Single AZ storage, replicated to standby | Distributed across 3 AZs, 6 copies automatically |
| **Read replicas** | Up to 5, async | Up to 15, low-lag |
| **Failover** | ~60 seconds | ~30 seconds |
| **Performance** | Standard | Up to 5x MySQL, 3x PostgreSQL |
| **Cost** | Cheaper | ~20% more than RDS |
| **Serverless option** | No | Yes (Aurora Serverless v2) |

**Choose Aurora when:**
- Production workload that needs high availability and fast failover
- You want up to 15 read replicas
- You're considering Aurora Serverless for variable/unpredictable traffic

**Stick with RDS when:**
- Dev/test or small production apps
- Cost is a concern

---

## 6. Automated Backups and Snapshots

### Automated Backups
- Enabled by default — RDS takes a daily backup during a maintenance window
- **Retention:** 1–35 days (default: 7 days)
- Supports **point-in-time recovery** — restore to any second within the retention window
- Stored in S3 (managed by AWS, you don't see the bucket)

### Manual Snapshots
- You trigger these manually or via automation
- **Never expire** — kept until you delete them
- Use for: before a major schema migration, before an upgrade, end-of-month archiving

```mermaid
graph LR
    RDS["RDS Instance"] -->|daily automatic| Backup["Automated Backup\n(retained 7 days)"]
    RDS -->|on-demand| Snapshot["Manual Snapshot\n(kept until deleted)"]

    Backup -->|point-in-time restore| NewDB["Restored DB Instance"]
    Snapshot -->|restore from snapshot| NewDB
```

> Deleting an RDS instance does NOT delete manual snapshots. You delete them separately.

---

## 7. Parameter Groups and Option Groups

### Parameter Groups
A parameter group is a named set of **database engine settings** applied to your RDS instance (equivalent to editing `postgresql.conf` or `my.cnf`).

Common parameters you might tune:
- `max_connections` — max simultaneous DB connections
- `shared_buffers` — PostgreSQL memory for caching
- `slow_query_log` — enable MySQL slow query logging

> RDS comes with a default parameter group you can't edit. Create a custom one and attach it to your instance to make changes. Requires a reboot for some parameters to take effect.

### Option Groups
Option groups add **extra features** to RDS (mostly relevant for Oracle and SQL Server). For PostgreSQL/MySQL, you'll rarely need to touch these.

---

## 8. Connecting from Lambda (VPC + Security Groups)

RDS has no public endpoint by default — it lives in your VPC. For Lambda to reach it, Lambda must also be in the same VPC.

```mermaid
graph LR
    subgraph VPC
        subgraph Private Subnet
            RDS["RDS Instance\n:5432"]
        end
        subgraph Lambda
            Fn["Lambda Function"]
        end
        Fn -->|port 5432| RDS
    end

    Internet -. blocked .-> RDS
```

**Security group setup:**
- Create an SG for Lambda (`sg-lambda`)
- Create an SG for RDS (`sg-rds`)
- In `sg-rds`: allow inbound on port `5432` **from `sg-lambda`** (not from `0.0.0.0/0`)

**The connection exhaustion problem:**
Lambda scales horizontally — 100 concurrent invocations = 100 simultaneous DB connections. PostgreSQL has a low `max_connections` limit. Without pooling, you'll hit it fast.

```python
# psycopg2 — basic connection (fine for EC2, bad for Lambda at scale)
import psycopg2
conn = psycopg2.connect(host="...", dbname="...", user="...", password="...")
```

---

## 9. RDS Proxy — Solve the Lambda Connection Problem

RDS Proxy sits between Lambda and RDS. It **pools and reuses** DB connections — hundreds of Lambda invocations share a small pool of actual DB connections.

```mermaid
graph LR
    L1["Lambda invocation 1"]
    L2["Lambda invocation 2"]
    L3["Lambda invocation 3"]
    LN["Lambda invocation N..."]

    L1 & L2 & L3 & LN -->|connect| Proxy["RDS Proxy\n(connection pool)"]

    Proxy -->|5-10 real connections| RDS["RDS Instance"]
```

- Lambda connects to the **Proxy endpoint**, not directly to RDS
- Proxy multiplexes many Lambda connections into a small pool
- Credentials stored in **Secrets Manager** — Proxy fetches them automatically (no password in your code)
- Adds ~1ms latency — negligible

**Connection string change:**

```python
import psycopg2
import boto3
import json

# Fetch credentials from Secrets Manager
secret = boto3.client("secretsmanager").get_secret_value(SecretId="prod/rds/postgres")
creds = json.loads(secret["SecretString"])

# Connect to Proxy endpoint (not the RDS endpoint directly)
conn = psycopg2.connect(
    host=creds["proxy_host"],   # your-proxy.proxy-xxxx.us-east-1.rds.amazonaws.com
    dbname=creds["dbname"],
    user=creds["username"],
    password=creds["password"],
    sslmode="require"
)
```

> Enable RDS Proxy whenever Lambda connects to RDS. The cost is low and it prevents connection exhaustion under any load.

---

###### Resources
- [RDS Getting Started — AWS Docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.html)
- [RDS Best Practices — AWS Docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
- [RDS Proxy User Guide — AWS Docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
- [Lambda + RDS — AWS Blog](https://aws.amazon.com/blogs/compute/using-amazon-rds-proxy-with-aws-lambda/)
- [Aurora vs RDS — AWS Docs](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.AuroraMySQL.Compare-AuroraMySQL-and-MySQL.html)
