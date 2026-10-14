import uuid

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active : dict[uuid.UUID,set[WebSocket]] = {} # khai báo bién active là 1 dict bao gồm id user và 1 set (ko trùng) các cổng kết nối tương đương nhiều thiết bị

    async def connect(self, user_id: uuid.UUID, ws: WebSocket):
        await ws.accept() # mở cổng kết nối
        self.active.setdefault(user_id,set()).add(ws) # thêm  cổng kết nối ws đó vào dict đang kết nối của user ví dụ {1:  {ws1, ws2}}
        '''giống django:
            self.get_channel_layer.group_add(room_name,channel_name)
            self.accept()   
        '''
    async def disconnect(self, user_id: uuid.UUID, ws: WebSocket):
        con = self.active.get(user_id) # lấy ra user id và các cổng ws của user_id đó
        if con:
            con.discard(ws) #loại bỏ cổng kêt nối ws đó ra khỏi dict khi có user_id, các cổng khác vãn còn trong user_id đó
            if not con:
                del self.active[user_id] #xóa luôn user id nếu không còn cổng nào(rỗng)

    async def send_to_user(self, user_id: uuid.UUID, data: dict): # truyền vào user_id và data để gửi tới
        for ws in list(self.active.get(user_id,[])): # lấy ra tất cả cổng ws của user_id để gửi tới từng cổng
            try:
                await ws.send_json(data)
            except Exception:
                await self.disconnect(user_id,ws)

manager = ConnectionManager()