<br />
<p align="center">
  <a href="https://github.com/rom1trt/crypto-news-bot">
    <img src="logo.png" alt="Logo" width="700" height="320">
  </a>

  <h3 align="center">Data-driven Trading Bot</h3>

  <p align="center">
    An awesome bot that enables you to trade using SMA, Bollinger-bands, and Machine Learning strategies.
    <br />
    <a href="https://github.com/rom1trt/trading-bot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/rom1trt/trading-bot">View Demo</a>
    ·
    <a href="https://github.com/rom1trt/trading-bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/rom1trt/trading-bot/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#disclaimer">Disclaimer</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Being passionate about financial markets, I decided to create a bot for putting 'virtual' money in work through few strategies and test the efficiency of each one. 
I picked 2 technical analysis tools that I usually use to manually study trading patterns: the Moving Average and Bollinger-bands.

The bot is specifically tailored for some specific strategies. I'll be adding more in the near future. 
You may also suggest changes by forking this repo and creating a pull request or opening an issue.

A list of commonly used resources that I found helpful.

### Built With
* [![Jupyter Notebook](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/)
* [![Anaconda](https://img.shields.io/badge/anaconda-darkgreen?style=for-the-badge&logo=anaconda)](https://www.anaconda.com/)
* [![Python](https://img.shields.io/badge/python-a8a300?style=for-the-badge&logo=python)](https://www.python.org/)

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation

1. Get a free practice account at [Oanda](https://www.oanda.com/eu-en/trading/)
2. Get your account ID at [Oanda](My services -> Manage API Access -> Create API Key)
3. Get your free API Key at [Oanda](Manage funds -> v20 Account Number)
4. Clone the repository
   ```sh
   git clone https://github.com/rom1trt/trading-bot.git
   ```
5. Install python packages (using pip)
   ```sh
   pip install numpy
   pip install pandas
   pip install sklearn
   pip install matplotlib
   pip install --upgrade git+https://github.com/yhilpisch/tpqoa.git
   ```
6. Enter the corresponding API in `config_example.py`
   ```sh
   [oanda]
    account_id = ...-...-........-...
    access_token = ........................-....................
    account_type = practice
   ```
 7. Rename the `oanda.cfg.example.cfg` to `oanda.cfg`
 8. Run the `main.py` file with the strategy you wish 

### DISCLAIMER

    I am not responsible for anything done with this bot.
    You use it at your own risk.
    There are no warranties or guarantees expressed or implied.
    You assume all responsibility and liability.
