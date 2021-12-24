# Features

This API has a variety of end-points for different features. For more detailed information, check out the [API docs](https://api.botish.xyz/docs).

Here are some of the features:

## Jokes

End-points for getting jokes.

- `GET /jokes/all`
  ```bash
  curl -X 'GET' \
    'http://127.0.0.1:8000/jokes/all' \
    -H 'accept: application/json'
  ```
  Response body:
  ```json
  {
    "jokes": [
      {
        "id": 0,
        "joke": "Can February march? No, but April may."
      },
      {
        "id": 1,
        "joke": "I cut my finger chopping cheese, but I think that I may have grater problems."
      },
      .
      .
      .
  }
  ```
- `GET /jokes/{joke_id}`
  ```bash
  curl -X 'GET' \
    'http://127.0.0.1:8000/jokes/0' \
    -H 'accept: application/json'
  ```
  Response body:
  ```json
  {
    "joke": "Can February march? No, but April may.",
    "id": 0
  }
  ```
- `GET /jokes?num=<n:int>` (num=1, by default)
  Gets `num` random jokes
  ```bash
  curl -X 'GET' \
    'http://127.0.0.1:8000/jokes?num=1' \
    -H 'accept: application/json'
  ```
  Response body:
  ```json
  {
    "jokes": [
      {
        "id": 60,
        "joke": "Did you hear about the kidnapping at school? It's fine, he woke up."
      }
    ]
  }
  ```

## Quotes

End-points for getting quotes.

- `GET /quotes/all`
  ```bash
  curl -X 'GET' \
    'http://127.0.0.1:8000/quotes/all' \
    -H 'accept: application/json'
  ```
  Response Body:
  ```json
  {
    "quotes": [
      {
        "id": 0,
        "quote": "Life isn’t about getting and having, it’s about giving and being.",
        "author": "Kevin Kruse"
      },
      .
      .
      .
    ]
  }
  ```
