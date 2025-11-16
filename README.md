# Computer Infrastructure

Course project for the course **Computer Infrastructure** - Higher Diploma in Science in Computing in Data Analytics, ATU Galway Mayo (IE). 

## About this repository

### The project

The code in this repository automatically downloads and plots financial data from [Yahoo Finance](https://finance.yahoo.com/) using the Python library [yfinance](https://ranaroussi.github.io/yfinance/). 

### Getting started 

- **Use a codespace**: To avoid compaitibility issues, it is recommended to use MacOs or codespaces, when the code is executed. [VERIFY]

- **Clone the repository**: Clone this repository using the HTTPS link (for more information, see [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)). 

- **Install python 3.12**: If it's not installed on your machine or virtual environment, install python 3.12: https://www.python.org/downloads/. 

- **Install the dependencies**: run *pip install -r requirements.txt* to install all the required libraries at once, or *pip install \*library name\* to install individual libraries. 

### Inside this repository 

The repository strucrure should include the following files. 

├── data\
├── roughwork [TO REMOVE]\
│   ├── notes.ipynb\
├── .gitignore\
├── problems.ipynb\
├── README.md\
├── requirements.txt\
├── stocks.py\


The main code is included in [stocks.py](stocks.py), the data is saved in the folder data. A detailed exaplantion of how the project was set up an developed is included in [problems.ipynb](problems.ipynb).

## Problems 

This sections includes a breakdown of the components in this repository. Every component has been developed and detailed in problems.ipynb, and later transferred to stocks.py to automated the execution of the code. 

### 1. Data from yfinance
Yfinance is used to download data from Yahoo Finance and save it in the folder "data". The data is renamed with a timestamp. At the moment, the code downloads data from the *past 5 days* for the *FAANG stocks*(Facebook, Apple, Amazon, Netflix, Google), but the code can be adjusted to modify these parameters. 

### 2. Plotting the data 
The latest data is read with Pandas, and the closing price for each stock is plotted to highlight significant variations (over the past 5 days). 

### 3. 

### 4. 

## References 

yfinance: https://ranaroussi.github.io/yfinance/


