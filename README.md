# RabbitMQ Subscriber for Picture Segmentation

This is a Python project that subscribes to a RabbitMQ queue and waits for messages containing picture IDs. The picture is downloaded from a MongoDB database and then segmented. The segmented picture is saved back to the MongoDB database.

## Installation

This project can be run using either Poetry or Docker.

### Using Poetry

1. Install [Poetry](https://python-poetry.org/docs/#installation) on your system.
2. Clone this repository to your local machine.
3. Navigate to the project root directory.
4. Run `poetry install` to install the project dependencies.

### Using Docker

1. Install [Docker](https://docs.docker.com/get-docker/) on your system.
2. Clone this repository to your local machine.
3. Navigate to the project root directory.
4. Build the Docker image by running `docker build -t rabbitmq-subscriber .`.

## Configuration

Before running the project, you will need to set up the config file `image_segmentation/config.py` and set up environment variables, have a look at file `.env.template`


## Usage

### Using Poetry

1. Activate the virtual environment by running `poetry shell`.
2. Start the subscriber by running `python program/main.py`.

### Using Docker

1. Start the subscriber by running `docker run -it rabbitmq-subscriber`.

The subscriber will start listening to the RabbitMQ queue and waiting for messages. When a message containing a picture ID is received, it will download the picture from the MongoDB database, segment it using the segmentation model specified in the configuration file, and then save the segmented picture back to the MongoDB database.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
