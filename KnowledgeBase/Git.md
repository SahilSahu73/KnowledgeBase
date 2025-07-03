# Git Notes and important Commands

## About Git

Git -> It is a version control system (VCS) and works on the principles of Distributed Version Control System (DVCS).
Earlier People had Local VCS and Centralized VCS but they had certain disadvantages which led to the development of DVCS.
Through DVCS clients don’t just check out the latest snapshot of the files; rather, they fully mirror the repository, including its full history. Thus, if any server dies, and these systems were collaborating via that server, any of the client repositories can be copied back up to the server to restore it. Every clone is really a full backup of all the data.


Git in a nutshell [Reference - https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F]

Major difference between git and other VCS is the way Git looks at it's data.
Conceptually, the other VCS store information as a list of file-based changes, they think of the information they store as a set of files and the changes made to each file over time (aka delta-based version control).

Now, Git does't think of or store it's data this way. Instead, it thinks of it's data more like a series of snapshots of a miniature filesystem. Everytime we commit or save the state of our project, Git basically takes a picture of what all your files look like at that moment and stores a reference to that snapshot. To be efficient, if some files are not changed, Git doesn't store the file again, just a link to the previous identical file it has already stored. Git thinks about it's data more like a stream of snapshots.

Nearly every operation is local
Most operations in git need only the local files and resources to operate. Entore history of the project is right there on the local disk so most operation seem almost instantaneous.

Git has Integrity
Everything in git is checksummed before it is stored and then referred to by that checksum. It becomes impossible for us to change the contents of any file or directory without git knowing about it. This functionality is built into git at the lowest levels and is integral to its philosophy.
The mechanism git uses for this checksumming is called SHA-1 hash. 40-characters string composed of hexadecimal characters and calculated based on the contents of a file or directory structure in git.

Git generally only adds Data
When we do any actions in git, nearly all of them only add data to the git database.

The Three States
Git has 3 main states that your files can reside in: **modified**, **staged** and **committed**.
Modified - changed the file but have not committed it to the database yet.
Staged - marked a modified file in its current version to go into your next commit snapshot.
Committed - data is safely stored in your local database.

This leads us to the 3 main sections of a git project: the working tree, the staging area, and the git directory.
The basic Git workflow goes something like this:
    You modify files in your working tree.

    You selectively stage just those changes you want to be part of your next commit, which adds only those changes to the staging area.

    You do a commit, which takes the files as they are in the staging area and stores that snapshot permanently to your Git directory.

## Setting things up on git:
After installing git on my system (Ubuntu) by - 'sudp apt install git-all'
'git config' lets you get and set configuration variables that control all aspects of how Git looks and operates.

My identity
To setup my username and email
git config --global user.name "sahil"
git config --global user.email Sahil.Sahu@esds.co.in

If need any help in git about any command then can use:
git help 'command'
git 'command' --help

eg: git add --help

## Getting started with Git repository

Can obtain a git repo in 2 ways:
1. take a local directory which is not under version control, and turn it into a git repository

navigate to the folder/project directory which you want to VC and then type:
git init

It wil create a new subdirectory '.git' that contains all of your necessary repository files -- a git repository selection.
At this point nothing in your project is tracked yet.
To start version controlling existing files, you should probably begin tracking those files and do an initial commit.

git add . or git add *.c
git commit -m 'Initial Project commit'

2. Cloning an existing repository
test

