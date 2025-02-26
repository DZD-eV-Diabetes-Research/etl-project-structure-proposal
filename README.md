# DZD ETL Process Design proposal

This is a proposal how one of our ETL Process code could be designed.

## Run

todo

## Development

Requirements:

- Python >= 3.11
- [Python PDM](https://pdm-project.org/latest/) for development ( https://wiki.apps.dzd-ev.org/guides/coding/python-setup )

run `pdm install` to install python modules

### Provide Base Config

create file `src/plisetl/.env` with the following minimal content (adapt `export_example` to your actuall directory that contains your Bitcare DIS Export):

```
PSEUDONYMIZATION_SECRET=123445erfsdverw_secret_string-changeme-in-production
BITCARE_DIS_EXPORT_CSVS_DIR=export_example
```

### Start main

`pdm run src/plisetl/main.py`

### Hints

- if you need to do some scratchbook scripts try create personal directory in `tests/`. have a look at `tests/dev_tim` for an example
