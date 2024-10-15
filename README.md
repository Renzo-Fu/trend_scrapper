
# Trend Scrapper

A web scraping project that collects articles from TrendHunter and stores them in a CSV file. The project uses Selenium, BeautifulSoup, and Pandas to scrape and store data.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Project Structure](#project-structure)
4. [Setup Instructions](#setup-instructions)
5. [Running the Project](#running-the-project)
6. [Contributing](#contributing)
7. [License](#license)

## Project Overview

This project is designed to scrape articles from the [TrendHunter](https://www.trendhunter.com/) website. The articles are processed and stored in a CSV file, with detailed information such as title, publication date, references, and article text. It uses a headless Chrome WebDriver for scraping with Selenium and BeautifulSoup to parse the content.

## Technologies Used

- **Selenium**: Web scraping tool for automating browser interactions.
- **BeautifulSoup**: Used to parse HTML and extract data from web pages.
- **Pandas**: Used to store and manipulate the scraped data.
- **Requests**: Used for making HTTP requests to retrieve article pages.
- **Poetry**: Python dependency management tool to handle dependencies and virtual environments.
- **Chrome WebDriver**: For automated web scraping in a headless browser.

## Project Structure

```
trend_scrapper/
│
├── src/                     # Source code for scraping
│   ├── __init__.py           # Empty file to make the folder a package
│   ├── config.py             # Configuration and constants
│   ├── driver_setup.py       # WebDriver setup functions
│   ├── utils.py              # Utility functions (e.g., file I/O)
│   ├── scraper.py            # Scraping logic (main functions)
│   └── main.py               # Entry point (execution)
│
├── notebooks/               # Jupyter/Colab notebooks
│   └── scraping_notebook.ipynb
│
├── requirements.txt         # Project dependencies
│
├── pyproject.toml           # Poetry configuration
│
├── README.md                # Project description and setup instructions
│
└── .gitignore               # Files/folders to ignore (e.g., .ipynb_checkpoints, data/)
```

## Setup Instructions

To set up this project, follow these steps:

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/trend_scrapper.git
cd trend_scrapper
```

### 2. Install Poetry

If you don't have Poetry installed, install it by following the instructions on the official [Poetry website](https://python-poetry.org/docs/#installation).

For example, on Unix-like systems:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Install Dependencies

After cloning the repository, install the required dependencies using Poetry:

```bash
poetry install
```

This command will install all dependencies listed in `pyproject.toml` including:

- `selenium`
- `beautifulsoup4`
- `requests`
- `pandas`

### 4. Set Up WebDriver

Ensure that the Chrome WebDriver is installed on your system. You can download it from [here](https://sites.google.com/chromium.org/driver/). Make sure that the version of the WebDriver matches the version of Chrome installed on your machine.

Once downloaded, either:

- Add the WebDriver path to your system's environment variables.
- Alternatively, specify the path directly in the `set_up_driver()` function in `src/driver_setup.py`.

## Running the Project

To run the scraping script, execute the following command:

```bash
poetry run python src/main.py
```

The script will:

1. Open a headless Chrome browser.
2. Scrape articles from TrendHunter.
3. Store the results in a CSV file named `trendhunter.csv`.

### Viewing the Results

After the script completes, the scraped data will be saved in a CSV file in the project root directory. You can open this file using any spreadsheet application like Excel or use Pandas to load and analyze the data in Python.

## Contributing

Contributions are welcome! If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Make your changes.
4. Commit your changes with clear messages.
5. Push your branch to your fork.
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Author**: Renzo A.
