# boosted_garp_alert.py
import yfinance as yf
import datetime
import os
import sendgrid
from sendgrid.helpers.mail import Mail

# === CONFIGURATION ===
stocks = {
    'NVDA': {'weight': 14, 'fpe_limit': 30, 'peg_limit': 0.7, 'ps_limit': 22},
    'META': {'weight': 14, 'fpe_limit': 24, 'peg_limit': 0.7, 'ps_limit': 9.5},
    'AMZN': {'weight': 11, 'fpe_limit': 30, 'peg_limit': 0.6, 'ps_limit': 3.3},
    'MELI': {'weight': 10, 'fpe_limit': 40, 'peg_limit': 0.8, 'ps_limit': 5.0},
    'MSFT': {'weight': 10, 'fpe_limit': 24, 'peg_limit': 2.5, 'ps_limit': 12},
    'ANET': {'weight': 9,  'fpe_limit': 28, 'peg_limit': 1.2, 'ps_limit': 14},
    'AAPL': {'weight': 8,  'fpe_limit': 26, 'peg_limit': 2.0, 'ps_limit': 7},
    'AXON': {'weight': 7,  'fpe_limit': 70, 'peg_limit': 1.5, 'ps_limit': 18},
    'AVGO': {'weight': 6,  'fpe_limit': 25, 'peg_limit': 2.0, 'ps_limit': 18},
    'NFLX': {'weight': 6,  'fpe_limit': 40, 'peg_limit': 1.1, 'ps_limit': 12},
    'LLY':  {'weight': 5,  'fpe_limit': 35, 'peg_limit': 0.7, 'ps_limit': 13}
}

# === HELPER FUNCTIONS ===
def get_financials(ticker):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        fpe = info.get('forwardPE') or float('inf')
        peg = info.get('trailingPegRatio') or float('inf')
        ps = info.get('priceToSalesTrailing12Months') or float('inf')
        if any(val == float('inf') for val in [fpe, peg, ps]):
            print(f"[Warning] Missing financial data for {ticker}")
        return {'fpe': fpe, 'peg': peg, 'ps': ps}
    except:
        print(f"[Error] Failed to fetch financials for {ticker}")
        return {'fpe': float('inf'), 'peg': float('inf'), 'ps': float('inf')}

def evaluate_entry(fpe, peg, ps, limits):
    score = 0
    if peg <= limits['peg_limit']: score += 45
    if fpe <= limits['fpe_limit']: score += 35
    if ps <= limits['ps_limit']: score += 20

    if score >= 75:
        decision = 'Strong Buy'
    elif score >= 55:
        decision = 'Partial Buy'
    else:
        decision = 'Hold'

    return score, decision

def generate_email_content(results):
    header = ['Stock Ticker', 'Current PE RATIO (FWD)', 'Current PEG RATIO', 'Current P/S RATIO',
              'UpperLimit PE RATIO (FWD)', 'UpperLimit PEG RATIO', 'UpperLimit P/S RATIO',
              'Weighted Score', 'Decision']
    rows = [header]

    for ticker, data in results:
        row = [
            ticker,
            f"{data['fpe']:.2f}",
            f"{data['peg']:.2f}",
            f"{data['ps']:.2f}",
            f"{data['limits']['fpe_limit']}",
            f"{data['limits']['peg_limit']}",
            f"{data['limits']['ps_limit']}",
            f"{data['score']}",
            data['decision']
        ]
        rows.append(row)

    table_html = '<table border="1" cellpadding="4">' + \
        '<tr>' + ''.join(f'<th>{col}</th>' for col in rows[0]) + '</tr>'
    for row in rows[1:]:
        table_html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    table_html += '</table>'
    return table_html

def send_email(subject, html_content):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ['SENDGRID_API_KEY'])
    email = Mail(
        from_email='alert@portfolio.com',
        to_emails='e0950510@u.nus.edu',
        subject=subject,
        html_content=html_content
    )
    sg.send(email)

# === MAIN EXECUTION ===
def main():
    results = []
    for ticker, limits in sorted(stocks.items(), key=lambda x: -x[1]['weight']):
        metrics = get_financials(ticker)
        score, decision = evaluate_entry(metrics['fpe'], metrics['peg'], metrics['ps'], limits)
        results.append((ticker, {
            'fpe': metrics['fpe'],
            'peg': metrics['peg'],
            'ps': metrics['ps'],
            'limits': limits,
            'score': score,
            'decision': decision
        }))

    date_str = datetime.datetime.now().strftime('%Y:%b:%d')
    any_buy = any(data['decision'] in ['Strong Buy', 'Partial Buy'] for _, data in results)
    subject_prefix = '[{} {}] Portfolio Notification'.format(date_str, 'Buy' if any_buy else 'Hold')
    html_body = generate_email_content(results)
    send_email(subject_prefix, html_body)

if __name__ == '__main__':
    main()
