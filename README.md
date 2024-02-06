# LazY - Remote shutdown
Remote shutdown for windows using SSH. Target machine has to have SSH enabled.

You will need to change the host and password in the script.

To get the sleep function to work, this command needs to be first executed once in a administrator terminal:

    powercfg -h off

## Installation

Clone the repository:
     
     git clone https://github.com/Blnix/LazY.git

Install depedencice:

     pip install -r requirements.txt

Run it:

    python LazY.py

### Using it on a phone
I suggest using on android the open-source app [Termux](https://termux.dev/). If you want to have an app, my goto would be [Tasker](https://tasker.joaoapps.com/).
