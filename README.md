# cryptofetch
A short Python script fetching cryptocurrency rates from Coinbase meant to be used with Polybar

# Usage
Get your API key and secret from [Coinbase](https://www.coinbase.com/settings/api) and place the `coins.svg` file in `~/.config/polybar/` or specify the path with 
`--coin-unicode-map <path/to/coins.svg>`

```
cryptofetch.py --coin ETH --base USD --api-key <API_KEY> --api-secret <api_secret>
```

# Credit
Credit to [polybar-cryptocurrency](https://github.com/plinki/polybar-cryptocurrency) for the coin icons
