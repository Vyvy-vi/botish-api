# Making Requests to this API

Here are a few example requests.

> In future this process might change due to addition of Auth.

## Javascript

<details>
    <summary>Expand to view examples of requests using Js</summary>

### With Fetch API
```js
fetch('https://api.heptagram.xyz/jokes/1')
  .then((response) => {
    return response.json()
  })
  .then((data) => {
    // Work with JSON data here
    console.log(data)
  })
  .catch((err) => {
    // Do something for an error here
  })
```

### With axios
```js
const axios = require('axios');

// Make a request for a joke with a give joke_id
axios.get('https://api.heptagram.xyz/jokes/1')
  .then(function (response) {
    // handle success
    console.log(response.json());
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .then(function () {
    // always executed
  });

// If you want to use async-await, add the async keyword to your outer function/method
async function getJoke() {
  try {
    const response = await axios.get('https://api.heptaram.xyz/jokes/1');
    console.log(response.json());
  } catch (error) {
    console.error(error);
  }
}
```
</details>

## Python

<details>
    <summary>Expand to view examples of requests using Python</summary>

### Using requests
```py
import requests

response = requests.get("https://api.heptagram.xyz/jokes/1")
print(response.json())
```

### Using aiohttp (async)
```py
import aiohttp
import asyncio

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.heptagram.xyz/jokes/1') as response:

            data = await response.json()
            print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
</details>
