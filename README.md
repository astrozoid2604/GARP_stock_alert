# 📈 Daily Alert System for `Boosted Balanced GARP` Portfolio

This repository contains an automated, valuation-driven stock alert system for the **Boosted Balanced GARP** portfolio — a curated set of high-growth, fundamentally strong stocks. It runs daily using GitHub Actions and delivers personalized alerts based on forward P/E, PEG, and P/S ratio thresholds.

---

## ⚠️ DISCLAIMER:
This script is part of a personal project and is NOT intended as financial advice.
All valuation logic and portfolio allocations are for educational use only.
Please do your own research before acting on any investment decision.

---

## Repository Layout

```bash
GARP_stock_alert/
├── .github/
│   └── workflows/
│       └── daily-alert.yml         ← GitHub Actions config (runs every 12PM SGT)
├── .env.template                   ← Local secrets template (user fills this manually)
├── .gitignore                      ← Ensures `.env` is not committed
├── alert.py                        ← Main alert script
└── requirements.txt                ← Python dependencies
```

---

## 🔧 Tech Stack

| Component    | Purpose                                 |
|--------------|------------------------------------------|
| **GitHub Actions** | Schedules and runs the workflow daily at 12:00PM Singapore Time (UTC+8) |
| **SendGrid API**   | Sends daily email notification with buy/hold signals |

---

## 📋 Decision Logic

Each stock is scored based on 3 valuation metrics:

| Metric            | Weight |
|-------------------|--------|
| PEG Ratio         | 45%    |
| Forward P/E Ratio | 35%    |
| Price/Sales Ratio | 20%    |

### Decision Rule

| Score Range | Decision      | Action                      |
|-------------|---------------|-----------------------------|
| ≥ 0.75      | Strong Buy     | Deploy full monthly capital |
| 0.55–0.74   | Partial Buy    | Deploy half capital         |
| < 0.55      | Hold           | Save cash for future entry  |

---

## 📊 Alert Format

Each daily email and WhatsApp message includes a 12×9 table sorted by portfolio allocation, with:

- Current PE RATIO (FWD)
- Current PEG RATIO
- Current P/S RATIO
- Trigger upper limits for each metric
- Weighted score
- Final decision per stock

---

## 🕒 Schedule

This system runs **once per day** at **12:00PM Singapore Time (UTC+8)** via GitHub Actions.

---

## 📬 Notification Channels

- **Email:** Sent via SendGrid to your inbox

---

## 🔐 Secrets Configuration

Before deploying, configure these GitHub Secrets in your repository:

| Secret Name          | Description                         |
|----------------------|-------------------------------------|
| `SENDGRID_API_KEY`    | SendGrid API key                    |
| `ALERT_EMAIL_FROM`    | Your email address for alerts       |
| `ALERT_EMAIL_TO`      | Your email address for alerts       |

---

## 🚀 Quick Start

1. Fork or clone this repo
2. Add your API keys and contact info under GitHub Secrets
3. Push to `main` branch
4. Daily alerts will start automatically at 12PM SGT

---

## 📎 License

MIT License. Feel free to fork and customize this system.

---

## 🤝 Acknowledgments

- [SendGrid](https://sendgrid.com)
