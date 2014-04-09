python freeze.py
git branch -D gh-pages
git checkout -b gh-pages
git add .
git commit -m "Deploying to github server"
git push -f origin gh-pages
