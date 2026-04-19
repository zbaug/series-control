## Series Control REPL
---
### Description
A terminal-based REPL tool to manage and rate TV series of your own preference.

### Table of Contents
- [Showcase](#showcase)
- [Features](#features)
- [Installation](#installation)
  - [From PyPI](#from-pypi)
  - [From source](#from-source)
- [Usage](#usage)
- [OMDb API Key](#omdb-api-key)
- [Contributing](#contributing)

### Features
* Add series and organize them by seasons and episodes
* Rate episodes individually or all at once (0 to 10, up to 2 decimal places)
* View a color-coded ratings table by episode and season
* Compare two series side by side
* Import IMDb ratings via the OMDb API
* Data is saved automatically in a local JSON file

### Install
Requires [Python 3.10+](https://www.python.org/downloads/) and [pipx](https://pipx.pypa.io/stable/installation/).

#### From PyPI
```bash
pipx install serctl
```

#### From source
```bash
git clone https://github.com/tu-usuario/serctl.git
cd serctl
pipx install -e .
```

### Usage
Run the program with:
```bash
serctl
```
Then use any of the available commands:
| Command | Description |
|---------|-------------|
| `ns` | Add a new serie |
| `as` | Add seasons to a serie |
| `ams` | Add more seasons to an existing serie |
| `es` | Eliminate a serie |
| `prte` | Rate a specific episode |
| `ra` | Rate all episodes from a serie |
| `ss` | See all series |
| `ser` | See episode ratings table |
| `cs` | Compare two series side by side |
| `setkey` | Save your OMDb API key |
| `exit` | Exit the program |

Type help inside the program to see all commands, and - at any prompt to return to the command box.

### Uninstall
```bash
pipx uninstall serctl
```

### Dependencies
| Package | Version |
|---------|---------|
| [InquirerPy](https://github.com/kazhala/InquirerPy) | >=0.3.4 |
| [platformdirs](https://github.com/platformdirs/platformdirs) | >=4.0.0 |

### OMDb API Key
The `cs` command supports IMDb ratings via the OMDb API. To use it, get a free key at omdbapi.com/apikey.aspx and save it with the setkey command (Free version should be enough for personal usage).

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.
