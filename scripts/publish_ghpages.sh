#!/usr/bin/env bash

# remember current branch name
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# checkout gh-pages branch and copy all files from this branch
# note: code is required because the docs are auto-generated
git checkout gh-pages
git checkout ${BRANCH} -- .

# rebuild documentation
rm -rf docs/build/html/
./scripts/make_docs

# delete all unwanted files and copy html docs to root
rm -rf !(docs)
rm .gitignore
mv docs/build/html/* ./
rm -r docs


git checkout ${BRANCH} -- README.rst

# without this the static files won't be copied to host
touch .nojekyll

# stage all files
git rm -rf --cache .
git add !(.idea|.|..)


# if there were changes push them
if git commit -m "Auto-generated docs from $BRANCH branch"
then
    git push origin gh-pages
fi

# return to initial branch
git checkout ${BRANCH}