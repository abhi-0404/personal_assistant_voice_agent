"""End-to-end tests for the voice assistant's tool-call endpoints."""
from tests.conftest import result_of, tool_call


# ---------- Todos ----------

def test_create_todo_returns_tool_call_id_and_todo(client):
    r = client.post("/create_todo/", json=tool_call("createTodo", {"title": "Buy milk", "description": "2 litres"}, "abc"))
    assert r.status_code == 200
    res = result_of(r)
    assert res["toolCallId"] == "abc"
    assert res["result"]["title"] == "Buy milk"
    assert res["result"]["completed"] is False
    assert res["result"]["id"] > 0


def test_arguments_may_arrive_as_a_json_string(client):
    r = client.post("/create_todo/", json=tool_call("createTodo", '{"title": "Call the bank"}'))
    assert r.status_code == 200
    assert result_of(r)["result"]["title"] == "Call the bank"


def test_get_todos_lists_created_items(client):
    for title in ("First", "Second"):
        client.post("/create_todo/", json=tool_call("createTodo", {"title": title}))
    r = client.post("/get_todos/", json=tool_call("getTodos", {}))
    assert r.status_code == 200
    assert [t["title"] for t in result_of(r)["result"]] == ["First", "Second"]


def test_complete_todo_marks_it_done(client):
    todo_id = result_of(client.post("/create_todo/", json=tool_call("createTodo", {"title": "Gym"})))["result"]["id"]
    r = client.post("/complete_todo/", json=tool_call("completeTodo", {"id": todo_id}))
    assert r.status_code == 200
    assert result_of(r)["result"]["completed"] is True


def test_complete_missing_todo_is_404(client):
    r = client.post("/complete_todo/", json=tool_call("completeTodo", {"id": 999}))
    assert r.status_code == 404


def test_delete_todo_removes_it(client):
    todo_id = result_of(client.post("/create_todo/", json=tool_call("createTodo", {"title": "Temp"})))["result"]["id"]
    r = client.post("/delete_todo/", json=tool_call("deleteTodo", {"id": todo_id}))
    assert r.status_code == 200
    assert result_of(r)["result"]["status"] == "success"
    remaining = result_of(client.post("/get_todos/", json=tool_call("getTodos", {})))["result"]
    assert remaining == []


# ---------- Request validation ----------

def test_wrong_function_name_is_rejected(client):
    r = client.post("/create_todo/", json=tool_call("deleteTodo", {"title": "x"}))
    assert r.status_code == 400


def test_invalid_arguments_are_rejected(client):
    r = client.post("/create_todo/", json=tool_call("createTodo", {"title": ""}))
    assert r.status_code == 422


def test_non_positive_id_is_rejected(client):
    r = client.post("/complete_todo/", json=tool_call("completeTodo", {"id": 0}))
    assert r.status_code == 422


# ---------- Reminders ----------

def test_reminder_lifecycle(client):
    created = client.post("/add_reminder/", json=tool_call("addReminder", {"reminder_text": "Pay rent", "importance": "high"}))
    assert created.status_code == 200
    reminder = result_of(created)["result"]
    assert reminder["importance"] == "high"

    listed = result_of(client.post("/get_reminders/", json=tool_call("getReminders", {})))["result"]
    assert [x["reminder_text"] for x in listed] == ["Pay rent"]

    deleted = client.post("/delete_reminder/", json=tool_call("deleteReminder", {"id": reminder["id"]}))
    assert deleted.status_code == 200
    assert result_of(client.post("/get_reminders/", json=tool_call("getReminders", {})))["result"] == []


# ---------- Calendar ----------

def test_calendar_entry_lifecycle(client):
    event = {
        "title": "Team sync",
        "description": "Weekly",
        "event_from": "2026-11-10T10:00:00",
        "event_to": "2026-11-10T10:30:00",
    }
    created = client.post("/add_calendar_entry/", json=tool_call("addCalendarEntry", event))
    assert created.status_code == 200
    entry = result_of(created)["result"]
    assert entry["title"] == "Team sync"

    listed = result_of(client.post("/get_calendar_entries/", json=tool_call("getCalendarEntries", {})))["result"]
    assert len(listed) == 1

    deleted = client.post("/delete_calendar_entry/", json=tool_call("deleteCalendarEntry", {"id": entry["id"]}))
    assert deleted.status_code == 200


def test_openapi_docs_are_served(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    paths = r.json()["paths"]
    for route in ("/create_todo/", "/add_reminder/", "/add_calendar_entry/", "/make_call/"):
        assert route in paths
