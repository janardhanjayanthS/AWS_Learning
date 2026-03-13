"""
HOW TO SET UP SES SMTP CREDENTIALS
====================================

Step 1 — Verify a sender identity
  - Go to AWS Console → SES → Verified Identities → Create Identity
  - Verify either your email address (click link in inbox)
    or your domain (add DNS TXT records AWS gives you)
  - The FROM address in this script must match a verified identity

Step 2 — Create SMTP credentials
  - Go to AWS Console → SES → SMTP Settings
  - Click "Create SMTP Credentials"
  - This creates an IAM user and generates SMTP username + password
  - Copy both — the password is shown ONCE, save it immediately
  - Paste SMTP_USER and SMTP_PASSWORD below

Step 3 — Attach IAM permission (if you get Access Denied)
  - Go to IAM → Users → <your smtp user> → Add permissions
  - Attach policy: AmazonSESFullAccess
  - Or attach a minimal inline policy:
      { "Effect": "Allow", "Action": "ses:SendRawEmail", "Resource": "*" }

Step 4 — Check sandbox mode
  - By default SES is in sandbox: recipient must also be a verified identity
  - To send to anyone: SES → Account Dashboard → Request Production Access

Step 5 — Pick the right SMTP port
  - Port 587 (recommended) — STARTTLS
  - Port 465 — SSL/TLS
  - Port 25 — often blocked by ISPs, avoid it
"""

import smtplib
from email.mime.text import MIMEText

# ── SES SMTP settings ─────────────────────────────────────────────────────────
# SMTP server is region-specific. Change region if your SES is in a different one.
SMTP_SERVER = "email-smtp.us-east-1.amazonaws.com"
SMTP_PORT = 587  # 587 = STARTTLS (recommended)

# From Step 2 above — SES Console → SMTP Settings → Create SMTP Credentials
SMTP_USER = "YOUR_SMTP_USERNAME"
SMTP_PASSWORD = "YOUR_SMTP_PASSWORD"

# ── Email content ─────────────────────────────────────────────────────────────
# FROM must be a verified identity in SES (see Step 1)
FROM_ADDRESS = "janardhanjayanth@bitcot.com"
TO_ADDRESS = "janardhan555jayanth@gmail.com"

msg = MIMEText("Hello, this is a test email from AWS SES.")
msg["Subject"] = "SES Test Email"
msg["From"] = FROM_ADDRESS
msg["To"] = TO_ADDRESS

# ── Send ──────────────────────────────────────────────────────────────────────
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.starttls()
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.sendmail(
        from_addr=msg["From"],
        to_addrs=[msg["To"]],
        msg=msg.as_string(),
    )

print("Email sent successfully.")
