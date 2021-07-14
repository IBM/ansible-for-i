#!/bin/sh
echo "Starting update github pages"
setup_git() {
  git config --global user.email "${GH_EMAIL}"
  git config --global user.name "Travis CI"
  git clone https://${GH_TOKEN}@github.com/IBM/ansible-for-i.git .website
  cd .website
}

commit_files() {
  git checkout gh-pages-trial
  rm -rf *
  rm -rf .doctrees
  rm -rf _source
  cp -R ../../../gh-pages/. .
  git add .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git push --quiet --set-upstream origin gh-pages-trial
  cd ..
}

setup_git
commit_files
upload_files
