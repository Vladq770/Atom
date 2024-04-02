import datetime
import os
import subprocess
import psutil
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from database import get_async_session
from sqlalchemy.exc import SQLAlchemyError

mes_proc_err = {'mes': 'some error with process'}
mes_db_err = {'mes': 'some error with db'}
mes_success_run = {'mes': 'some error with process'}
mes_no_process = {'mes': 'No such process'}


# реализована пагинация для get-метода
def pagination(limit: int = 100, offset: int = 0):
    return {'limit': limit, 'offset': offset}


async def begin_robot(start: int = 0, session: AsyncSession = Depends(get_async_session)):
    base = os.getcwd()
    os.chdir('..')
    os.chdir('robot')
    cur = os.getcwd()
    path = os.path.join(cur, 'robot.py')
    os.chdir(base)
    try:
        process = subprocess.Popen(['python', path, f'{start}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, start_new_session=True)
    except subprocess.SubprocessError:
        return JSONResponse(content=mes_proc_err, status_code=400)
    try:
        await session.execute(
            text(f"insert into process(pid, start_number) values({process.pid}, {start})"))
        await session.commit()
    except SQLAlchemyError:
        process.terminate()
        await session.rollback()
        return JSONResponse(content=mes_db_err, status_code=400)
    return {'mes': 'process running', 'pid': process.pid}


async def terminate_robot(pid: int, session: AsyncSession = Depends(get_async_session)):
    try:
        process = psutil.Process(pid)
        if process.name() != 'python.exe':
            raise psutil.NoSuchProcess(pid)
    except psutil.NoSuchProcess:
        return JSONResponse(content=mes_no_process, status_code=400)
    process.kill()
    date = datetime.datetime.now()
    try:
        await session.execute(text(f"update process set finish_date='{date}', "
                                   f"status='terminated' where status='running' and pid={pid}"))
        await session.commit()
    except SQLAlchemyError:
        return JSONResponse(content=mes_db_err, status_code=400)
    return {'mes': f'process with pid = {pid} was terminated'}


async def terminate_all(session: AsyncSession = Depends(get_async_session)):
    pids = await session.execute(text(f"select pid from process where status='running'"))
    for pid in pids.all():
        try:
            process = psutil.Process(pid[0])
            if process.name() != 'python.exe':
                raise psutil.NoSuchProcess(pid)
        except psutil.NoSuchProcess:
            continue
        process.kill()
    date = datetime.datetime.now()
    try:
        await session.execute(text(f"update process set finish_date='{date}', "
                                   f"status='terminated' where status='running'"))
        await session.commit()
    except SQLAlchemyError:
        return JSONResponse(content=mes_db_err, status_code=400)
    return {'mes': 'all processes were terminated'}


async def get_processes(order: str = 'begin_date~desc', pagination_params: dict = Depends(pagination),
                        session: AsyncSession = Depends(get_async_session)):
    order = ','.join((order.replace('~', ' ')).split('-'))
    try:
        processes = await session.execute(text(f"select * from process order by {order} limit"
                                               f" {pagination_params['limit']} offset {pagination_params['offset']}"))
        return processes.mappings().all()
    except SQLAlchemyError:
        return JSONResponse(content=mes_db_err, status_code=400)

