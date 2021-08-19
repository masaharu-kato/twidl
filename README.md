# TwiDL
Twitter tweets downloader

## Setup
1. Prepare a python virtualenv:  
   `python3 -m venv env` (Use python3.8 or later)
1. Enter to the virtualenv:  
   `. env/bin/activate`
1. Install this app (and the all dependencies):  
   `pip install -e .[dev]`  
   (In the production, `pip install .`)

## Preparation of setting files
### Configurations directory
- `/conf.default`  
   Default configuration files (templates, git managed)
- `/conf`
   Actual configuration files (gitignored)

### List of the configuration files
- `apikeys.json`    
   API keys
