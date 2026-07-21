# Web Exploitation

## Server Side Template Injection (picoCTF)
**Goal:** To get the flag located somewhere in  a file in the server

### Procedures
1. **Test:** Test the website and run different langauge-specific payloads to find the langauge and language used.
2. **FInd the template specific code for Remote Code execution:** After runninng multiple payloads, It was discovered that jinja was used as the template engine
3. **Run the code:** Run the code to first find the contents of the server using `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls').read() }}` and find the flag file and then read it using `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat flag').read() }}`

**Challenges:** Finding out the template engine used in the website

**Lesson learnt**
1. How to expliot basic Server Side Template injections
2. How to run Remote Code Execution


## Cross Site Scripting (Google XSS game)
**Goal:** To inject a script to pop up an alert() in the context of the application.
### Level 1 procedures (Regular XSS flaw)
1. **Find the target and inject the XSS payload:**Find the box to inject the XSS payload and enter the classic `<script>alert(1)</script>` which is a basic XSS paylaod to expliot improper handling of user data

### Level 2 procedures (Stored XSS flaw)
1.  **Bypass innerHTML Script Restrictions:** The XSS flaw in this level is a Stored XSS flaw  and thusStandard `<script>alert(1)</script>` tags will fail here. Web browsers do not execute <script> elements injected via innerHTML to prevent late-stage execution risks. Instead, utilize an alternative HTML tag that triggers an execution event natively upon loading.
2. **Craft and Submit the Payload:** Inject a broken image element configured with an onerror event handler with the code `<img src=x onerror=alert(1)>`
3. **Verify Persistent Execution:**Once submitted, the browser attempts to load the image x, fails, and executes alert(1). Because the level stores this input, the code remains in the post history. Every time you reload the browser tab, the application pulls the payload from its data store, renders it, and automatically solves the level again.

### Levele 3 procedures (Reflected XSS flaw)
1. **Find the target:**Since you can't enter your payload anywhere in the application, you will have to manually edit the address in the URL bar indicated in the level .
2. **Figure out how to exploit the XSS vulnerability:**Usng the  url and code available `https://xss-game.appspot.com/level3/frame#1` and the code `html += "<img src='/static/level3/cloud" + num + ".jpg' />"` which directly substistutes page nuber into the url and allows us to pop up an alert using `https://xss-game.appspot.com/level3/frame#1'><script>alert(1)</script>` to both close the src attribute and to close the tag thus allowing us to execute the alert() in between scripts tags.

### Level 4 procedures (DOM-based XSS via JS injection)
1. **Find the target:** The vulnerability is in the timer input field on the page. 
The server-side template injects your input directly into a JS event handler:
`onload="startTimer('{{ timer }}');"`

2. **Figure out how to exploit the vulnerability:** Since your input lands inside 
a JS string inside an HTML event handler, you are already in a JS execution context 
— no `<script>` tags needed. Submitting `'` alone breaks the JS and throws 
`Uncaught SyntaxError: missing ) after argument list`, confirming the injection point 
is live. The payload needs to close the open string, call alert(), and reopen the 
string to keep the surrounding JS valid.

3. **Craft and Submit the Payload:** Type `'+alert(1)+'` into the timer input field 
and submit. This turns the onload attribute into:
`onload="startTimer(''+alert(1)+'');"` 
which is valid JS — the string concatenation executes alert(1) as the argument 
to startTimer(), popping the alert and solving the level.


### Level 5 procedures (DOM-based XSS via javascript: URI)

1. **Find the target:** The vulnerability is in the `next` URL parameter. The
server-side template reflects your input directly into the `href` attribute of
an existing anchor tag:
`<a href="{{ next }}">Next >></a>`

2. **Figure out how to exploit the vulnerability:** Since your input lands
directly inside an `href` attribute, standard tag injection won't work — the
template engine escapes `<` and `>` into `&lt;` and `&gt;`, preventing you
from injecting new elements. However, HTML entity encoding does not validate
URI *schemes*. Browsers treat the content of an `href` as a URI and will
execute any `javascript:` URI when the link is clicked — no new DOM elements
needed. Submitting `'` or a broken URL confirms the parameter is reflected
live in the rendered HTML.

3. **Craft and Submit the Payload:** Navigate to the level URL and change the
`next` parameter to `javascript:alert(1)`:
`https://xss-game.appspot.com/level5/frame?next=javascript:alert(1)`. This turns the anchor tag into:
`<a href="javascript:alert(1)">Next >></a>` .Then click the "Next >>" link. The browser interprets the `href` as a
JavaScript URI rather than a navigation URL and executes `alert(1)` in the
context of the page, solving the level — without a single new element being
injected into the DOM.

### Level 6 procedures (DOM-based XSS via data: URI scheme bypass)

1. **Find the target:** The vulnerability is in the URL fragment (the part
after `#`). The page's `includeGadget()` function reads `window.location.hash`
and injects its value directly as the `src` of a dynamically created `<script>`
element:
`scriptEl.src = url;`
`document.head.appendChild(scriptEl);`

2. **Figure out how to exploit the vulnerability:** The only defence is a
regex that blocks URLs beginning with `http://` or `https://`:
`if (url.match(/^https?:\/\//))` 
This leaves every other URI scheme unblocked. The `data:` URI scheme lets
you embed content directly in a URL without a network request — including
executable JavaScript via `data:text/javascript,<code>`. Because the filter
only checks for `http`/`https`, passing a `data:` URI bypasses it entirely.
The script tag the app creates itself becomes the delivery mechanism, so no
new elements need to be injected manually.

3. **Craft and Submit the Payload:** Navigate to the level URL and set the
fragment to the `data:` URI payload:
`https://xss-game.appspot.com/level6/frame#data:text/javascript,alert(1)`

The app reads the fragment, passes it through the (ineffective) filter, and
appends:
`<script src="data:text/javascript,alert(1)"></script>`

The browser treats the `src` as an inline script resource, executes
`alert(1)` immediately on page load without any user interaction, and solves
the level.