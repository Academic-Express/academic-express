#!/bin/bash

github_langs="python,javascript,java,go,ruby,php,swift,typescript,c,cpp,csharp,scala,kotlin,shell,rust,perl"
github_periods="daily,weekly,monthly"

echo "Crawling arXiv e-prints..."
python -m crawler.arxiv --catchup --save

echo "Crawling GitHub..."
python -m crawler.github --lang ${github_langs//,/ } --since ${github_periods//,/ } --save

echo "Syncing crawled data..."
python manage.py syncarxiv
python manage.py syncgithub
