# CTF_Challenge

CTF (Capture The Flag) Wargame platform designed for cybersecurity and linux based events. It enables teams to participate in challenges across multiple levels, each hosted in an isolated container. Each level can be created by a different team member for diversity and skill-testing.

**🔧 Features**

- Web-based frontend for users to view and interact with levels
- Master node to manage users, levels, and container state
- Docker containers as isolated worker nodes (each running a CTF level)
- Per-level flag verification and user session management
- Real-time scoreboard to track team progress


**⚙️ Setup Instructions**

To start the game, clone the repo:

```
git clone https://github.com/Pooja411/CTF_Challenge-.git

cd Wargames_2k25
```

Then, run the game using the following command:

```
sudo bash initiate.sh
```

Type `begin` to start the game:

```
begin
```
