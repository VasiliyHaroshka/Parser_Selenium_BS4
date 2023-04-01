# Parser_Slenium-BS4

This parser uses libraries Selenium and Beautiful Soup 4 to take necessary data.
Its work includes in searching adds of bycicles 'Fuji' in Belarus from site 'Kufar.by'. This parser works with browser
Chrome.

To use this parcer:

1) create directory and install virtual environment in it: "python3 -m venv <your_env_name>" (for Linux) or "python -m
   venv <your_env_name>" (for Windows)
2) activate your virtual environment: "source <your_env_name>/bin/activate" (for Linux) or "<your_env_name>
   /Scripts/activate" (for Windows)
3) activate Git in your directory with command: "git init".
4) clone files from this repository to yours with command: "git
   clone https://github.com/VasiliyHaroshka/Parcer_Slenium-BS4.git"
5) install necessary libraries from requirements.txt with command: "pip install -r requirements.txt"
6) download webdriver for Chrome browser from this link: "https://chromedriver.chromium.org/downloads" then extract it
   in directory with the project
7) change path to your webdriver for Chrome in the file main.py: browser = Chrome("<path_to_webdriver>"
   ,options=options) (string 18)
8) launch parser with command: "python main.py"
9) you will get 3 files (“results”) with results of parser's work in .csv, .json and .xlsx format
