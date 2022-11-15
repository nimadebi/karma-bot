#!/bin/bash

# get current path
CURRENT_PATH=$(pwd)

# create necessary directory for ol tool to function
[ ! -d "~/.0L" ] && mkdir ~/.0L

# copy the ol tool config file
cp $CURRENT_PATH/assets/0L.toml ~/.0L

# make the ol tool executable
chmod +x $CURRENT_PATH/bin/ol

# add the path of the ol tool to the PATH variable. 
# This should be done every time you logout and login
# again. To prevent this, you can add this line at
# the bottom of the .bashrc file in your home dir.
export PATH="$CURRENT_PATH/bin:$PATH"
