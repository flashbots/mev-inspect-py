# Contributing guide

Welcome to the Flashbots collective! We just ask you to be nice when you play with us.

## Pre-commit

We use pre-commit to maintain a consistent style, prevent errors, and ensure test coverage.

To set up, install dependencies through `poetry`:

```
poetry install
```

Then install pre-commit hooks with:

```
poetry run pre-commit install
```

## Tests

Run tests with:

```
./mev test
```

## Send a pull request

- Your proposed changes should be first described and discussed in an issue.
- Open the branch in a personal fork, not in the team repository.
- Every pull request should be small and represent a single change. If the problem is complicated, split it in multiple issues and pull requests.
- Every pull request should be covered by unit tests.

We appreciate you, friend <3.
