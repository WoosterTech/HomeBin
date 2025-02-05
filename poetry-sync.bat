echo Syncing poetry dependencies with dev, test, and docs groups...
@echo off

poetry sync --with dev,test,docs
