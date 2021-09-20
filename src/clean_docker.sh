#! /bash/sh
cp -r ./data/toLoad ./toLoad
rm -rf ./data
mkdir -p ./data
cp -r ./toLoad ./data
rm -rf ./toLoad
echo "Now pull the (updated) repository from github (using github desktop)."
echo "Start the virtuoso triple store again using \"docker-compose up\"."
echo "Go to \"localhost:8890\" in your browser."
