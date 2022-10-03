# Technical assignment I

## Specs

The scope of this project consist of two subtasks:
1. to rapidly spin-up and populate the
PosgreSQL database with deleted orders streaming out of [Bitstamp](https://www.bitstamp.net/s/webapp/examples/live_orders_v2.html)'s API.
2. to perform a SQL query to extract some insight out of the last 24 
hours data.

## Plan

To achieve the goal from the requirements, the project is going to
spin up a cluster of 4 microservices:
1. producer service: it fetches the data out of the Bitstamp's 
web-socket, and ingest it to a streaming queue
2. streaming queue, which collects the data and makes it available for consumers
3. consumer service: here we read from the data stream and populate the 
database and aggregates the view.
4. database service: where data is stored for persistance
