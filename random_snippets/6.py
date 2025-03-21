import asyncio
from coordinator import run
from getter import get_connection
from conf import SERVER_IP
from logger import COORDINATOR_LOGGER as LOGGER

async def main():
    previous_engine_status = None
    cursor = None
    conn = None
    error_occurred = False
    while True:
        try:
            conn = await get_connection()
            error_occurred = False
            cursor = conn.cursor()
            query = '''SELECT Engine FROM Settings;'''
            cursor.execute(query)
            engine = cursor.fetchone()[0]
            if previous_engine_status is None or previous_engine_status != engine:
                if engine == 0:
                    LOGGER.info('Engine is not running')
                elif engine == 1:
                    LOGGER.info('Engine is running')
                previous_engine_status = engine
            elif engine == 1:
                await run(cursor=cursor, conn=conn)

        except Exception as e:
            if not error_occurred:
                error_occurred = True  
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

if __name__ == "__main__":
    asyncio.run(main())
