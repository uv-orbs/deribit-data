import asyncio
from dotenv import load_dotenv
from bnnc import start_binance
from drbt import start_deribit
from concurrent.futures import ProcessPoolExecutor

# async def printi(s):
#     print(s)


async def main():
    load_dotenv()
    #executor = ProcessPoolExecutor(2)

    await start_binance(asyncio)
    # a = loop.run_in_executor(executor, start_binance)
    # b = loop.run_in_executor(executor, start_deribit)

    # asyncio.get_event_loop().run_until_complete(start_all())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main()
    loop.run_forever()

    print('DONE!!!')
