In this project we want to create an app called Obsidia which will focus on CaseFileManagement and extend into other features as we build onto it. Eventually it will include a separate project for the frontend of Obsidia.

## Getting Started - Dev Setup
The steps to get setup can be summarized as:
1. Clone the repo: `git clone https://github.com/BlackEdgeConsulting/Obsidia.git`
2. [Setup the virtual environment](#setup-the-virtual-environment)
3. [Install the dependencies](#install-the-dependencies)
4. [Create a branch](#create-branch)
5. Do the work
6. [Make a Pull Request](#make-a-pr) into remote branch `develop`


### Setup the Virtual Environment
You will want to use `venv` to manage your python environment. Example:
```sh
python3 -m venv .venv # This will create a directory called `.venv`

# Run whichever command fits for your Operating System
source .venv/bin/activate # On MacOS/Linux
source .venv/Scripts/activate # On Windows

# IF YOU WANT TO DEACTIVATE THE VENV
deactivate
```

### Install the dependencies
Your should see your terminal display the `(venv)` once activated

### Create Branch
Name your branches in a way that explains what they're for, i.e. if it's a feature then call it `feature-a-thing-that-does-stuff`, if it's a hotfix then call it `hotfix-it-fixes-a-thing`.

You don't have to use `git flow` but [this is a good reference](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) for branch naming.

### Make a PR
After you've pushed the branch to github then go in and create a Pull Request to pull your branch into `develop`.