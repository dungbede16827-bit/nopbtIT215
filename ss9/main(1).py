from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

tasks_db = []
id_counter = 1

class TaskCreate(BaseModel):
    title: str
    description: str
    assignee: str
    priority: int

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    assignee: str = None
    priority: int = None
    status: str = None


def check_trung_title(title: str, check_id: int = None):
    for t in tasks_db:
        if t["title"].lower() == title.lower():
            if check_id is not None and t["id"] == check_id:
                continue
            return True
    return False


@app.get("/")
def home():
    return {"message": "API dang chay bình thuong. Vao /docs de xem tài lieu."}


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    global id_counter
    
    if check_trung_title(task_data.title):
        raise HTTPException(status_code=400, detail="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!")

    new_task = {
        "id": id_counter,
        "title": task_data.title,
        "description": task_data.description,
        "assignee": task_data.assignee,
        "priority": task_data.priority,
        "status": "todo",
        "created_at": str(datetime.now())
    }
    
    tasks_db.append(new_task)
    id_counter += 1
    
    return {
        "statusCode": 201,
        "message": "Tạo mới công việc nhóm thành công!",
        "data": new_task,
        "timestamp": str(datetime.now())
    }


@app.get("/tasks/search")
def search_tasks(keyword: str = None, status: str = None):
    kq_tim_kiem = []
    
    for item in tasks_db:
        dung_keyword = True
        dung_status = True
        
        if keyword is not None:
            kw = keyword.lower()
            t_title = item["title"].lower()
            t_assignee = item["assignee"].lower()
            if (kw not in t_title) and (kw not in t_assignee):
                dung_keyword = False
                
        if status is not None:
            if item["status"] != status:
                dung_status = False
                
        if dung_keyword and dung_status:
            kq_tim_kiem.append(item)
            
    return {
        "statusCode": 200,
        "message": "Tìm kiếm công việc thành công",
        "data": {
            "total": len(kq_tim_kiem),
            "tasks": kq_tim_kiem
        },
        "timestamp": str(datetime.now())
    }


@app.get("/tasks/{task_id}")
def get_one_task(task_id: int):
    task_found = None
    for item in tasks_db:
        if item["id"] == task_id:
            task_found = item
            break
            
    if task_found is None:
        raise HTTPException(status_code=404, detail="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!")
        
    return {
        "statusCode": 200,
        "message": "Lấy thông tin công việc thành công",
        "data": task_found,
        "timestamp": str(datetime.now())
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update_data: TaskUpdate):
    vitri = -1
    for i in range(len(tasks_db)):
        if tasks_db[i]["id"] == task_id:
            vitri = i
            break
            
    if vitri == -1:
        raise HTTPException(status_code=404, detail="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!")
        
    current_task = tasks_db[vitri]
    
    if update_data.title is not None:
        if check_trung_title(update_data.title, task_id):
            raise HTTPException(status_code=400, detail="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!")
        current_task["title"] = update_data.title
        
    if update_data.description is not None:
        current_task["description"] = update_data.description
        
    if update_data.assignee is not None:
        current_task["assignee"] = update_data.assignee
        
    if update_data.priority is not None:
        current_task["priority"] = update_data.priority
        
    if update_data.status is not None:
        if update_data.status not in ["todo", "in_progress", "done"]:
            raise HTTPException(status_code=400, detail="Lỗi: Trạng thái công việc cập nhật không đúng quy định!")
        current_task["status"] = update_data.status

    tasks_db[vitri] = current_task
    
    return {
        "statusCode": 200,
        "message": "Cập nhật công việc thành công",
        "data": current_task,
        "timestamp": str(datetime.now())
    }


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    vitri = -1
    for i in range(len(tasks_db)):
        if tasks_db[i]["id"] == task_id:
            vitri = i
            break
            
    if vitri == -1:
        raise HTTPException(status_code=404, detail="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!")
        
    tasks_db.pop(vitri)
    return None