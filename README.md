### Hexlet tests and linter status:
[![Actions Status](https://github.com/DREU007/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/DREU007/python-project-83/actions)
[![Python CI](https://github.com/DREU007/seo-page-analyzer/actions/workflows/pyci.yml/badge.svg)](https://github.com/DREU007/seo-page-analyzer/actions/workflows/pyci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/defcd586c528f7e7849d/maintainability)](https://codeclimate.com/github/DREU007/seo-page-analyzer/maintainability)

### Description
[SEO Page Analyzer](https://seo-page-analyzer-rx3z.onrender.com/) is a web tool to check Serch Engine Optimization support of a given URL.

### Showcase
[![Showcase](/showcase/seo-page-analyzer-showcase.gif)](https://seo-page-analyzer-rx3z.onrender.com/)

### Requirement
* Python
* Poetry
* Postgres

### Installation
**Setting up enviroment**
```bash
git clone https://github.com/DREU007/seo-page-analyzer
cd seo-page-analyzer
make build
```

Configure .env in the root folder
```
cp .env_example .env
```

**Dev**
```bash
make dev
```

**Prod**
```bash
make start
```

*Additional functions are available in Makefile*
