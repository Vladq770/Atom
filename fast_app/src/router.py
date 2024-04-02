from typing import Mapping
from fastapi import APIRouter, Depends
from service import begin_robot, terminate_robot, terminate_all, get_processes

router = APIRouter(prefix='/process', tags=['Process'])


@router.get('/get_processes')
async def get_repos(processes: Mapping = Depends(get_processes)):
    return processes


@router.post('/run')
async def run(mes: dict = Depends(begin_robot)):
    return mes


@router.post('/terminate/{pid}')
async def terminate(mes: dict = Depends(terminate_robot)):
    return mes


@router.post('/terminate_all')
async def terminate_all(mes: dict = Depends(terminate_all)):
    return mes
