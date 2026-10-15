# Pomodoro Project Manager

A desktop productivity application based on the **Pomodoro Technique**, developed with **Python, PySide6 and MySQL**.

The application allows users to manage multiple projects, run Pomodoro work sessions, take short and long breaks, track progress and view productivity statistics.

---

## Project Overview

This project was developed as a desktop application using an **MVC architecture**.

The main objective is to help users organize their work using Pomodoro sessions while tracking progress for multiple projects.

The application includes:

- Multi-project management
- Pomodoro timer
- Short and long breaks
- Productivity statistics
- Daily Pomodoro goals
- Session history
- Notifications
- Sound alerts
- MySQL persistence
- Custom application settings

---

## Main Features

### Multi-Project Management

Users can create and manage several projects.

Each project contains:

- Name
- Description
- Target number of Pomodoros
- Completed Pomodoros
- Creation date
- Update date
- Progress percentage

The application automatically calculates project progress based on completed Pomodoro sessions.

---

## Pomodoro Sessions

The application supports three types of sessions:

- Work session
- Short break
- Long break

Default durations:

```text
Work: 25 minutes
Short break: 5 minutes
Long break: 15 minutes
