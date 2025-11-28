# Telegram Agent - Deployment Guide

This guide explains how to deploy the Telegram Agent to your server (`api.openfinance.cloud`) using PM2 and Caddy.

## 1. Local Preparation (Do this ONCE on your Mac)

1. **Initialize Git and Push**:

    ```bash
    cd /Users/Kato/Desktop/telegram-agent
    git init
    git add .
    git commit -m "Initial commit for deployment"
    git branch -M main
    git remote add origin https://github.com/Kato-Official/telegram-agent.git
    git push -u origin main
    ```

## 2. Server Deployment (Do this on your Server)

SSH into your server:

```bash
ssh amatocapitallimited@api.openfinance.cloud
```

### Step A: Clone and Setup

Run these commands one by one:

```bash
# 1. Clone the repository
git clone https://github.com/Kato-Official/telegram-agent.git
cd telegram-agent

# 2. Create Virtual Environment
python3 -m venv .venv

# 3. Install Dependencies
./.venv/bin/pip install -r requirements.txt

# 4. Setup Configuration
cp .env.example .env
# (Optional) Edit .env if you need to change keys: nano .env
```

### Step B: Authentication (Critical)

You need to generate the session file on the server.
**Option 1 (Recommended): Upload from Mac**
If you have already logged in locally, upload your session file:

```bash
# Run this ON YOUR MAC terminal (not the server)
scp /Users/Kato/Desktop/telegram-agent/circle_dxb_session.session amatocapitallimited@api.openfinance.cloud:~/telegram-agent/
```

**Option 2: Login on Server**
If you haven't logged in locally, run this on the server and follow the prompts:

```bash
./.venv/bin/python main.py
```

### Step C: Start with PM2

We use the included `ecosystem.config.js` for easy management.

```bash
pm2 start ecosystem.config.js
pm2 save
```

Your app is now running on **port 8001**.

### Step D: Configure Caddy (Domain)

Add the following block to your Caddyfile to expose the app at `telegram.openfinance.cloud`.

1. Edit Caddyfile:

    ```bash
    sudo nano /etc/caddy/Caddyfile
    ```

2. Add this to the end of the file:

    ```caddy
    telegram.openfinance.cloud {
        reverse_proxy localhost:8001
    }
    ```

3. Reload Caddy:

    ```bash
    sudo systemctl reload caddy
    ```

## 3. Verification

Visit **[https://telegram.openfinance.cloud/docs](https://telegram.openfinance.cloud/docs)** to see your API live!

## 4. Updates

To update the code later:

```bash
cd ~/telegram-agent
git pull
pm2 restart telegram-agent
```
