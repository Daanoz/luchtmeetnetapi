FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

RUN pipx install poetry

RUN su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install 16 2>&1"
