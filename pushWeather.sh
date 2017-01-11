#!/bin/bash

answer=$(curl "http://api.openweathermap.org/data/2.5/weather?q=Minden,de&appid=30afce1037a5a85d1b089f347d2c6580")
curl -X POST -H "Content-Type: application/json" -d "${answer}" http://127.0.0.1:8000/location/weather/add/1/

