import yaml
import argparse

__config = None


def configuration():
    global __config
    if not __config:
        with open('../config.yaml', mode='r') as config_file:
            __config = yaml.load(config_file, Loader=yaml.FullLoader)
    return __config


def main():
    parser = argparse.ArgumentParser()

    news_sites = list(configuration()['news_sites'].keys())

    print(news_sites)


main()
