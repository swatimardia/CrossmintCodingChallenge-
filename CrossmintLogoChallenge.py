import asyncio
from http import HTTPStatus
from typing import List, Optional
import aiohttp
from aiolimiter import AsyncLimiter
import MegaverseApi
from MegaverseBodies import Cometh, Soloon, Polyanet, MegaverseBody

SEMAPHORE_VALUE = 3  # number of api calls made simulaneously
ASYNC_LIMITER_VALUE = 3  # number of api calls per second


async def _getMegaverseBody(goalMapUnit: str, row_idx: int, col_idx: int) -> MegaverseBody:
    megaverse_arr = goalMapUnit.split("_")
    if len(megaverse_arr) == 2:
        if megaverse_arr[1] == str(MegaverseApi.MEGAVERSE_BODIES.COMETH):
            return Cometh(row_idx, col_idx, megaverse_arr[0].lower())
        elif megaverse_arr[1] == str(MegaverseApi.MEGAVERSE_BODIES.SOLOON):
            return Soloon(row_idx, col_idx, megaverse_arr[0].lower())
    elif len(megaverse_arr) == 1 and megaverse_arr[0] == str(MegaverseApi.MEGAVERSE_BODIES.POLYANET):
        return Polyanet(row_idx, col_idx)

async def getGoalMap(candidateId) -> Optional[List[List[str]]]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(MegaverseBody.getUrl() + "/map/" + candidateId + "/goal") as resp:
                resp = await resp.json()  # cant get goal map
                return resp['goal'] if 'goal' in resp else None
    except Exception as e:
        # log exception e to logger ideally, currently printing to terminal
        print(str(e))
        return None


async def createCross(limiter, semaphore, goalMap: List[List[str]], candidateId) -> None:
    if not goalMap:
        return None

    async with aiohttp.ClientSession() as session:
        tasks = []
        for row_idx, row in enumerate(goalMap):
            for col_idx, unit in enumerate(row):
                megaverse_body = _getMegaverseBody(unit, row_idx, col_idx)
                if megaverse_body:
                    tasks.append(asyncio.ensure_future(MegaverseApi.addMegaverseBody(megaverse_body, session, semaphore, limiter, candidateId)))
        while tasks:
            responses = await asyncio.gather(*tasks)
            remaining_tasks = []
            for task, response in zip(tasks, responses):
                if response[0] == HTTPStatus.TOO_MANY_REQUESTS:
                    remaining_tasks.append(task)
            tasks = remaining_tasks


async def resetMap(limiter, semaphore, goalMap: List[List[str]], candidateId) -> None:
    if not goalMap:
        return None

    async with aiohttp.ClientSession() as session:
        tasks = []
        for row_idx, row in enumerate(goalMap):
            for col_idx, unit in enumerate(row):
                megaverse_body = _getMegaverseBody(unit, row_idx, col_idx)
                if megaverse_body:
                    tasks.append(asyncio.ensure_future(MegaverseApi.deleteMegaverseBody(megaverse_body, session, semaphore, limiter, candidateId)))
        while tasks:
            responses = await asyncio.gather(*tasks)
            remaining_tasks = []
            for task, response in zip(tasks, responses):
                if response[0] == HTTPStatus.TOO_MANY_REQUESTS:
                    remaining_tasks.append(task)
            tasks = remaining_tasks


def main(candidateId, createOrResetCrossMap):
    limiter = AsyncLimiter(ASYNC_LIMITER_VALUE, 1)
    semaphore = asyncio.Semaphore(value=SEMAPHORE_VALUE)
    goalMap = asyncio.run(getGoalMap(candidateId))
    if createOrResetCrossMap:
        asyncio.run(createCross(limiter, semaphore, goalMap, candidateId))
    else:
        asyncio.run(resetMap(limiter, semaphore, goalMap, candidateId))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Crossmint Coding Challenge')
    parser.add_argument('--candidateId', required=True, type=str,
                        help='Please input your candidate ID.')
    parser.add_argument('--createOrResetCrossMap', required=True, type=int,
                        help='1 if you want to create cross map, or 0 if you reset the crossmap to original.')
    args = parser.parse_args()
    main(candidateId=args.candidateId, createOrResetCrossMap=args.createOrResetCrossMap)