# Contributing

Thanks for considering a contribution! This is a small learning/portfolio project,
so contributions of any size are welcome — typo fixes, new features, bug reports.

## Getting set up

1. Fork the repo and clone your fork
2. Create a virtual environment and install dev dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # venv\Scripts\activate on Windows
   pip install -r requirements-dev.txt
   ```
3. Copy `.env.example` to `.env` and fill in your own bot token and API key
   (see the README for how to get them — both are free)

## Before opening a pull request

```bash
ruff check .      # lint
pytest            # run the test suite
```

## Ideas for contributions

- Additional language support for bot messages
- Hourly forecast charts
- Scheduled weather alerts
- Docker support
- More test coverage

Feel free to open an issue first to discuss larger changes.
