# IMS: Inventory Management System

**You have a spreadsheet. We have opinions about it.**

IMS is a Flask app that turns a boring CSV into something you can actually use: who's low on stock, what's about to expire, revenue by row, and a forecast trained on *your* numbers, not a demo file from 2019.

No login circus. No enterprise sales deck. Upload a file, poke around, train a model when you feel brave.

---

## Why bother?

Because *"I'll check the inventory later"* is how shelves go empty and yogurt goes bad. IMS fixes that.

| Feature | What it actually does |
|---|---|
| 🏠 **Home** | KPIs at a glance + drag-and-drop CSV upload |
| 📦 **Inventory** | Restock nudges and expiry radar |
| 📊 **Analytics** | Revenue by row, top/bottom movers, Chart.js from your real data |
| 🔮 **Forecast** | Three recent stock levels in, one estimate out (scikit-learn) |

Ships locally or on Vercel. Paths adapt automatically when `VERCEL` is set.

---

## Quick start

```bash
git clone https://github.com/jonathanrao99/Inventory-Management-System
cd Inventory-Management-System
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** and feed it `data_set/data.csv`, or your own file with the same column shape.

> **Want forecasting?** Pull in the ML extras:
> ```bash
> pip install -r requirements-ml.txt
> ```

---

## Project map

| Path | Purpose |
|---|---|
| `app.py` | Routes, JSON API, your new best friend |
| `paths.py` | "Am I on a laptop or a postage-stamp server?" |
| `Prediction.py` | Training pipeline for the forecast |
| `public/static/` | CSS + JS (Vercel-friendly `public/`) |
| `templates/` | Jinja2 + `base.html` layout |
| `data_set/data.csv` | Sample loot for testing |

---

## Configuration

Tweak behavior with environment variables. No config files, no drama.

| Variable | Default | What it does |
|---|---|---|
| `APP_NAME` | `IMS` | Short label in the header |
| `APP_FULL_NAME` | `Inventory Management System` | Long name next to the mark |
| `VERCEL` | *(unset)* | Switches data/model scratch space to `/tmp` |

---

## Deploying

**Locally** -- the quick start above is all you need.

**Vercel** -- set the `VERCEL` environment variable in your project settings and push. The app detects it and reroutes file I/O to `/tmp` automatically.

---

## Contributing

PRs and issues are welcome! A few ground rules before you dive in:

1. **Fork + branch from `main`** with a name that hints at the change: `fix/upload-timeout`, `feat/dark-mode`, you get the idea.
2. **Keep scope tight.** One logical change per PR beats a kitchen-sink diff every time.
3. **Smoke-test your touches** -- upload flow, inventory table, analytics chart, forecast + train.
4. **Describe what *and* why** in the PR body. Reviewers should nod, not squint.

Filing a bug? Include your OS, Python version, and what you clicked before the world ended.

---

## License

Released under the **MIT License** -- use it, break it, fix it, ship it. Just keep the copyright notice and license text with your copies.

Full legalese in [LICENSE](LICENSE). Copyright (c) 2024 Jonathan Thota.

---

## Star History

<a href="https://www.star-history.com/?repos=jonathanrao99%2FInventory-Management-System&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=jonathanrao99/Inventory-Management-System&type=date&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=jonathanrao99/Inventory-Management-System&type=date&legend=top-left" />
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=jonathanrao99/Inventory-Management-System&type=date&legend=top-left" />
  </picture>
</a>

---

*Now go count some boxes. Responsibly.*
