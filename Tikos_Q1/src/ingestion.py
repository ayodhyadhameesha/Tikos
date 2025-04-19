import aiohttp
import asyncio
#from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from src.connections.database import collection
from src.config import get_error_logger



logger = get_error_logger()

try:
    
    raise ValueError("Simulated critical error")
except Exception as e:
    logger.error(f"An error occurred: {e}")

##The transformation function gets the raw API data and reshape it and clean it to a consistent structure.
def transform_user(data,source):
    return{
        "user_id": data.get("id"),
        "name": data.get("name"),
        "email": data.get("email"),
        "source": source,
        "timestamp": datetime.utcnow()
    }

# This function fetches data from REST API.Asynchronous functions and libraries are used for much better performance 
async def fetch_rest_users(session):
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            raw_data = await response.json()

            transformed = [transform_user(user, "REST") for user in raw_data]

            if transformed:
                await collection.insert_many(transformed)
                logger.info(f"Inserted {len(transformed)} REST users into MongoDB")
            else:
                logger.warning("No transformed REST data to insert.")
            return transformed
    except Exception as e:
        logger.error(f"REST API fetch failed: {e}")
        return []



# This function fetches data from GraphQL API
async def fetch_graphql_users(session):
    url = "https://graphqlzero.almansi.me/api"
    query = {
        "query": """
        {
          users {
            data {
              id
              name
              email
            }
          }
        }
        """
    }
    try:
        async with session.post(url, json=query) as response:
            response.raise_for_status()
            result = await response.json()
            users = result["data"]["users"]["data"]
            logger.info(f"Fetched {len(users)} users from GraphQL API.")
            return [transform_user(user, "GraphQL") for user in users]
    except Exception as e:
        logger.error(f"GraphQL API fetch failed: {e}")
        return []

# This function fetches all user data from REST API and GraphQL API and returns a single combined list.
async def fetch_all_users():
    async with aiohttp.ClientSession() as session:
        rest_task = fetch_rest_users(session)
        graphql_task = fetch_graphql_users(session)
        rest_data, graphql_data = await asyncio.gather(rest_task, graphql_task)
        return rest_data + graphql_data


if __name__ == "__main__":
    
    logger.info("Running ingestion test")
    all_users = asyncio.run(fetch_all_users())
    logger.info(f"Inserted {len(all_users)} users into MongoDB")
