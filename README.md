# cryptofetch
A short Python script fetching cryptocurrency rates from Coinbase meant to be used with Polybar

# Setup
Get your API key and secret from 
[Coinbase](https://www.coinbase.com/settings/api) and place the `coins.svg` 
file in `~/.config/polybar/` or specify the path with `--coin-unicode-map 
<path/to/coins.svg>` and place the `coins.otf` file in `~/.fonts`.

# Usage
```shell
cryptofetch.py --coin ETH --base USD --api-key <API_KEY> --api-secret 
<API_SECRET>
```

## Polybar
If you want to use this with Polybar, add a module
```ini
[module/crypto]
type = custom/script
format = <label>
exec = path/to/cryptofetch.py --coin <COIN> --base USD ...
; Keep in mind the cache expiry is set to 60 seconds by default anyway
interval = 30
```
### Screenshots
![image](https://user-images.githubusercontent.com/22553678/142580339-64244e7e-d73b-4ee8-9a66-eb0e793bf1fd.png)

# Credit
Credit to [polybar-cryptocurrency](https://github.com/plinki/polybar-cryptocurrency) for the coin icons
