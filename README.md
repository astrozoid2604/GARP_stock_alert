# 📈 Boosted Balanced GARP Daily Alert System

This repository contains an automated, valuation-driven stock alert system for the **Boosted Balanced GARP** portfolio — a curated set of high-growth, fundamentally strong stocks. It runs daily using GitHub Actions and delivers personalized alerts based on forward P/E, PEG, and P/S ratio thresholds.

---

## 🔧 Tech Stack

| Component    | Purpose                                 |
|--------------|------------------------------------------|
| **GitHub Actions** | Schedules and runs the workflow daily at 12:00PM Singapore Time (UTC+8) |
| **Finnhub API**    | Retrieves valuation metrics for 11 selected stocks |
| **SendGrid API**   | Sends daily email notification with buy/hold signals |
| **Twilio API**     | Sends daily WhatsApp alert message to user |

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
- **WhatsApp:** Message sent via Twilio to your preferred number

---

## 🔐 Secrets Configuration

Before deploying, configure these GitHub Secrets in your repository:

| Secret Name          | Description                         |
|----------------------|-------------------------------------|
| `FINNHUB_API_KEY`     | Finnhub API key                     |
| `SENDGRID_API_KEY`    | SendGrid API key                    |
| `TWILIO_ACCOUNT_SID`  | Twilio account SID                  |
| `TWILIO_AUTH_TOKEN`   | Twilio auth token                   |
| `TWILIO_FROM`         | Twilio WhatsApp sender (sandbox or verified) |
| `WHATSAPP_TO`         | Your WhatsApp number (`whatsapp:+65XXXXXXX`) |
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

- [Finnhub.io](https://finnhub.io)
- [SendGrid](https://sendgrid.com)
- [Twilio WhatsApp API](https://www.twilio.com/whatsapp)
