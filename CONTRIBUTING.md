# Contributing

Thanks for your interest in improving this repository.

## Getting set up

```bash
git clone https://github.com/aidless/flowgrid-aml-retriever.git
cd flowgrid-aml-retriever
```

The offline demo and the unit suite need no third-party packages. `requirements.txt`
lists optional imports (locust, matplotlib), not the default path.

## Verifying your change

```bash
python3 examples/demo_add_search.py
python3 -m unittest discover -s tests
python3 -m pytest tests -q    # optional; CI uses this. pytest.ini points at tests/
```

If the repository has a `Makefile`, `make check` or the closest equivalent runs the same
checks as CI. Please run it before opening a pull request.

## Pull requests

- One logical change per pull request.
- Explain what breaks or is missing without the change.
- State how you verified it, and paste the command output.
- Keep unrelated reformatting out of the diff.

## Security

Do not open a public issue for a security problem. Use the private channel described
in [SECURITY.md](SECURITY.md).

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
