""" Nutrition app. """

import argparse
from nutrition.app import run_app


def run():
    """ Runs the application. """
    parser = argparse.ArgumentParser(description="Run the nutrition app.")
    # TODO better default handling
    default_config_name = ".nutrition_config"
    parser.add_argument("--config", default=default_config_name, help="path to the config file")

    args = parser.parse_args()
    run_app(args.config)


run()
