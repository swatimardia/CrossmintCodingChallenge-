from typing import Tuple

async def addMegaverseBody(megaverse_body, session, semaphore, limiter, candidateId) -> Tuple[int, str]:
    try:
        async with semaphore:
            async with limiter:
                async with session.post(megaverse_body.getUrl(), json=megaverse_body.getParams(candidateId)) as resp:
                    resp_json = await resp.json()
                    return resp.status_code, resp_json
    except Exception as e:
        # log exception e to logger ideally, currently printing to terminal
        print(str(e))
        return 0, ""


async def deleteMegaverseBody(megaverse_body, session, semaphore, limiter, candidateId) -> Tuple[int, str]:
    try:
        async with semaphore:
            async with limiter:
                async with session.delete(megaverse_body.getUrl(), json=megaverse_body.getParams(candidateId)) as resp:
                    resp_json = await resp.json()
                    return resp.status_code, resp_json
    except Exception as e:
        # log exception e to logger ideally, currently printing to terminal
        print(str(e))
        return 0, ""
