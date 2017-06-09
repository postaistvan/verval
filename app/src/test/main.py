#!/usr/bin/env python
from app.src.dweet import Dweet

if __name__ == "__main__":
    dweet = Dweet()

    # dweet an dweet without a thing name. Returns a a thing name in the response
    # print dweet.dweet({"hello": "world"})

    # dweet with a thing name
    hum = 4
    temp = 1

    print dweet.dweet_by_name(name="madafaka", data={"Humidity": hum, "Temperature": temp})
    # print dweet.dweet_by_name(name="madafaka", data={"hello": "madafaka12"})

    # get the latest dweet by thing name. Only returns one dweet.
    print dweet.latest_dweet(name="madafaka")

    # get all the dweets by dweet name.
    # print dweet.all_dweets(name="madafaka")
