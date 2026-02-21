# Web Exploitation

## Server Side Template Injection
**Goal:** To get the flag located somewhere in  a file in the server

### Procedures
1. **Test:** Test the website and run different langauge-specific payloads to find the langauge and language used.
2. **FInd the template specific code for Remote COde execution:** After runninng multiple payloads, It was discovered that jinja was used as the template engine
3. **Run the code:** Run the code to first find the contents of the server using `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls').read() }}` and find the flag file and then read it using `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat flag').read() }}`

**Challenges:** Finding out the template engine used in the website

**Lesson learnt**
1. How to expliot basic Server Side Template injections
2. How to run Remote Code Execution

