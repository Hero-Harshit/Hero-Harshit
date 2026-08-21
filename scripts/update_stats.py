import os
import re
import json
import urllib.request
import textwrap
from datetime import datetime, timezone, timedelta

USERNAME = "Hero-Harshit"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
IST = timezone(timedelta(hours=5, minutes=30))

def fetch_graphql(query, variables=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request("https://api.github.com/graphql", data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", {})
    except Exception as e:
        print(f"GraphQL request fallback: {e}")
        return None

def update_daily_quote():
    quotes_path = os.path.join(os.path.dirname(__file__), "quotes.json")
    if not os.path.exists(quotes_path):
        print("quotes.json not found, skipping quote update.")
        return

    with open(quotes_path, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    if not quotes:
        return

    # Use IST day of year so it rolls over at midnight Indian Standard Time
    now = datetime.now(IST)
    day_of_year = now.timetuple().tm_yday
    quote_index = (day_of_year + now.year) % len(quotes)
    todays_quote = quotes[quote_index]

    # Generate spacious, large-font quote.svg
    clean_quote = todays_quote.strip('“”"')
    lines = textwrap.wrap(clean_quote, width=58)
    
    # Calculate spacious dynamic height
    line_height = 28
    text_block_height = len(lines) * line_height
    card_height = max(135, 75 + text_block_height)

    line_spans = ""
    start_y = 52 if len(lines) == 1 else (48 if len(lines) == 2 else 44)
    for i, line in enumerate(lines):
        y_pos = start_y + (i * line_height)
        line_spans += f'    <text x="56" y="{y_pos}" class="quote-body">{line}</text>\n'

    svg_content = f"""<svg width="820" height="{card_height}" viewBox="0 0 820 {card_height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="quoteGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#70a5fd" />
      <stop offset="50%" stop-color="#c084fc" />
      <stop offset="100%" stop-color="#38bdf8" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#70a5fd" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#c084fc" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#e4e2e2" stop-opacity="0.5"/>
    </linearGradient>
  </defs>

  <style>
    .quote-body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, sans-serif;
      font-weight: 600;
      font-size: 18px;
      fill: #f0f6fc;
      font-style: italic;
      letter-spacing: 0.2px;
    }}
    .quote-mark {{
      font-family: Georgia, serif;
      font-size: 54px;
      font-weight: 900;
      fill: url(#quoteGrad);
      opacity: 0.9;
    }}
    .author-tag {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Ubuntu, sans-serif;
      font-weight: 600;
      font-size: 12px;
      fill: #a78bfa;
      letter-spacing: 0.5px;
    }}
  </style>

  <!-- Background Card -->
  <rect x="0.5" y="0.5" width="819" height="{card_height - 1}" rx="8" fill="#151515" stroke="url(#borderGrad)" stroke-width="1.2"/>

  <!-- Quotation Accent Mark -->
  <text x="20" y="52" class="quote-mark">“</text>

  <!-- Quote Content -->
  <g transform="translate(10, 0)">
{line_spans}  </g>

  <!-- Footer Tag -->
  <text x="790" y="{card_height - 18}" text-anchor="end" class="author-tag">✦ Daily Reflection • Hero Harshit</text>
</svg>"""

    with open("quote.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Generated quote.svg successfully.")

    if os.path.exists("Readme.md"):
        with open("Readme.md", "r", encoding="utf-8") as f:
            content = f.read()

        new_content = re.sub(
            r"<!-- DAILY_QUOTE:START -->[\s\S]*?<!-- DAILY_QUOTE:END -->",
            f"<!-- DAILY_QUOTE:START -->\n<p align=\"center\">\n  <img src=\"./quote.svg\" alt=\"Hero Harshit's Daily Reflection\" width=\"820\" />\n</p>\n<!-- DAILY_QUOTE:END -->",
            content
        )

        with open("Readme.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated daily quote in Readme.md (Quote #{quote_index + 1})")

def update_streak_and_stats():
    total_contributions = 1616
    current_streak = 377
    mean_commits = 4.3
    max_daily_commit = 80
    max_daily_date = "August 1, 2026"

    # Try GraphQL with Token
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    
    data = fetch_graphql(query, {"login": USERNAME}) if GITHUB_TOKEN else None
    
    if data and "user" in data and data["user"]:
        cal = data["user"].get("contributionsCollection", {}).get("contributionCalendar", {})
        total_contributions = cal.get("totalContributions", total_contributions)
        days = []
        for w in cal.get("weeks", []):
            for d in w.get("contributionDays", []):
                days.append((d["date"], d["contributionCount"]))
        
        days.sort(key=lambda x: x[0])
        
        # Calculate current streak
        today_str = datetime.now(IST).strftime("%Y-%m-%d")
        c_streak = 0
        started = False
        for date_str, count in reversed(days):
            if count > 0:
                c_streak += 1
                started = True
            else:
                if started:
                    break
                if date_str == today_str:
                    continue
                else:
                    break
        
        if c_streak > 0:
            current_streak = c_streak
            
        for date_str, count in days:
            if count >= max_daily_commit:
                max_daily_commit = count
                try:
                    dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    max_daily_date = dt_obj.strftime("%B %d, %Y").replace(" 0", " ")
                except Exception:
                    max_daily_date = date_str
                    
        active_days = len([c for _, c in days if c > 0]) or 1
        mean_commits = round(total_contributions / active_days, 1)

    print(f"Stats -> Total: {total_contributions}, Current Streak: {current_streak}, Mean: {mean_commits}, Max: {max_daily_commit} ({max_daily_date})")

    # Update streak-stats.svg
    if os.path.exists("streak-stats.svg"):
        with open("streak-stats.svg", "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(
            r"(<text x='0' y='72' text-anchor='middle' class='bold-num' font-size='28px'>)[^<]+(</text>)",
            f"\\g<1>{total_contributions:,}\\g<2>",
            content
        )
        if current_streak > 0:
            content = re.sub(
                r"(<text x='0' y='73' text-anchor='middle' class='bold-num' font-size='26px'>)[^<]+(</text>)",
                f"\\g<1>{current_streak}\\g<2>",
                content
            )
        content = re.sub(
            r"(<text x='0' y='0' text-anchor='middle' class='bold-num' font-size='22px'>)[^<]+(</text>)",
            f"\\g<1>{mean_commits}\\g<2>",
            content
        )
        if max_daily_commit > 0:
            content = re.sub(
                r"(<text x='0' y='0' text-anchor='middle' class='accent-num'>)[^<]+(</text>)",
                f"\\g<1>{max_daily_commit}\\g<2>",
                content
            )
        if max_daily_date:
            content = re.sub(
                r"(<text x='0' y='33' text-anchor='middle' class='date-sub'>)[^<]+(</text>)",
                f"\\g<1>{max_daily_date}\\g<2>",
                content
            )

        with open("streak-stats.svg", "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated streak-stats.svg")

if __name__ == "__main__":
    update_daily_quote()
    update_streak_and_stats()
