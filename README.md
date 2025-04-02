![beacon](https://github.com/user-attachments/assets/c5fd6745-74e6-4cd7-9c93-c735ee58e5b2)


# beacon 📚

[![Release](https://img.shields.io/github/v/release/proteusiq/beacon)](https://img.shields.io/github/v/release/proteusiq/beacon)
[![Build status](https://img.shields.io/github/actions/workflow/status/proteusiq/beacon/main.yml?branch=main)](https://github.com/proteusiq/beacon/actions/workflows/main.yml?query=branch%3Amain)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

beacon is a semantic book recommendation system that helps you find your next great read based on natural language descriptions.

## features

- natural language book search
- semantic similarity matching
- fast vector database backend
- curated book collection from goodreads

## installation

```bash
uv pip install git+https://github.com/proteusiq/beacon.git
```

## quick start

```python
from beacon import recommend

# get book recommendations
results = recommend("fantasy adventure with dragons and magic")

# print matched books
for book in results:
    print(f"📖 {book['title']} by {book['author']}")
```

## development setup

1. clone the repository

```bash
git clone https://github.com/proteusiq/beacon.git
cd beacon
```

2. install dependencies and pre-commit hooks

```bash
make install
```

3. run tests

```bash
uv run pytest
```

4. format code and run linters

```bash
uv run pre-commit run -a
```

## examples

find books similar to your favorites:

```python
recommend("detective solving murders in victorian london")
recommend("post-apocalyptic survival story")
recommend("romance in a small coastal town")
```

---

made with ❤️ using [proteusiq/pyproject](https://github.com/proteusiq/pyproject)
