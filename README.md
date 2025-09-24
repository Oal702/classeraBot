# ClasseraBot

## Installing Dependencies

Uses poetry for clean, reproducible installs.

### Prerequisites

Python 3.13+

Poetry installed:

```
curl -sSL https://install.python-poetry.org | python3 -
```

After install, restart your terminal so poetry is on your PATH.

1) Install project deps

run:
```
poetry install
```

This will create/use a virtualenv and install everything from pyproject.toml / poetry.lock.

2) (Playwright only) Install browser engines

If you’re using Playwright:

```
poetry run playwright install
```

Installs Chromium, Firefox, and WebKit so scripts can actually launch a browser.

3) Run the app
```
poetry run python main.py
```

## Overview
classeraBot is a project for a bot designed to save your time by handling repetitive and boring virtual homework tasks on your behalf.