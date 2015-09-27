# RuseBackend
The backend server for the Ruse game.

## Setup
Run the setup.sh file:

`$ ./setup.sh`

If you get a permission denied error, you need to give the setup file an execute permission before running it:

`$ chmod a+x setup.sh`

## Developing
After setting up the virtual environment, you can activate it using this command:

`$ source env/bin/activate`

To leave the virtual environment:

`$ deactivate`

## Running
To run the server, ensure that you have activated the virtual environment. Then run the ruse_api.py file:

`$ python ruse_api.py`
