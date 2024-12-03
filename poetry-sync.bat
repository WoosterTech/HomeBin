echo Syncing poetry dependencies with dev, test, and docs groups...
@echo off

poetry install --sync --with dev,test,docs
