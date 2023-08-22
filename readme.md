## Pr0j3ct-EMI
Pr0j3ct-EMI is a script designed to automate the process of placing orders for product on shopee.vn. It helps you avoid having to manually spam order placements. I developed this script in April 2022 for my personal selfish purpose: secure a limited version of the Jujutsu Kaisen manga through a "camping" strategy. I'm now publishing it for educational purpose and will not assume any responsibility for those who utilize it for either profit or non-commercial purposes.

## Features
- Logging in with multiple accounts
- Removing accounts from the list
- Displaying account status (indicating whether an account is currently usable or not)
- Primarily, automatically simultaneously place orders for a product across multiple accounts

## Getting Started
To run Pr0j3ct-EMI, follow these steps:
1. Clone this repository
2. Install Python and its dependencies
3. Install chromedriver for Selenium
4. Run the `main.py` script

## Usage
**1. Logging into an account**  
To add an account, choose `option 2`. If you've logged in before and need to re-login due to and expired session, you can enter the username to avoid entering the OTP again. Otherwise, leave it blank. The Selenium window will open, allowing you to login as usual.  
![](./images/Pasted%20image%2020230822145241.png)

**2. Checking account status**  
Select `option 1` to verify if the account is active  
![](./images/Pasted%20image%2020230822145618.png)

**3. Obtaining item information**  
Navigate to the product page for which you want to place an order. Switch to the Network tab, locate get_pc and copy the content of Response as shown below:  
![](./images/Pasted%20image%2020230822141731.png)
Then paste this data into the `item_data` file located within the folder of the repository.

**4. Automated order placement process**  
Choose `option 4`, select the product model you want, and let Pr0j3ct-EMI "camp" it for you!  
![](./images/Pasted%20image%2020230822152815.png)

The script will repeatedly attempt to place an order until the production becomes available and will display various `error` messages during this process. Once successful, it will display a message like the one shown below:  
![](./images/Pasted%20image%2020230822152505.png)
