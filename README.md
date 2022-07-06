# report-russian-propaganda (telegram only for now)

## Guide
### Requirements:
1. python3 and pip3 installed on your machine

### Instructions:
1. Clone the repository to local machine.
2. Install the requirements via command `pip3 install -r requirements/requirements.txt`
3. Put your telegram api_id and api_hash in `src/config.py` file.
4. To generate api_id and api_hash please visit **https://my.telegram.org/apps**.
5. Go to the telegram and start the bot: **@stopdrugsbot**
6. Run the script (`python3 src/main.py`).

### How it works:
The script will go through the list of telegram channels with russian propaganda provided by **@stopdrugsbot** and report each of them.


## How to add new features

First of all please instal a required dev packages - `pip install -r requirements/requirements-dev.txt`

Next thing is to setup a pre-commit hooks - `pre-commit install`

Once the installation is done, all the files that are changed will be formatted automatically (and commit halted if something goes wrong, e.g there is a syntactic error). You can also run the formatting manually:

```bash
pre-commit run
# or
pre-commit run --all-files
```

If for some reason you'll want to turn the hook off temporarily, you can do that with - `SKIP=flake8 git commit -m "foo"`.

Or you can uninstall it completely with - `pre-commit uninstall`.

To update package versions inside `.pre-commit-config.yaml` - `pre-commit autoupdate`.

