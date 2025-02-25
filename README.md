
# StockFrontend

**StockFrontend** is a Python-based desktop application for stock market data retrieval and analysis. It provides a user-friendly graphical interface to download historical stock data, compute key indicators, and visualize results. The project combines data science libraries with a front-end built in PyQt5 to allow users to interactively fetch and examine stock information.

## Key Features

- **Graphical User Interface (GUI)** – Intuitive desktop interface built with PyQt5 for ease of use ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=pyqt5%20%3D%20)). Users can select options via buttons, date pickers, and input fields instead of using command-line prompts.  
- **Stock Data Retrieval** – Fetches historical stock price data (daily or weekly intervals) using Yahoo Finance API through `yfinance` and pandas data readers ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=pandas%20%3D%20)). Users can specify date ranges (Start Date, End Date) and retrieve data for multiple ticker symbols.  
- **Multi-threaded Download** – Supports multi-core data fetching to speed up downloading large datasets. The application can retrieve data for many stocks in parallel, utilizing Python’s multiprocessing (`joblib`) for efficiency ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=yfinance%20%3D%20)). A **“Get Data”** button initiates the download, and a **“Stop”** button is available to cancel an ongoing download if needed ([stockfrontend/MainWindow.ui at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/MainWindow.ui#:~:text=)).  
- **Data Analysis & Indicators** – Computes key indicators and metrics on the fetched data. For example, the app calculates daily return ratios (e.g., next-day close/open results) and can generate summary statistics. It prepares data tables of open, close, high, low, volume, and derived results for each trading day, which can be viewed in the interface or exported as HTML reports.  
- **Modular Design** – The codebase is organized into modules for different tasks: data fetching (single-thread or multi-thread modes), indicator calculations, and data serialization. This separation makes it easier to maintain and extend functionality (for instance, adding new indicators or data sources).  
- **Local Data Storage** – Retrieved data can be saved locally for caching and offline analysis. The application uses `umsgpack` for efficient binary serialization of data ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=pandas%20%3D%20)). This allows users to build a local database of stock data (optionally updateable via the **“Update”** mode in the UI) without needing to re-fetch unchanged historical data each time.  

## Installation & Setup

1. **Clone the Repository**: Start by cloning the GitHub repository to your local machine.  
   ```bash
   git clone https://github.com/pantoner/stockfrontend.git
   cd stockfrontend
   ```  
2. **Python Environment**: Ensure you have Python 3.7 installed (the project is built and tested with Python 3.7 ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=))). It’s recommended to use a virtual environment. You can use **pipenv** (as a Pipfile is provided) or any environment tool of your choice.  
3. **Install Dependencies**:  
   - **Using Pipenv**: Run `pipenv install` to install all required packages listed in the Pipfile (PyQt5, pandas, pandas-datareader, yfinance, etc.) ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=pyqt5%20%3D%20)) ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=umsgpack%20%3D%20)). This will also ensure the correct Python version is used.  
   - **Using pip**: Alternatively, install dependencies with pip. Since there is no `requirements.txt`, you can manually install the needed libraries:  
     ```bash
     pip install pyqt5==5.9.2 pandas pandas-datareader yfinance umsgpack rolling joblib
     ```  
     *(The above list is derived from the Pipfile; adjust versions if needed.)*  
4. **Run the Application**: After installing dependencies, launch the app by running the `runmain.py` script:  
   ```bash
   python runmain.py
   ```  
   This will open the StockFrontend GUI window on your desktop.

## Usage

Using StockFrontend is straightforward thanks to its GUI design. After launching the application, you will see the main window with various controls:

- **Selecting Date Range**: Choose the **Start Date** and **End Date** for the historical data you want. You can type the dates or use the provided date pickers. A “Today” shortcut button is available to quickly set the end date to the current date ([stockfrontend/MainWindow.ui at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/MainWindow.ui#:~:text=match%20at%20L2366%20)) ([stockfrontend/MainWindow.ui at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/MainWindow.ui#:~:text=)).  
- **Data Frequency**: Select **Daily** or **Weekly** data via the interface (the GUI provides options to toggle between daily and weekly intervals for price data).  
- **Database Name**: (Optional) You may specify a name or path for the local data storage. This can be used to differentiate datasets or choose a target database file if the application supports it. By default, the system will use a standard name defined in the configuration for storing data.  
- **New vs Update**: Choose **“New”** to create a fresh dataset or **“Update”** to append new data to an existing dataset. For a new dataset, the application will fetch all data from the start date; in update mode, it will only fetch data from the last stored date forward to avoid duplication.  
- **Initiating Download**: Click the **“Get Data”** button to start downloading the stock data based on your settings ([stockfrontend/MainWindow.ui at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/MainWindow.ui#:~:text=)). The application will connect to Yahoo Finance (via the internet) and retrieve the historical prices for the specified stocks and time range. If multiple symbols are involved, it will fetch them in parallel to save time. During this process, status messages or progress may be displayed.  
- **Stopping Process**: If you need to cancel the download (for example, if you entered wrong parameters or the process is taking too long), click the **“Stop”** button. This triggers an interrupt that halts the data fetching threads gracefully ([stockfrontend/MainWindow.ui at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/MainWindow.ui#:~:text=)).  
- **Viewing Results**: Once data retrieval is complete, the application will process the data. Depending on the selected analysis tabs, you can view different results:  
  - In the **Describe** tab, you might see summary information or basic statistics about the fetched dataset (e.g. date range, number of records, etc.).  
  - In the **Indicators** tab, the program can display calculated technical indicators or ratios. For instance, it computes daily return ratios (closing price vs opening price) for each day, which may be shown in a table or used to signal trends. Other possible indicators (like moving averages or highs/lows over intervals) can be included here.  
  - In the **Algo** tab, if provided, you could run or view results of any algorithmic analysis. (This might be a placeholder for future enhancements where trading algorithms or predictive models analyze the data.)  

The data table of results (dates, prices, volumes, and computed fields) can be displayed within the app. Under the hood, the application generates an HTML report of the data (as seen in `myhtml2.html`) which is styled for readability ([stockfrontend/myhtml2.html at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/myhtml2.html#:~:text=)) ([stockfrontend/myhtml2.html at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/myhtml2.html#:~:text=)). The interface may show this HTML report directly or allow you to open it in a browser for further examination. You can use this output to inspect the historical prices and any derived metrics for each stock.

Overall, the usage flow is: set parameters → fetch data → view analysis. All interactions are done via the GUI, making it accessible even if you are not comfortable with Python scripting.

## Tech Stack

The project leverages the following technologies and libraries:

- **Python 3.7** – The core programming language used. Chosen for its rich ecosystem in data analysis and GUI development ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=)).  
- **PyQt5 (Qt for Python)** – Used for building the desktop GUI. PyQt5 provides the widgets, windows, and event handling that create the interactive front-end ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=pyqt5%20%3D%20)). The interface (windows, buttons, etc.) was designed using Qt Designer (the file `MainWindow.ui`) and converted to Python code ([stockfrontend/runmain.py at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/runmain.py#:~:text=from%20PyQt5)) ([stockfrontend/runmain.py at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/runmain.py#:~:text=class%20MainWindow)).  
- **Pandas** – Utilized for data manipulation and analysis. Stock price time-series are loaded into Pandas DataFrames for processing (e.g., calculating indicators, sorting by date) ([stockfrontend/tickersymbols.py at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/tickersymbols.py#:~:text=symboldf%20%3D%20symboldf.sort_values%28by%3D)).  
- **Pandas-DataReader** – Helps in fetching financial data from online sources. It works in conjunction with pandas to pull stock data easily ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=pandas%20%3D%20)).  
- **yfinance** – A Python API for Yahoo Finance, used to retrieve historical stock price data including open, close, high, low, and volume ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=pandas%20%3D%20)). This abstracts the web calls to Yahoo Finance and returns data in pandas-friendly formats.  
- **u-msgpack** – A MessagePack serialization library for Python ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=yfinance%20%3D%20)). It is used to store and load stock data efficiently in a compact binary form. This improves the speed of reloading data and reduces storage space compared to CSV or SQL for large datasets.  
- **Joblib & Multiprocessing** – Employed for parallel processing. The application can spawn multiple worker processes to fetch data for different symbols concurrently, taking advantage of multi-core CPUs ([stockfrontend/getcloudmulti.py at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/getcloudmulti.py#:~:text=def%20runmulticore)). Joblib is a convenient library to simplify launching and managing such parallel tasks.  
- **Other Libraries**: The **rolling** library (for rolling window calculations) ([stockfrontend/Pipfile at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/Pipfile#:~:text=yfinance%20%3D%20)) might be used to compute moving averages or rolling metrics for indicators. Standard Python modules like `json`, `sqlite3` (some legacy code for SQLite is present but not actively used), and others are also utilized where appropriate.

## Configuration & Environment Variables

Most configuration is handled via the `config.py` file in the repository. This file contains settings like default values and file paths used by the application. Key configurations include:

- **Default Start Year** – e.g., the variable for the default start year of data (`startyear`) is set to "2019" in `config.py` ([stockfrontend/config.py at master · pantoner/stockfrontend · GitHub](https://github.com/pantoner/stockfrontend/blob/master/config.py#:~:text=sentinal%20%3D%200)). This means if you do not specify a start date in the GUI, the system might default to fetching data from 2019 onward (you can change this in the config if needed).  
- **Data Storage Path** – The application defines a path for raw stock data storage (e.g., `rawstockdatapath` in `config.py`). This is the directory where the fetched data (possibly as MessagePack files or databases) will be saved. Ensure that the path exists or adjust it to a desired location on your system. By default, it may store in a subfolder of the project or a temp directory.  
- **Other Parameters** – A sentinel or flag (`sentinal` variable) is used internally to control processes or state. Typical users do not need to modify this. There might also be configuration for database names or table names (for example, references to a table named "cloud" in the code). These are mostly for internal use and advanced configurations.

No external API keys or environment variables are required for StockFrontend to run. All data is obtained from Yahoo Finance without an API key, thanks to yfinance. Just ensure your internet connection is active when fetching data. If you need to tweak settings (like the data source or add an API key for another data provider), you would do so by modifying the code or adding new config variables. Always restart the application after changing configuration values to ensure they take effect.

## Contributing

Contributions to **StockFrontend** are welcome! If you’d like to improve the project or fix issues, please follow these guidelines:

- **Fork the Repository**: Start by forking the project on GitHub to your own account. Then clone your fork locally to make changes.  
- **Create a Branch**: Create a new branch for your feature or bugfix (e.g., `feature/add-new-indicator` or `bugfix/fix-date-parsing`). This makes it easier to manage and review your changes.  
- **Make Changes**: Implement your feature or fix in the code. Ensure that the GUI remains functional and user-friendly. If you add new dependencies, update the Pipfile (or provide a requirements update). Include documentation for new features either in the README or as separate documentation files as appropriate.  
- **Testing**: Try to test your changes with a variety of stock symbols and scenarios (different date ranges, large data downloads, etc.) to ensure stability and correctness. If possible, add or update any automated tests (if the repository includes tests; if not, manual testing is okay).  
- **Submit a Pull Request**: Push your branch to your fork on GitHub and open a Pull Request against the main repository (`pantoner/stockfrontend`). In the PR description, clearly describe your changes, why they are beneficial, and any steps needed to test them. The maintainers will review your proposal and merge it if everything looks good.  

Feel free to also open issues on the repository’s issue tracker for any bugs you find or suggestions for enhancements. Engaging in discussions can help shape the project roadmap. By contributing, you agree to uphold the project’s coding style and standards. We appreciate your interest in improving StockFrontend!

## License

*This project does not yet specify an open-source license.* As a result, the default copyright provisions apply – the code is © 2025 the author/maintainer of StockFrontend. If you plan to use this project’s code in your own work, please contact the repository owner for clarification or permission. 

It’s recommended that the project adopt a formal license (such as MIT, GPL, etc.) so that others clearly understand usage rights. Until then, please assume that all rights are reserved by the creator.
