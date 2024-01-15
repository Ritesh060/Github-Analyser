# Github-Analyser
To run this repository first download source code and then put your API key in ChatGPT.py.<br>

Then run the GithubAccess file.

## Features:
Oauth Authentication for Github Profile<br><br>
Allowing to chat with the repository<br><br>
Allowing to find out errors and giving the code to fix it <br><br>
Allows long length code <br><br>
Giving out insights and suggestion for the codebase

## Procedure
First I do the Outh process after taking username, then I take the required Repository name. After taking the repository name, I start making prompts and putting them in a main list. This main list starts with saying the repository name and then it goes on to take code of every programming file after labelling them and making prompts for each file and putting it in the main list. If the file exceeds the limit then a block is made and then entered in the next prompt, this allows me to put long codes also into the process. After all the files in the repository is exhausted, the main list is entered into ChatGPT by saving all the inputs in the history of a new chat so its like the chat with those inputs already happened. <br>

Then the user is asked to enter their choice of function, which is:<br>
1. Provide insights and suggestions on the codebase. <br>
2. Enhance code quality and maintainability by suggestions for code refactoring and improvements.<br>
3. Improve code performance by identifying areas for efficiency increase, such as reducing time complexity.<br>
4. Strengthen testing and validation by suggesting additional test cases for better coverage.<br>
5. Identify and fix potential bugs by pinpointing bugs with possible solutions or preventive measures.<br>

Or<br>

Put your own question to ChatGPT about the repository.
