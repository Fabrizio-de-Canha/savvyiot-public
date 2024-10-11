import asyncio
from endpoints.authenticate import get_token_header
import models
from deps import get_session
import select

from fastapi import APIRouter, Body, Depends, HTTPException, WebSocket, status
from sqlalchemy.orm import Session, Query
from db.session import pg_url_socket
import asyncpg

router = APIRouter()

async def listen_to_tenant_updates(websocket: WebSocket, tenant_id):
    conn: asyncpg.Connection = await asyncpg.connect(pg_url_socket)
    await conn.execute(f"LISTEN tenant_{tenant_id}_updates;")

    websocket_open = True 

    async def callback(connection,
                   pid,
                   channel,
                   payload):
        nonlocal websocket_open
        if websocket_open:  # Check if the WebSocket is still open
            try:
                await websocket.send_text(payload)
            except Exception as e: 
                # Stop sending if the WebSocket is closed
                print(f"WebSocket closed: {e.code}")
                websocket_open = False

    await conn.add_listener(f'tenant_{tenant_id}_updates', callback)
    
    try:
        while websocket_open:
            await asyncio.sleep(1)  # Keep the loop alive to prevent blocking
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if not conn.is_closed():
            await conn.close()
        
@router.websocket("/ws")
async def websocket_endpoint(
            websocket: WebSocket,
            db: Session = Depends(get_session)
        ):
    
    # Extract token from query params (instead of headers)
    query_params = websocket.query_params
    token = query_params.get("token")

    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Validate token
    try:
        user: dict = await get_token_header(token)
    except HTTPException as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    task = asyncio.create_task(listen_to_tenant_updates(websocket, user['tenant']))

    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled")
    finally:
        try:
            await websocket.close()
        except Exception as e:
            print(f"Error closing WebSocket: {e}")