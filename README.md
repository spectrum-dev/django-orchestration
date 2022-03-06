# Spectrum (Backend)
## _Orchestration Service_

![django](https://logodix.com/logo/1758961.png)

This reposiory manages the:

- External GraphQL API for the client
- Authentication
- Determining what order to run blocks and assembling requests with the relevant payloads
- Orchestration of different "blocks" into a strategy
- Storing strategies
- Computing strategy analytics

## Installation

Installation has been automated by the [_local-environment-setup_](https://github.com/spectrum-dev/local-environment-setup) repository. Please refer to it for instructions on how to set up your environment!

## Docker

It's super easy to get your Spectrum environment set up!

The best way to use Django commands (like running tests, running the server, creating migrations, etc) is to use the docker-compose file in _local-environment-storage_. 

```sh
cd local-environment-storage
docker-compose run --rm orchestration /bin/bash
<perform any Django CLI functions here>
```

## Development

Want to contribute? Great! Feel free to create PR's for improvements and I will take a look at them as quickly as possible! Forks are also encouraged as well!


## License

MIT
