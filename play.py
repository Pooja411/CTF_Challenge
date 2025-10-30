#!/usr/bin/env python3

import os
import sys
import subprocess

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
BOLD = "\033[1m"

user_file_path = os.path.expanduser("~/.ctf_user")
progress_file_path = os.path.expanduser("~/.ctf_progress")

# Hardcoded flags for each level
LEVEL_FLAGS = {
    1: "FLAG{welcome_to_ctf}",
    2: "FLAG{basic_linux_commands}",
    3: "FLAG{file_permissions_master}",
    4: "FLAG{process_management_pro}",
    5: "FLAG{network_ninja}",
    6: "FLAG{script_wizard}",
    7: "FLAG{security_expert}",
    8: "FLAG{docker_master}",
    9: "FLAG{advanced_exploitation}",
    10: "FLAG{ultimate_hacker}"
}

TOTAL_LEVELS = len(LEVEL_FLAGS)

def get_username():
    """Get or prompt for username, save in ~/.ctf_user"""
    if os.path.isfile(user_file_path):
        with open(user_file_path, "r") as f:
            username = f.read().strip()
            if username:
                print(f"{BOLD}{YELLOW}Welcome back, {username}!{RESET}")
                return username
    username = ""
    while not username:
        username = input(f"{BOLD}{MAGENTA}Enter your CTF username: {RESET}").strip()
    with open(user_file_path, "w") as f:
        f.write(username)
    print(f"{BOLD}{YELLOW}Your username is set to {username}.{RESET}")
    return username

def get_current_level():
    """Get current level from local file"""
    if os.path.isfile(progress_file_path):
        with open(progress_file_path, "r") as f:
            try:
                level = int(f.read().strip())
                return level if 1 <= level <= TOTAL_LEVELS else 1
            except ValueError:
                return 1
    return 1

def save_progress(level):
    """Save current level to local file"""
    with open(progress_file_path, "w") as f:
        f.write(str(level))

def check_internet():
    try:
        subprocess.check_call(
            ["ping", "-c", "2", "google.com"], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        print(f"{BOLD}{GREEN}Internet is working!{RESET}")
        return True
    except subprocess.CalledProcessError:
        print(f"{BOLD}{YELLOW}No internet connection. Continuing offline...{RESET}")
        return False

def are_you_sudo():
    return os.geteuid() == 0

def get_os():
    if sys.platform.startswith("linux"):
        try:
            with open("/etc/os-release") as f:
                lines = f.read().lower()
                if "ubuntu" in lines: return "Ubuntu"
                if "debian" in lines: return "Debian"
                if "centos" in lines: return "CentOS"
                if "red hat" in lines: return "RHEL"
                if "fedora" in lines: return "Fedora"
                if "arch" in lines: return "Arch"
        except Exception:
            pass
    elif sys.platform == "darwin":
        return "MacOS"
    return "Unknown"

def check_docker():
    """Check if Docker is available"""
    result = subprocess.call(
        "docker --version > /dev/null 2>&1", 
        shell=True
    )
    if result == 0:
        print(f"{BOLD}{BLUE}Docker is installed!{RESET}")
        return True
    else:
        print(f"{BOLD}{YELLOW}Docker not found. Some features may not work.{RESET}")
        return False

def pull_level(level):
    """Pull a single Docker level image"""
    tag = f"warg{level}"
    docker_image = f"ghcr.io/walchand-linux-users-group/wildwarrior44/wargame_finals:{tag}"
    print(f"{YELLOW}Pulling level {level}...{RESET}", end=" ", flush=True)
    
    get_level = f"docker pull {docker_image} > /dev/null 2>&1"
    exit_status = subprocess.call(get_level, shell=True)
    
    if exit_status == 0:
        print(f"{GREEN}✓{RESET}")
        return True
    else:
        print(f"{RED}✗{RESET}")
        return False

def setup():
    """Simple setup without threading"""
    if not are_you_sudo():
        print(f"{BOLD}{RED}Run the script with sudo!{RESET}")
        return False
    
    os.system("clear")
    check_internet()
    
    if not check_docker():
        print(f"{BOLD}{RED}Please install Docker manually.{RESET}")
        return False
    
    print(f"{BOLD}{MAGENTA}Pulling level images...{RESET}")
    for i in range(1, TOTAL_LEVELS + 1):
        pull_level(i)
    
    print(f"{BOLD}{GREEN}Setup complete!{RESET}")
    return True

def check_file():
    """Check if setup has been performed"""
    if os.path.isfile(user_file_path):
        with open(user_file_path, "r") as f:
            if f.read().strip():
                return True
    return False

def verify_flag(flag, level):
    """Verify flag locally"""
    expected_flag = LEVEL_FLAGS.get(level)
    if expected_flag and flag.strip() == expected_flag:
        return True
    return False

def print_section_header(title):
    print(f"{BOLD}{MAGENTA}┌──────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{MAGENTA}│ {title}{RESET}{BOLD}{MAGENTA}{' ' * (38 - len(title) - 1)}│{RESET}")
    print(f"{BOLD}{MAGENTA}└──────────────────────────────────────┘{RESET}")

def reset_progress(user_id):
    """Reset user progress to level 1"""
    save_progress(1)
    print(f"{YELLOW}{BOLD}Progress reset to level 1!{RESET}")
    # Clean up all containers
    for i in range(1, TOTAL_LEVELS + 1):
        subprocess.call(f"docker rm -f ctf{i} > /dev/null 2>&1", shell=True)

def delete_user():
    """Delete user data"""
    if os.path.isfile(user_file_path):
        os.remove(user_file_path)
    if os.path.isfile(progress_file_path):
        os.remove(progress_file_path)
    # Clean up containers
    for i in range(1, TOTAL_LEVELS + 1):
        subprocess.call(f"docker rm -f ctf{i} > /dev/null 2>&1", shell=True)
    print(f"{RED}{BOLD}User deleted! Goodbye!{RESET}")

def interactive_level_shell(level_name, level_num, user_id):
    """Run interactive shell for a level"""
    # Check if container exists
    check_container = f"docker ps -a --format '{{{{.Names}}}}' | grep -w {level_name} > /dev/null 2>&1"
    container_exists = subprocess.call(check_container, shell=True)
    
    tag = f"warg{level_num}"
    docker_image = f"ghcr.io/walchand-linux-users-group/wildwarrior44/wargame_finals:{tag}"
    
    if container_exists != 0:
        print(f"{YELLOW}Starting container for level {level_num}...{RESET}")
        level_string = (
            f"docker run -dit --hostname {user_id} --user root --name {level_name} "
            f"{docker_image} /bin/bash > /dev/null 2>&1"
        )
        exit_code = subprocess.call(level_string, shell=True)
        if exit_code != 0:
            print(f"{RED}Failed to start container.{RESET}")
            print(f"{YELLOW}You can still submit the flag if you know it!{RESET}")
    
    print_section_header(f"Level {level_num} - {user_id}")
    print(f"{GREEN}{BOLD}Commands:{RESET}")
    print(f"  {BLUE}submit FLAG{{...}}{RESET} - Submit your flag")
    print(f"  {BLUE}play{RESET}           - Enter Docker shell")
    print(f"  {BLUE}restart{RESET}        - Reset progress to level 1")
    print(f"  {BLUE}delete{RESET}         - Delete account")
    print(f"  {BLUE}exit{RESET}           - Exit current level\n")

    while True:
        try:
            user_input = input(f"{BOLD}{MAGENTA}ctf-{level_num}> {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        
        if not user_input:
            continue
            
        if user_input.lower().startswith("submit "):
            flag = user_input[7:].strip()
            if verify_flag(flag, level_num):
                print(f"{GREEN}{BOLD}✓ Correct flag! Level complete!{RESET}")
                # Clean up container
                subprocess.call(f"docker rm -f {level_name} > /dev/null 2>&1", shell=True)
                new_level = level_num + 1
                save_progress(new_level)
                return new_level
            else:
                print(f"{RED}{BOLD}✗ Incorrect flag. Try again!{RESET}")
        
        elif user_input.lower() == "play":
            attach_command = f"docker start {level_name} > /dev/null 2>&1 && docker exec -it {level_name} bash"
            os.system(attach_command)
        
        elif user_input.lower() == "restart":
            confirm = input(f"{RED}Are you sure you want to reset? (yes/no): {RESET}").strip().lower()
            if confirm == "yes":
                reset_progress(user_id)
                subprocess.call(f"docker rm -f {level_name} > /dev/null 2>&1", shell=True)
                return 1
        
        elif user_input.lower() == "delete":
            confirm = input(f"{RED}Are you sure you want to delete your account? (yes/no): {RESET}").strip().lower()
            if confirm == "yes":
                delete_user()
                sys.exit(0)
        
        elif user_input.lower() == "exit":
            print(f"{YELLOW}Exiting level {level_num}...{RESET}")
            return level_num
        
        else:
            print(f"{YELLOW}Unknown command. Type 'submit', 'play', 'restart', 'delete', or 'exit'.{RESET}")
    
    return level_num

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-r":
        print_section_header("Resetting User")
        if os.path.isfile(user_file_path):
            with open(user_file_path, "r") as f:
                user_id = f.read().strip()
                if user_id:
                    reset_progress(user_id)
                    return
        print(f"{RED}No user found to reset.{RESET}")
        return
    
    if not check_file():
        if not setup():
            return
    
    user_id = get_username()
    current_level = get_current_level()
    
    print(f"{GREEN}{BOLD}Welcome, {user_id}!{RESET}")
    print(f"{BLUE}Current Level: {current_level}/{TOTAL_LEVELS}{RESET}\n")
    
    while current_level <= TOTAL_LEVELS:
        os.system("clear")
        level_name = f"ctf{current_level}"
        new_level = interactive_level_shell(level_name, current_level, user_id)
        
        if new_level is None or new_level == current_level:
            break
        
        current_level = new_level
    
    if current_level > TOTAL_LEVELS:
        os.system("clear")
        print(f"{BOLD}{GREEN}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{BOLD}{GREEN}  🎉 Congratulations! You completed all {TOTAL_LEVELS} levels! 🎉{RESET}")
        print(f"{BOLD}{GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
    else:
        print(f"{BOLD}{YELLOW}\nSee you next time, {user_id}!{RESET}")

if __name__ == "__main__":
    main()
