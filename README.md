# ALBot and ALBotA

A python3 Discord bot used to run the Open Source Club's Discord server. The bot is using the [Discord.py rewrite](https://github.com/Rapptz/discord.py/tree/rewrite).

## Features

Current features include:

- Printing the "Hello World" code of different languages
- Compiling code using judge0 api
- Setting the playing text/randomizing from a file
- Echoing a command
- Orange/Blue type chant
- Play music from YouTube in the voice channels
- Assigning roles to members for different projects

Checkout the Issues tab and [TODO.md](TODO.md) for wanted features.

## Getting started

These instructions are for getting the code to run and a bot in a discord server.

### Prerequisites

You will need Python 3 to run the bot. (NOTE the bot is only tested on 3.6 and 3.7).

Then install the requirements using pip3.

```bash
pip3 install -r requirements.txt
```

### Getting a Discord token and inviting bot

TODO

### Setting up config

Create a file named `config.py` and add your discord token

```py
ALBOT_TOKEN  = "PASTE_TOKEN_HERE"
```

### Running the bot

Running the bot is as easy as

```bash
python3 ALBot.py
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for information about contributing to this projects.

## License

This project is licensed under the **MIT** License - see the [LICENSE](LICENSE) for more details.

## Credits

- [Discord.py Examples](https://github.com/Rapptz/discord.py/tree/rewrite/examples)
- [SpueBox repo for how to play music](https://github.com/CarlosFdez/SpueBox)
