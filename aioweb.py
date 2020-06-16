import asyncio

import aiomysql

from mgtv import upload_img as ul


def fetch(session, queue):
    pass


async def upload_img(item):
    return await ul(item)

    # while True:
    #     try:
    #         data_dict = queue.get_nowait()
    #         await ul(data_dict)
    #         print(data_dict)
    #     except asyncio.QueueEmpty():
    #         break


async def get_data(offset, count, queue):
    async with aiomysql.create_pool(
        host="27.102.102.96",
        port=3306,
        user="kacker_dy",
        password="3rSPYXxRkcBtd5MD",
        db="kingvstr_dy",
        charset="utf8",
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as corsur:
                sql = (
                    "select v_id, v_pic from sea_data  WHERE v_pic NOT LIKE '%%{}%%' order by v_addtime desc limit %s, %s"
                ).format("alicdn")
                await corsur.execute(sql, (offset, count))
                data_list = await corsur.fetchall()

                data_new_list = []
                for item in data_list:
                    data_new_list.append(await upload_img(item))

                up_sql = "update sea_data set v_pic = %s where v_id = %s"
                try:
                    rows = await corsur.executemany(up_sql, data_new_list)
                    await conn.commit()
                    print(str(rows) + "success")
                except Exception as e:
                    print(e)

            # async with conn.cursor() as cursor:
            #     up_sql = "update sea_data set v_pic = %s where v_id = %s"
            #     try:
            #         print(data_new_list)
            #         rows = await corsur.executemany(up_sql, data_new_list)
            #         await conn.commit()
            #         print(rows + "=====")
            #     except Exception as e:
            #         print(e)

            # [queue.put_nowait({"v_id": item[0], "v_pic": item[1]}) for item in data_list]
            # data_dicts = [{"v_id": item[0], "v_pic": item[1]} for item in data_list]
            # for item in data_dicts:
            #     await upload_img(item)
            # [print(item) for item in data_dicts]
            # await upload_img(queue)

        # async with pool.acquire() as conn:
        #     async with conn.cursor() as cursor:
        #         await upload_img()


# async def main():
#     data_queue = asyncio.Queue()
#     # tasks = [get_data(i * 2, 2, data_queue) for i in range(2)]
#     task = asyncio.ensure_future(get_data())

#     loop = asyncio.get_event_loop()

#     loop.run_until_complete(task)

# await asyncio.(*tasks)

# print(data_queue)


if __name__ == "__main__":
    data_queue = asyncio.Queue()

    # task = asyncio.ensure_future(get_data(0, 7, data_queue))
    tasks = [asyncio.ensure_future(get_data(i * 5, 5, data_queue)) for i in range(13)]

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.gather(*tasks))
    # asyncio.run(main())
