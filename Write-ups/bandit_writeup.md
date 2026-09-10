# My OverTheWire Bandit Wargame Journey

A write-up series documenting my progress through the Bandit wargame — a beginner-friendly CTF that teaches essential Linux and security skills from scratch. I'll be documenting each level, what I did, and what lessons I took away from it.

---

## Level 0 → 1
**Goal:** Log into the game server using SSH and find the password stored in a file called `readme` in the home directory

### Procedure:
1. **Login:** I connected to the server using the SSH command below with the given credentials
   `ssh bandit0@bandit.labs.overthewire.org -p 2220`
   The password was simply `bandit0`

2. **Locate the file:** I ran `ls` to see what was in the home directory and sure enough there was a file called `readme`

3. **Read the file:** I used `cat readme` to print the contents of the file and got the password for the next level

**Lessons Learnt:**
* How to connect to a remote server using SSH
* How to use `ls` to list the contents of a directory
* How to use `cat` to read a file

---

## Level 1 → 2
**Goal:** Find and read a file called `-` in the home directory
**Challenge:** The filename starts with a dash which caused `cat -` to not work — the shell was treating it as a flag/option rather than a filename

### Procedure:
1. **Find the file:** I ran `ls` to confirm the file was there — and it was, just called `-`

2. **Read the file:** I couldn't just do `cat -` so I had to explicitly tell the shell it's a path by doing `cat ./-` which worked perfectly

**Lessons Learnt:**
* How to read dashed filenames using `./` to prefix the path
* How the shell distinguishes between command flags and actual filenames

---

## Level 2 → 3
**Goal:** Read a file called `spaces in this filename` in the home directory
**Challenge:** The spaces in the filename break the normal way you'd type a `cat` command since the shell treats each word as a separate argument

### Procedure:
1. **Find the file:** Used `ls` to confirm the filename

2. **Read the file:** I wrapped the filename in quotes — `cat "spaces in this filename"` — and that did the trick. You can also escape each space with a backslash like `cat spaces\ in\ this\ filename` but quoting felt cleaner

**Lessons Learnt:**
* How to handle filenames with spaces using quotes or backslash escaping
* That the shell splits arguments on spaces unless you tell it not to

---

## Level 3 → 4
**Goal:** Find a hidden file inside the `inhere` directory and read it
**Challenge:** Hidden files in Linux start with a `.` and don't show up when you run a plain `ls`

### Procedure:
1. **Navigate to the directory:** I ran `cd inhere` to move into the folder

2. **List hidden files:** I used `ls -la` which shows ALL files including hidden ones. There it was — a file starting with a dot

3. **Read the file:** Used `cat` with the full hidden filename to get the password

**Lessons Learnt:**
* That files starting with `.` are hidden by default in Linux
* How to use `ls -la` (or `ls -a`) to reveal hidden files

---

## Level 4 → 5
**Goal:** Find the only human-readable file among several files in the `inhere` directory
**Challenge:** There were 10 files (`-file00` through `-file09`) and most were binary — only one had actual readable text

### Procedure:
1. **Navigate:** `cd inhere`

2. **Check file types:** I ran `file ./*` which runs the `file` command on every file at once. This tells you what type each file is — binary data, ASCII text, etc. One of them came back as `ASCII text` and that was my target

3. **Read it:** Used `cat ./-file07` (or whichever file it pointed to) to get the password

**Lessons Learnt:**
* How to use the `file` command to identify what type of data a file contains
* How to use `*` as a wildcard to run a command on multiple files at once

---

## Level 5 → 6
**Goal:** Find a file somewhere in the `inhere` directory that is human-readable, exactly 1033 bytes in size, and not executable

### Procedure:
1. **Use `find` with specific filters:**
   `find inhere -type f -size 1033c ! -executable`
   - `-type f` means regular files only
   - `-size 1033c` means exactly 1033 bytes (the `c` stands for bytes)
   - `! -executable` means the file must not be executable

2. **Read the result:** Only one file matched all three conditions — I used `cat` on it to get the password

**Lessons Learnt:**
* How powerful `find` is when you combine multiple filters
* That `find` uses `c` for bytes when specifying file size
* How to negate a condition with `!` in `find`

---

## Level 6 → 7
**Goal:** Find a file somewhere on the entire server that is owned by user `bandit7`, owned by group `bandit6`, and is 33 bytes in size
**Challenge:** This time I had to search the whole filesystem, not just the home directory

### Procedure:
1. **Search from root:**
   `find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null`
   - `/` means start searching from the very root of the filesystem
   - `-user` and `-group` filter by ownership
   - `2>/dev/null` silences all the "Permission denied" errors that come from trying to read directories I don't have access to — without this the output is a mess

2. **Read the file:** The result pointed to `/var/lib/dpkg/info/bandit7.password` — ran `cat` on it and got the password

**Lessons Learnt:**
* How to search the entire Linux filesystem using `find /`
* How to filter by file ownership using `-user` and `-group`
* How to redirect stderr to `/dev/null` to clean up noisy output

---

## Level 7 → 8
**Goal:** The password is in `data.txt`, stored next to the word `millionth`

### Procedure:
1. **Search for the keyword:**
   `grep "millionth" data.txt`
   The file was huge so manually reading it was out of the question. `grep` instantly found the line containing the word and printed the password right next to it

**Lessons Learnt:**
* How to use `grep` to search for a specific string inside a file
* That `grep` is incredibly useful when dealing with large files

---

## Level 8 → 9
**Goal:** The password is the only line in `data.txt` that appears exactly once — every other line is a duplicate
**Challenge:** I had to find a single unique line among thousands of repeated ones

### Procedure:
1. **Sort and filter:**
   `sort data.txt | uniq -u`
   - `sort` rearranges all the lines alphabetically so identical lines end up next to each other
   - `uniq -u` then prints only the lines that appear exactly once
   Without sorting first, `uniq` wouldn't catch duplicates that aren't adjacent

**Lessons Learnt:**
* How `sort` and `uniq` work together as a pipeline
* That `uniq` needs sorted input to correctly identify duplicates
* The `-u` flag on `uniq` for isolating unique-only lines

---

## Level 9 → 10
**Goal:** The password is in `data.txt` — a mostly binary file — hidden among a few human-readable strings, preceded by several `=` characters

### Procedure:
1. **Extract readable strings and filter:**
   `strings data.txt | grep "=="`
   - `strings` pulls out all printable character sequences from the binary file
   - `grep "=="` then narrows it down to lines that have `=` characters in them, which quickly pointed me to the password

**Lessons Learnt:**
* How `strings` extracts readable text from binary/mixed files
* How to chain `strings` and `grep` for targeted extraction

---

## Level 10 → 11
**Goal:** `data.txt` contains base64-encoded data — decode it to get the password

### Procedure:
1. **Decode the file:**
   `base64 -d data.txt`
   Simple one-liner — the `-d` flag tells `base64` to decode rather than encode

**Lessons Learnt:**
* What base64 encoding is and why it's commonly used (safe text transport)
* How to decode base64 data using `base64 -d`

---

## Level 11 → 12
**Goal:** The contents of `data.txt` have been encoded with ROT13 — every letter has been shifted 13 positions in the alphabet

### Procedure:
1. **Decode ROT13:**
   `cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'`
   The `tr` command translates characters — here it maps every letter to its ROT13 equivalent. Since the alphabet has 26 letters, applying ROT13 twice gets you back to the original, so encode and decode are the same operation

**Lessons Learnt:**
* What ROT13 is and how it works as a simple substitution cipher
* How to use `tr` for character-level translation in the terminal

---

## Level 12 → 13
**Goal:** `data.txt` is a hexdump of a file that has been compressed multiple times. Reverse the hexdump and then keep decompressing until you reach the actual password
**Challenge:** This one had several layers — I had to unwrap them one by one, which got tedious

### Procedure:
1. **Create a working directory:** Since the home directory is read-only I had to work in `/tmp`
   `mkdir /tmp/mywork` then `cp data.txt /tmp/mywork/` and `cd /tmp/mywork`

2. **Reverse the hexdump:**
   `xxd -r data.txt > data.bin`
   This converts the hex representation back into actual binary data

3. **Repeatedly identify and decompress:**
   I kept running `file data.bin` to check what type of file it was, then decompressed accordingly:
   - For `.gz` files: `gzip -d filename.gz`
   - For `.bz2` files: `bzip2 -d filename.bz2`
   - For `.tar` archives: `tar -xf filename.tar`
   I renamed files between steps to keep track of where I was. After enough rounds of this, I finally got a plain text file with the password

**Lessons Learnt:**
* How to reverse a hexdump using `xxd -r`
* How to identify and handle multiple compression formats (`gzip`, `bzip2`, `tar`)
* Why working in `/tmp` is useful when you need write access
* Patience — this level is genuinely repetitive

---

## Level 13 → 14
**Goal:** There's no password file this time — instead there's a private SSH key in the home directory that lets you log in as `bandit14`

### Procedure:
1. **Use the SSH key to log in as bandit14:**
   `ssh -i sshkey.private bandit14@localhost -p 2220`
   The `-i` flag lets you specify a private key file for authentication instead of a password

2. **Retrieve the password:**
   `cat /etc/bandit_pass/bandit14`
   Now that I was logged in as `bandit14` I could read the password directly

**Lessons Learnt:**
* How SSH key-based authentication works
* How to use the `-i` flag with SSH to specify a key file
* That on Bandit, passwords are stored in `/etc/bandit_pass/` and only readable by the respective user

---

## Level 14 → 15
**Goal:** Send the current level's password to port 30000 on localhost — the server will respond with the next password

### Procedure:
1. **Send the password over the network:**
   `echo "current_password_here" | nc localhost 30000`
   `nc` (netcat) opens a raw TCP connection to the given host and port. Piping the password into it sends it as a message, and the server responds with the next password

**Lessons Learnt:**
* What netcat (`nc`) is and how to use it for basic TCP communication
* How to pipe output from one command into a network connection

---

## Level 15 → 16
**Goal:** Same idea as the last level but this time port 30001 requires an SSL/TLS encrypted connection — plain netcat won't work here

### Procedure:
1. **Connect using OpenSSL:**
   `openssl s_client -connect localhost:30001`
   This opens an SSL-encrypted connection. Once connected I pasted in the current password and the server returned the next one

**Lessons Learnt:**
* The difference between a plain TCP connection and an SSL/TLS encrypted one
* How to use `openssl s_client` to connect to SSL services from the terminal

---

## Level 16 → 17
**Goal:** Find a port between 31000 and 32000 that speaks SSL and will accept the current password — it will respond with an SSH private key for the next level
**Challenge:** I had to figure out which port was the right one out of a range

### Procedure:
1. **Scan the port range:**
   `nmap -sV -p 31000-32000 localhost`
   This scans all ports in that range and identifies which ones are open and what services they're running. I was looking for one that showed SSL

2. **Connect to the right port:**
   `openssl s_client -connect localhost:31790`
   I pasted the current password and received an RSA private key back

3. **Save and use the key:**
   I created a file in `/tmp/`, pasted the key in, set the right permissions with `chmod 400`, then used it to SSH in as `bandit17`

**Lessons Learnt:**
* How to use `nmap` for port scanning and service detection with `-sV`
* Combining port scanning with SSL connection attempts
* That SSH keys need strict permissions (`chmod 400`) or SSH refuses to use them

---

## Level 17 → 18
**Goal:** There are two files in the home directory — `passwords.old` and `passwords.new`. The password for the next level is the one line that changed between them

### Procedure:
1. **Compare the two files:**
   `diff passwords.old passwords.new`
   `diff` shows you exactly what changed between two files. The line marked with `>` is the new one — that's the password

**Lessons Learnt:**
* How `diff` works for comparing files line by line
* Reading `diff` output: `<` means the old line, `>` means the new/changed line

---

## Level 18 → 19
**Goal:** The password is in `readme` in the home directory but the `.bashrc` has been modified to immediately log you out the moment you connect
**Challenge:** Every time I tried to SSH in, the session closed before I could do anything

### Procedure:
1. **Run the command directly through SSH without opening an interactive shell:**
   `ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme`
   By appending a command at the end of the SSH line, it executes that command on the remote machine and returns the output — without ever actually loading `.bashrc` or giving the logout script a chance to run

**Lessons Learnt:**
* How to execute a remote command via SSH without starting an interactive session
* That `.bashrc` can be used to kick users on login — and how to bypass it
* Non-interactive SSH is a really useful trick

---

## Level 19 → 20
**Goal:** Use the setuid binary in the home directory to read the password for `bandit20`

### Procedure:
1. **Inspect the binary:**
   Running `ls -la` I noticed a binary called `bandit20-do` with the setuid bit set — meaning it runs as `bandit20` regardless of who executes it

2. **Use it to read the password:**
   `./bandit20-do cat /etc/bandit_pass/bandit20`
   Since the binary runs as `bandit20`, it can read files that I as `bandit19` normally can't

**Lessons Learnt:**
* What setuid binaries are — files that run with the permissions of their owner, not the person running them
* How setuid can be both a useful feature and a serious security risk

---

## Level 20 → 21
**Goal:** Use the setuid binary `suconnect` which connects to a localhost port, reads a line, and if it matches the current password, returns the next password. I had to set up my own listener first.

### Procedure:
1. **Start a listener in the background:**
   `echo "current_password" | nc -lp 4444 &`
   This starts a netcat listener on port 4444 that sends the current password to whatever connects to it. The `&` runs it in the background so I can still use the terminal

2. **Run the binary:**
   `./suconnect 4444`
   It connected to my listener, read the password, confirmed it matched, and printed the next password

**Lessons Learnt:**
* How to set up a basic TCP listener with `nc -l`
* Running processes in the background with `&`
* How two local processes can communicate through localhost ports

---

## Level 21 → 22
**Goal:** A program is being run automatically at regular intervals via cron. Find out what it's doing and use that to get the password.

### Procedure:
1. **Check what cron jobs are running:**
   `ls /etc/cron.d/` then `cat /etc/cron.d/cronjob_bandit22`

2. **Read the script it's executing:**
   `cat /usr/bin/cronjob_bandit22.sh`
   The script was writing the `bandit22` password to a file in `/tmp/`

3. **Read that file:**
   `cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`

**Lessons Learnt:**
* What cron jobs are and where to find them on a Linux system
* How to trace a cron job from its schedule through to its output

---

## Level 22 → 23
**Goal:** Another cron job — this time the script generates a filename based on the username using a hash. I had to understand the script and reproduce its logic to figure out where it was writing the password.

### Procedure:
1. **Read the script:**
   `cat /etc/cron.d/cronjob_bandit23` then `cat /usr/bin/cronjob_bandit23.sh`
   The script was doing something like: take the string `I am user bandit23`, hash it with `md5sum`, and write the password to `/tmp/<that_hash>`

2. **Reproduce the hash manually:**
   `echo I am user bandit23 | md5sum | cut -d ' ' -f 1`
   This gave me the exact filename the cron job was using

3. **Read the password:**
   `cat /tmp/<hash>`

**Lessons Learnt:**
* How to read and understand someone else's shell script
* How `md5sum` and `cut` work together
* That reproducing another process's logic manually is a core CTF skill

---

## Level 23 → 24
**Goal:** Write a shell script and place it in a directory that a cron job watches — the cron job will execute it as `bandit24`, allowing me to copy the password somewhere I can read it

### Procedure:
1. **Create a working directory:**
   `mkdir /tmp/mybandit23` and `chmod 777 /tmp/mybandit23` so the cron job can write to it

2. **Write the script:**
   I created a file called `getpass.sh` containing:
   `cat /etc/bandit_pass/bandit24 > /tmp/mybandit23/password.txt`
   Then made it executable with `chmod +x getpass.sh`

3. **Drop it in the watched directory:**
   `cp getpass.sh /var/spool/bandit24/foo/`

4. **Wait for the cron job to run** (up to a minute), then:
   `cat /tmp/mybandit23/password.txt`

**Lessons Learnt:**
* How cron drop directories work — scripts placed there get automatically executed
* Why directory and file permissions matter so much when another user needs to write to your folder
* Writing a script designed to be executed by a different user is a key privilege escalation concept

---

## Level 24 → 25
**Goal:** A daemon on port 30002 will give the next password if I send it the current password plus the correct 4-digit PIN. I don't know the PIN so I had to brute-force all 10,000 possibilities.

### Procedure:
1. **Write a brute-force script** that loops through every number from 0000 to 9999, pairs it with the current password, and sends all combinations to the port at once via netcat

2. **Filter out failures:**
   `grep -v "Wrong" output.txt`
   The server returns "Wrong" for bad PINs so filtering those out leaves only the correct response

**Lessons Learnt:**
* How to write a basic brute-force loop in bash
* Using `seq -w` for zero-padded number sequences
* Piping bulk generated input into netcat for batch testing

---

## Level 25 → 26
**Goal:** Log in as `bandit26` using the provided SSH key — but `bandit26`'s login shell isn't bash, it's a custom binary that immediately exits. I had to find a way to stay in.
**Challenge:** Every time I SSH'd in, the connection closed almost instantly

### Procedure:
1. **Investigate the custom shell:**
   `cat /etc/passwd | grep bandit26` showed the shell was `/usr/bin/showtext`
   `cat /usr/bin/showtext` revealed it just runs `more` on a text file and then exits

2. **Exploit `more`:** I made my terminal window really small vertically so the text couldn't fit on one screen — this forced `more` into interactive mode instead of just printing and exiting

3. **From within `more`, open vim** by pressing `v`

4. **Inside vim, escape to a shell:**
   `:set shell=/bin/bash` then `:shell`
   And just like that I had a working bash shell as `bandit26`

**Lessons Learnt:**
* How `/etc/passwd` controls what shell a user gets on login
* That `more` has an interactive mode and can open an editor — a classic escape vector
* Using vim's `:shell` command to break out of restricted environments
* This one was genuinely satisfying to figure out

---

## Level 26 → 27
**Goal:** While still logged in as `bandit26` (via the vim shell trick), use the setuid binary `bandit27-do` to grab the next password

### Procedure:
1. **From the shell I had inside vim:**
   `./bandit27-do cat /etc/bandit_pass/bandit27`
   The binary runs with `bandit27` permissions so it can read the password file directly

**Lessons Learnt:**
* How to chain techniques across levels
* Recognising setuid binaries and what they let you do

---

## Level 27 → 28
**Goal:** Clone a git repository hosted on localhost and find the password inside it

### Procedure:
1. **Create a temp directory** to clone into since the home directory is read-only:
   `mkdir /tmp/gitwork27` and `cd /tmp/gitwork27`

2. **Clone the repo:**
   `git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo`

3. **Read the README:**
   `cat repo/README`
   Password was sitting right there

**Lessons Learnt:**
* How to clone a git repository over SSH
* That CTF challenges increasingly use git — so basic git literacy matters

---

## Level 28 → 29
**Goal:** Same setup — but this time the password has been removed from the current version of the repo. It's somewhere in the commit history.

### Procedure:
1. **Clone and check the history:**
   After cloning, I ran `git log --oneline` and could see a commit with a message like "fix info leak" — suspicious

2. **Inspect that commit:**
   `git show <commit-hash>`
   Sure enough the password was visible in a previous version before it was redacted

**Lessons Learnt:**
* How `git log` lets you browse commit history
* How `git show` reveals what changed in a specific commit
* A really important real-world lesson: deleting sensitive data from a git repo doesn't erase it from history

---

## Level 29 → 30
**Goal:** The password isn't in the main branch of the repo — it's somewhere else

### Procedure:
1. **Clone and check all branches:**
   After cloning I ran `git branch -a` to list every branch including remote ones. One called `dev` looked interesting

2. **Switch to it:**
   `git checkout dev` then `cat README.md`
   Password was in there

**Lessons Learnt:**
* How to list all branches with `git branch -a`
* How to switch branches with `git checkout`
* Sensitive information doesn't always live on the main branch

---

## Level 30 → 31
**Goal:** The password is hidden in a git tag

### Procedure:
1. **Clone and check tags:**
   After cloning I ran `git tag` — there was one called `secret`

2. **Read it:**
   `git show secret`
   Password right there

**Lessons Learnt:**
* What git tags are (markers attached to commits or arbitrary objects)
* How to list and inspect tags — they're often overlooked in security audits

---

## Level 31 → 32
**Goal:** Push a specific file to the remote repo — the server checks it and responds with the next password

### Procedure:
1. **Clone the repo** and create the required file:
   `echo "May I come in?" > key.txt`

2. **Add, commit, and push:**
   `git add -f key.txt`
   The `-f` flag was necessary because `.gitignore` was blocking `*.txt` files
   `git commit -m "Add key"` then `git push origin master`
   The server accepted the push and returned the next password

**Lessons Learnt:**
* The full git workflow: create → add → commit → push
* How `.gitignore` works and how to override it with `git add -f`
* That server-side git hooks can execute logic when you push — useful and dangerous

---

## Level 32 → 33
**Goal:** After logging in, every command I typed was being converted to uppercase — making most Linux commands completely useless. I had to escape this restricted shell.
**Challenge:** `ls`, `cat`, `sh` all became `LS`, `CAT`, `SH` — none of which are valid commands

### Procedure:
1. **Use a shell variable instead of typing a command:**
   `$0`
   The special variable `$0` holds the name of the current shell. Since it's a variable reference rather than typed text, it doesn't get uppercased. Entering it dropped me straight into a normal `/bin/sh`

2. **Read the password:**
   `cat /etc/bandit_pass/bandit33`

**Lessons Learnt:**
* How restricted/modified shells work and their limitations
* The special shell variable `$0` and what it refers to
* That knowing your shell internals can get you out of seemingly impossible situations

---

## Level 33 → 34
**Goal:** Reach the end and read the final message

### Procedure:
1. **Login and read:**
   `ssh bandit33@bandit.labs.overthewire.org -p 2220` then `cat README.txt`

```
The README congratulates you on finishing all currently available Bandit levels — a genuinely satisfying moment after everything it took to get here.
```
---

## Final Thoughts

Bandit was a great starting point. It covers a wide range of fundamentals — file handling, networking, scripting, git, privilege escalation — without ever being unfair. Every level teaches you something concrete. Some levels (looking at you, level 12 and level 25) were genuinely frustrating, but working through that frustration is part of the point.

If you're reading this and just starting out — don't skip levels and don't just copy commands. Try to understand *why* each command works the way it does. That's where the actual learning is.

On to the next wargame.
