#!/usr/bin/python3

from coinbase.wallet.client import Client
import argparse
import json
import os
import sys
import time
import logging
from logging import INFO, DEBUG

DEFAULT_CACHE_LOCATION = "/tmp/cryptofetch_cache.json"
DEFAULT_CACHE_EXPIRY_SECONDS = 60
DEFAULT_COINS_MAP = os.path.expanduser("~/.config/polybar/coins.svg")


def format_rate(rate, round_to, thousand):
    round_offset = 0
    if thousand:
        rate = rate / 1000
        round_offset = 3
    rate = round(rate, -round_to + round_offset)
    return f"{rate:,}{'K' if thousand else ''}"


def retrieve_rate_from_data(data, coin, base, round_to, thousands, unicode_map):
    rates = data.get("rates", {})
    coin_price = rates.get(coin.upper(), None)
    base_price = rates.get(base.upper(), None)
    if coin_price is not None and base_price is not None:
        formatted_rate = format_rate(
            float(base_price) / float(coin_price), round_to, thousands
        )
        unicode_coin = unicode_map.get(coin.lower(), None)
        unicode = chr(int(unicode_coin, 16)) if unicode_coin else ""
        return f"{unicode} {formatted_rate}"
    return None


def load_unicode_map(path):
    if not os.path.exists(path):
        raise FileNotFoundError("No coins.svg file was found")
    unicode_map = {}
    with open(path, "r", encoding="utf-8") as icons:
        for line in icons:
            unicode, coin = line.strip().split(":")
            unicode_map[coin] = unicode
    return unicode_map


def main():
    parser = argparse.ArgumentParser(prog="cryptofetch")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--api-key", type=str, help="Coinbase API Key", required=True
    )
    parser.add_argument(
        "--api-secret", type=str, help="Coinbase API Secret", required=True
    )
    parser.add_argument(
        "--coin", type=str, default="BTC", help="Coin to fetch price on"
    )
    parser.add_argument(
        "--base",
        type=str,
        default="USD",
        help="Currency base to convert against",
    )
    parser.add_argument("--round", type=int, default="1", help="Round")
    parser.add_argument(
        "-k", "--thousands", action="store_true", help="Format in thousands"
    )
    parser.add_argument(
        "--cache",
        type=str,
        default=DEFAULT_CACHE_LOCATION,
        help="Cache file location",
    )
    parser.add_argument(
        "--cache-expiry-seconds",
        type=int,
        default=DEFAULT_CACHE_EXPIRY_SECONDS,
        help="How long the cache is valid for",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Forces an API call regardless of the last cached prices",
    )
    parser.add_argument(
        "--coin-unicode-map",
        type=str,
        help="Unicode map for coin icons",
        default=DEFAULT_COINS_MAP,
    )

    args = parser.parse_args()

    coin = args.coin
    base = args.base
    cache_location = args.cache
    cache_expiry_seconds = args.cache_expiry_seconds
    round_to = args.round
    thousands = args.thousands
    api_key = args.api_key
    api_secret = args.api_secret
    verbose = args.verbose
    no_cache = args.no_cache
    coin_unicode_map_path = args.coin_unicode_map
    logging.basicConfig(level=DEBUG if verbose else INFO)

    now_time = int(time.time())

    cache_data = {}
    if os.path.exists(cache_location):
        logging.debug(f"Cache found at {cache_location}")
        with open(cache_location, "r") as cache:
            cache_data = json.load(cache)

    cache_timestamp = cache_data.get("timestamp", 0)

    unicode_map = {}
    try:
        unicode_map = load_unicode_map(coin_unicode_map_path)
    except FileNotFoundError:
        logging.debug("Coins map wasn't found, ignoring...")

    # If the cache hasn't expired yet, then try to read from the cache
    if now_time - cache_timestamp < cache_expiry_seconds and not no_cache:
        logging.debug(
            f"Cache has timestamp {cache_timestamp}, trying to read from it",
        )
        rate = retrieve_rate_from_data(
            data=cache_data,
            coin=coin,
            base=base,
            round_to=round_to,
            thousands=thousands,
            unicode_map=unicode_map,
        )
        if rate is not None:
            sys.stdout.write(rate)
            sys.exit(0)

    logging.debug("Cache expired or forced no cache, making API call")
    # Otherwise, make the Coinbase API call
    client = Client(api_key, api_secret)
    data = client.get_exchange_rates()

    # Set timestamp
    data["timestamp"] = now_time
    with open(cache_location, "w") as cache:
        json.dump(
            data,
            cache,
            indent=4,
        )
    rate = retrieve_rate_from_data(
        data=data,
        coin=coin,
        base=base,
        round_to=round_to,
        thousands=thousands,
        unicode_map=unicode_map,
    )
    if rate is not None:
        sys.stdout.write(rate)
        sys.exit(0)

    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f'cryptofetch script fail\n{e}')
