# Spectrum (Backend)
## _Orchestration Service_

<img src='https://camo.githubusercontent.com/d4d20d5aec9e28160c88c042ef37001b754a9ff5b30bb790164ed3fddb9e9b51/687474703a2f2f7777772e69636f6e617263686976652e636f6d2f646f776e6c6f61642f6937333032372f636f726e6d616e7468653372642f706c65782f4f746865722d707974686f6e2e69636f' width='50'> <img src='https://logodix.com/logo/1758961.png' width='50'>

This reposiory manages the:

- External GraphQL API for the client
- Authentication
- Determining what order to run blocks and assembling requests with the relevant payloads
- Orchestration of different "blocks" into a strategy
- Storing strategies
- Computing strategy analytics

## Installation

Installation has been automated by the [_codex_](https://github.com/spectrum-dev/codex) repository. Please refer to it for instructions on how to set up your environment!

## Docker

It's super easy to get your Spectrum environment set up!

The best way to use Django commands (like running tests, running the server, creating migrations, etc) is to use the docker-compose file in _codex_. 

```sh
cd codex
docker-compose run --rm orchestration /bin/bash
<perform any Django CLI functions here>
```

## Development

Want to contribute? Great! Feel free to create PR's for improvements and I will take a look at them as quickly as possible! Forks are also encouraged as well!


## License

MIT
