# Good Girl Bot

Good Girl Bot is a Telegram bot that sends encouraging and supportive messages. It interacts with users through commands, inline buttons, and scheduled messages. The bot logs updates and stores data in MongoDB for persistent tracking of chats and user interactions.

## Features

- **Good Girl Messages:** Sends random "good girl" messages combined with positive emojis.
- **Praise Messages:** Delivers customized praise with inline buttons allowing users to request more praise.
- **Scheduling:** Uses a job queue to schedule messages at randomized intervals.
- **Logging and Updates:** Saves every update to the database and logs message details for auditing.
- **Database Operations:** Implements MongoDB operations to manage active chats and message logs.

## Project Structure

- **goodGirlBot.py:** Main entry point; sets up and runs the Telegram bot.
- **messages.py:** Contains command handlers and functions for sending messages and handling button presses.
- **logger.py:** Configures logging for both file and console output.
- **db.py:** Implements MongoDB connectivity and operations including migrations and CRUD actions.
- **utils.py:** Provides utility functions such as selecting random good girl emojis.
- **kehut.txt:** Contains a list of positive praise phrases used when sending messages.
- **good_responses.txt:** (currently empty) Can be used to store additional responses if needed.
- **README.md:** This file.

## Prerequisites

- Python 3.7 or above
- A Telegram Bot token (obtained from BotFather)
- MongoDB server running locally or accessible via network
- Required Python packages:
    - python-telegram-bot
    - pymongo

## Installation

1. Clone this repository.
2. Configure your bot token in `goodGirlBot.py` by replacing the placeholder.
3. Install the required packages:
     ```
     pip install python-telegram-bot pymongo
     ```
4. Ensure MongoDB is running on your machine or update the connection string in `db.py` if using a remote database.

## Usage

Run the bot by executing the main script:
```
python goodGirlBot.py
```
The bot will start polling for updates. When a user sends the `/start` command, it will initialize scheduling for that chat. Other commands include `/praise` and `/goodgirl` to manually receive messages.

## Contributing

Feel free to open issues or submit pull requests regarding bugs, feature requests, or documentation improvements.

## License

This project is provided under the MIT License.

Happy coding and keep spreading positivity!