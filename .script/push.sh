#!/bin/sh
setup_git() {
  git config --global user.email "${GH_EMAIL}"
  git config --global user.name "Travis CI"
  git clone https://${GH_TOKEN}@github.com/IBM/ansible-for-i.git .temp
  cd .temp
}

commit_files() {
  git checkout git-sync
  rm -rf *
  ls -al
  rsync -avu --exclude={'ibm-power_ibmi*.gz','.git','.github','.gitignore','.script','*.FILE','meta','bindep.txt','changelogs','.temp','.travis.yml','ansible.cfg'} ../ .
  git add .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git push --quiet --set-upstream origin git-sync
  cd ..
}

setup_git
commit_files
upload_files
