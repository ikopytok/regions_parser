regions_parser
==============================

Parse Rosstat socio-eoconomic indicators from special appendix (https://rosstat.gov.ru/folder/210/document/47652).

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── section.py  <- Parse xlsx and save to CSV.
    │   │   └── comment.py  <- Find and parse footnotes and comments from specific sheet.
    │   │   └── indicator.py  <- Find and parse info about indicator from specific sheet.
    │   │   └── objects.py  <- Find and parse info about regions from specific sheet.
    │   │   └── periods.py  <- Find and parse info about years from specific sheet.
    │   │   └── regions_etalon.yaml  <- Dict with regions info.
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
