""" Nutrition app. """

import argparse
from nutrition.app import main


def run():
    """ Runs the application. """
    parser = argparse.ArgumentParser(description="Run the nutrition app.")
    # TODO better default handling
    default_config_name = ".nutrition_config"
    parser.add_argument("--config", default=default_config_name, help="path to the config file")

    args = parser.parse_args()
    main(args.config)


run()
