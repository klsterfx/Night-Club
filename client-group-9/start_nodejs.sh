#!/bin/bash

echo "CURR APP:"$CURR_APP
if [ ! -d "$CURR_APP" ]; then
  echo "CURRENT APP not set, or directory does not exist - nothing to build!"
else
  cd $CURR_APP 
  echo "Create subfolder in gitlab public folder"
  mkdir ../public/$CURR_APP
  npm install
  npm run build
  echo "Copy build folder to gitlab public folder"
  cp -p -r build/* ../public/$CURR_APP 
  echo "Return to the root directory"
  cd ..
fi