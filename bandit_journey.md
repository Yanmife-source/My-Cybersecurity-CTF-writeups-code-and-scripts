# My Overthewire Bandit wargame journey write-up series

## Level 0 to 1 (Initial login)
**Goal:** To login using SSH and find the password in a file 'readme' in the home directory

### Procedure: 
1. **Login:** Connect using SSH with the following command using the given credenials `ssh bandit0@bandit.labs.overthewire.org -p 2220`
2. **Locate file:** Use the 'ls' command to know the contents of the home directory
3. **Read the file:** Using the command 'cat',I read the file by entering `cat readme`

**Lesson learnt:** 
* How to connect to a server using SSH
* How to use the 'ls' command to knwo the contents of a directory
* How to use 'cat' to read files

---

## Level 1 to 2
**Goal:** To read a file '-' in the home directory for the password
**Challenges:**The file name begins with a dash which made cat to not work correctly and read it so I had to use `./` to specify the current directory

### Procedure:
1. **Find the file:** Use 'ls' to find the contents of the home directory
2. **Read the file:** Read the file using the command `cat ./-` as doing it normally `cat -` causes issues. 

**Lesson Learnt:**
* How to use cat to read filenames that beginning with a dash/dashed filenames

---

## Level 2 to 3
**Goal:** 
