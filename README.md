# CTF_waragmes

A Python-based platform for running and playing Capture the Flag (CTF) wargames with an interactive, multi-level challenge system using Docker containers.

---

## Overview

**CTF_waragmes** is an automated CTF challenge platform that manages Docker-based wargame environments. The script orchestrates 10 progressive challenge levels, tracks your progress locally, and provides an interactive command-line experience for solving and submitting flags.

---

## Features

- **10-Level CTF Challenge:** Progress through sequential difficulty levels.
- **Docker-Based Environments:** Each level runs in an isolated Docker container.
- **Interactive CLI:** User-friendly command-line interface with colored output and clear instructions.
- **Shell Access:** Use the `play` command to attach to each level's Docker environment.
- **Local Progress Tracking:** Your progress is saved locally and persists across sessions.
- **GitHub Container Registry Integration:** Automatically pulls challenge containers from GHCR.
- **Flag Verification:** Submit flags directly through the CLI interface.
- **Progress Management:** Reset progress, delete account, or exit at any time.

---

## Prerequisites

- **Python 3.6+**
- **Docker** (installed and running)
- **Root/Sudo Access** (required for Docker operations)
- **GitHub Personal Access Token** (with `read:packages` permission for private images)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/PranavG1203/CTF_waragmes.git
cd CTF_waragmes
```

---

### 2. Run the Setup

```bash
sudo bash script.sh
```

The script will:
- Check for Docker installation
- Prompt for GitHub authentication (first run only)
- Pull all 10 challenge Docker images
- Set up your CTF environment

---

## Usage

### Available Commands

At each level prompt (`ctf-X>`), you can use:

- **`submit FLAG{...}`** – Submit your flag for the current level
- **`play`** – Open an interactive shell in the current level's Docker container
- **`restart`** – Reset your progress back to level 1
- **`delete`** – Delete your account and all progress
- **`exit`** – Exit the current level session

---
s' Group

---
