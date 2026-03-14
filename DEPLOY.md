# 🚀 Deploy Guide — Read This First!

## Step 1 — Upload to GitHub

1. Go to https://github.com/new
2. Name: `File-Sharing-Bot`
3. Set to **Public** → Click **Create repository**
4. On the next page, click **uploading an existing file**
5. **Drag and drop ALL files** from this extracted folder
6. Click **Commit changes**

✅ Your repo is now on GitHub!

---

## Step 2A — Deploy on Railway

1. Go to https://railway.app → Sign up with GitHub
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your `File-Sharing-Bot` repo
4. Click **Add Variables** and fill in:

| Variable | Value |
|---|---|
| TG_BOT_TOKEN | From @BotFather |
| APP_ID | From my.telegram.org |
| API_HASH | From my.telegram.org |
| OWNER_ID | Your Telegram user ID |
| CHANNEL_ID | Your DB channel ID |
| DATABASE_URL | Your MongoDB Atlas URL |

5. Click **Deploy** ✅

---

## Step 2B — Deploy on Koyeb

1. Go to https://app.koyeb.com → Sign up with GitHub
2. Click **Create Service** → **GitHub**
3. Select your `File-Sharing-Bot` repo
4. Set **Run command** to: `python3 main.py`
5. Add the same environment variables as above
6. Click **Deploy** ✅

---

## Step 3 — MongoDB Atlas (Free Database)

1. Go to https://mongodb.com/atlas → Sign up free
2. Create a **free M0 cluster**
3. Create a database user (save the password!)
4. Network Access → Add IP → **0.0.0.0/0**
5. Connect → Drivers → Copy the URI
6. Replace `<password>` with your password
7. Paste as `DATABASE_URL` in Railway/Koyeb

---

## Step 4 — Telegram Setup

1. Create a **private channel** → add your bot as admin → copy the channel ID as `CHANNEL_ID`
2. Send any message to the channel, then visit:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
   to find your channel ID (starts with -100)
3. Optional: Create force-sub channel → set `FORCE_SUB_CHANNEL`
4. Optional: Create requests channel → set `REQUEST_CHANNEL_ID`

---

## ✅ Bot is Live! Test with:
- Send /start to your bot
- Send /adminhelp to see all commands
- Forward a file to store it and get a link
