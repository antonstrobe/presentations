# Presentations

This project contains a small Python application that communicates with the OpenAI API.
It generates an image, audio narration and a short video for any word you enter.

## Usage

1. Run `run.bat` on Windows. The script upgrades `pip`, installs dependencies and launches the app.
2. On the first run you will be prompted for your OpenAI API key. It will be saved in `openai_key.txt` for future sessions.
3. Enter a word in the application window and press **Send**. After processing you will receive an image, a playable audio file
and a short video.

The interface uses Tkinter with basic styling and shows progress messages as each step completes.

## Android Widget Project

The [`android-widget`](android-widget) directory contains a minimal Android app widget targeting API 34. The repository omits the Gradle wrapper JAR; run `gradle wrapper` in that directory before building. See its README for build instructions.
