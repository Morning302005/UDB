# Rate Limiter Using Python and Redis

## Overview
This project implements a rate limiter using Python and Redis. It controls the number of requests a client can make within a specified time interval.

## Algorithm
Sliding Window Log Algorithm

## Data Model
Redis Sorted Set (ZSET)

## Configuration
- Maximum requests: 5
- Time window: 60 seconds
- Database: Redis
- Language: Python

## Working Principle
The system identifies a client using a unique ID and stores the timestamp of each accepted request in Redis.

Before processing a new request, expired timestamps are removed. The remaining requests are counted, and the new request is accepted if the count is below the configured limit. Otherwise, it is rejected.

## Features
- Request tracking by client ID
- Sliding time-window validation
- Redis-based request storage
- Automatic removal of expired requests
- Rejection of requests exceeding the limit
- Approximate retry time calculation

## Requirements
- Python 3
- Redis server or Redis-compatible server (Memurai)
- Python Redis library

## Installation

```bash
pip install -r requirements.txt
```

## Execution

```bash
python rate_limiter.py
```

## Example
The first five requests are accepted. The sixth and seventh requests are rejected when they are sent within the same 60-second time window.

## Limitations
- Uses a locally running Redis-compatible database.
- Requests are simulated rather than received through an HTTP API.
- The request limit and time window are statically configured.
- A large number of requests may increase storage usage.

## Conclusion
This project demonstrates the implementation of a rate limiter using Python and Redis. The Sliding Window Log algorithm ensures that requests are controlled within a specified time window while Redis provides fast storage and retrieval of request timestamps.
