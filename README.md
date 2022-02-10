# OLX deal finder
## A python script that monitors a product on OLX and emits an alert if it finds a deal ##

To run, it's required to have all the packages on requirements.txt installed.

```
pip install -r requirements.txt
```

It's also needed to change the server, login, password and port on config.yml. Also on that file, there will be the max amount of pages to be scraped.

![Captura de Tela 2022-02-10 às 18 46 12](https://user-images.githubusercontent.com/22485873/153501820-e0b20dda-eb11-483f-974f-2b6ee97f6f36.png)

To run, you'll need to pass two arguments: first, the link for the first page of the desired product; second, how cheap the product needs to be to be considered a deal.

```
python deal_finder.py {link} {deal}
```
Example:
```
python deal_finder.py "https://rs.olx.com.br/autos-e-pecas/motos/bmw/g/650" "21000"
```
There will be an email alert for every new deal found. Every deal sent will be stored in a SQLite db, so it won't be scraped again.

I apologise to the BMW G650 owners that I inflated the views during development. My bad!
