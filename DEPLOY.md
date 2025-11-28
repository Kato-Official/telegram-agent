# Telegram Agent - Deployment Guide

This guide explains how to deploy the Telegram Agent to your server (`api.openfinance.cloud`) using PM2 and Caddy.

## 1. Local Preparation (Do this ONCE on your Mac)

1. **Initialize Git and Push**:

    ```bash
    cd /Users/Kato/Desktop/telegram-agent
    git add .
    git commit -m "Update with Dashboard and Auth"
    git push origin main
    ```

## 2. Server Deployment (Do this on your Server)

SSH into your server:

```bash
ssh amatocapitallimited@api.openfinance.cloud
```

### Step A: Update Code

```bash
cd ~/telegram-agent
git pull
```

### Step B: Update Dependencies

```bash
./.venv/bin/pip install -r requirements.txt
```

### Step C: Upload Secrets (Critical)

Since we don't commit secrets to GitHub, you need to upload your Firebase key and Session file from your Mac.

**Run this ON YOUR MAC terminal:**

```bash
# Upload Session File
scp /Users/Kato/Desktop/telegram-agent/circle_dxb_session.session amatocapitallimited@api.openfinance.cloud:~/telegram-agent/

# Upload Secrets Folder
scp -r /Users/Kato/Desktop/telegram-agent/secrets amatocapitallimited@api.openfinance.cloud:~/telegram-agent/
```

### Step D: Restart App

```bash
pm2 restart telegram-agent
```

### Step E: Verify

Visit **[https://telegram.openfinance.cloud/dashboard](https://telegram.openfinance.cloud/dashboard)**
