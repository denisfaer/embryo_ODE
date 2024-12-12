import nox

nox.options.sessions = ["tests"]
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session
def tests(session):
    session.install(".[test]")
    session.run("pytest")


@nox.session
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
