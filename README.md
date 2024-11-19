# project Platform
This was a group project for INF-2900: Software Engineering. The project was to create a general social media platform.

## Overview

- [How to run](#how-to-run)
- [Virtual enviroment](#Virtual-enviroment)
    - [Virtual enviroment on Ubuntu](#virtual-enviroment-on-ubuntu)
    - [Virtual enviorment on Windows](#virtual-enviroment-on-windows)
- [GitHub branch rules](#github-branch-rules)
- [Client specifics](#client-specifics)
    - [Necessary Node.js packages](#necessary-nodejs-packages)
- [Server specifics](#server-specifics)

## How to run
To run the project you'll need two terminals, one for the client and one for the server.
Start by navigating to `PS \Team15>`, from here you'll activate the [virtual enviroment](#Virtual-enviroment). Now that your virtual enviroment is running, you'll navigate to `PS \Team15\projectPlatform>` and run `python .\manage.py runserver`, now the server is running on `localhost:8000` and you should see incoming requests and errors in the terminal. Open up a new terminal and navigate to `PS \Team15\client>`. Here you'll run `npm start` which will initiate the client on `localhost:3000`, you can open up a browser of your choice and head to `localhost:3000/` in your browser to see the webpage.

> [!IMPORTANT]
> npm version: `9.8.1`
> node version: `v18.18.0`
> Check Team15/requirements.txt regarding python libraries. Although there might be some libs missing!

You will need a `.env.local` file in the `client/` directory, here is an example of one that should work:
```
HOST=localhost

BACKEND_PORT=8000
FRONTEND_PORT=3000

REACT_APP_API_URL=http://127.0.0.1:8000

FULLCHAIN=
PRIVKEY=
```

## Virtual enviroment
> [!WARNING]
> Do not push the virtual enviroment!

1. To avoid pushing the virtual environment, create a `.gitignore` file:
2. Open the `.gitignore` file in a text editor.
3. Add a line to ignore the virtual environment directory. If your virtual environment directory is named 'venv', you would add the following line:
    ```
   venv/
    ```
4. You can add the '.gitignore' file it self to avoid pushing it

Install virtual enviroment with the follwing commands:

```
PS \Team15> python -m venv venv
PS \Team15> venv/Scripts/activate
(venv) PS Team15> pip install -r requirements.txt
```

> [!NOTE]
> On Windows, the directory is named `Scripts`, while on Ubuntu its `Bin`.

and then when you're done and ready to push, type:

```
(univenv) PS \Team15> pip freeze 
```

which will print through the terminal which lib's are neccessary for the project. Replace the `requirements.txt` with the terminal print.

> [!IMPORTANT]
> Freezing the libraries allows for others to maintain the neccessary libraries.

Then deactivate the virtual enviroment with:

```
(venv) PS \Team15> deactivate
```

### Virtual enviroment on Ubuntu
1. Install venv package:
    ```
    apt install python3-venv
    ```
2. Inside the project directory:
    ```
    python3 -m venv venv
    ```
3. Activate the virtual envirment:
    ```
    source venv/bin/activate
    ```

### Virtual enviroment on Windows
> [!TIP]
> Change the execution policy settings in PowerShell to allow virtual enviroments to run.

PowerShell might cause you some trouble when you're trying to activate the scripts, here's how to fix that:

```
PS \Team15> get-ExecutionPolicy
```

This command will most likely tell you that the current execution policy is restricted. Lets change that:

```
PS \Team15> Set-ExecutionPolicy Unrestricted -Scope Process
```

Now we've set the execution policy to unrestricted for processes, which is generally a safe solution. If you're still having trouble, see [Stack Overflow - 'virtualenv' won't activate on Windows](https://stackoverflow.com/a/18713789).

## GitHub branch rules
> [!IMPORTANT]
> Do not create merge conflicts!

- Create a branch to develop assigned features. Create a pull request if you want to change something that isn't yours.
- Check with others before you push anything to any branch that isn't yours alone.
- Do not push to the main branch without consulting the entire group.
- Always fetch before you push.
- Double check that you're not implementing something in a file others may implement too.

## Client specifics
To run the client, you'll need [Node.js](https://nodejs.org/dist/v20.11.1/node-v20.11.1-x64.msi) and npm. You can check if they're installed with:
```
PS > node -v
```
and
```
PS > npm -v
```
npm usually comes with Node.js, but if it didn't, you can install it with:
```
PS > npm install -g npm
```
To run the development server for the client, you'll have to install the `node_modules`. To do this, `cd` into the `/client` directory and do:
```
PS Team15\client> npm install
```
This will install all dependencies defined in the `package.json`. Now that you've got the modules to run the server, you can go ahead and write `npm run`, which will initiate the React.js project at `localhost:3000`.

## Server specifics
To run the server, you'll have to install Django with:

```
PS > pip install Django
```

Now that Django is installed, you're ready and set to run the server. Though you might need the other dependencies, which can be activated through a [virtual enviroment](#Virtual-enviroment).
