# Underground chat
Console program for connecting chat and saving chat history.

## Environment variables

Part of the project settings is taken from the environment variables. To define them, create a `.env` file next to python files and write data there in the following format: `VARIABLE=value`.

There are 3 variables available:
- `HOST` - Connection host used to connect.
- `CHAT_PORT` — Connection port used to connect `reader.py`.
-  `FILE_PATH` - Saved chat history file.
- `WRITER_PORT` - Connection port used to connect `writer.py`.
- `TOKEN` - Your personal account hash

## Launch

You will need Python 3 to run the site.

Download the code from GitHub. Install dependencies:

```
pip install -r requirements.txt
```

## reader.py

The script starts viewing the chat and saving the history to a file.

Launch
```
python reader.py
```
for show help info launch `python reader.py -h`

## writer.py
The script allows you to send a message to the chat.<br>
If you are writing to the chat for the first time, you will be assigned the username `anonymous`.

Launch
```
python reader.py <your massege>
```
for show help info launch `python writer.py -h`
