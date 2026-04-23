from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db_connection

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()

    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if title:
            conn.execute(
                "INSERT INTO tasks (title, status) VALUES (?, ?)",
                (title, "Pending")
            )
            conn.commit()

        conn.close()
        return redirect(url_for("main.home"))

    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY created_at DESC"
    ).fetchall()

    total_tasks = len(tasks)
    pending_tasks = len([task for task in tasks if task["status"] == "Pending"])
    in_progress_tasks = len([task for task in tasks if task["status"] == "In Progress"])
    done_tasks = len([task for task in tasks if task["status"] == "Done"])

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        done_tasks=done_tasks
    )


@main_bp.route("/update_status/<int:task_id>/<status>", methods=["POST"])
def update_status(task_id, status):
    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("main.home"))


@main_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("main.home"))

@main_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    conn = get_db_connection()

    if request.method == "POST":
        new_title = request.form.get("title", "").strip()
        if new_title:
            conn.execute(
                "UPDATE tasks SET title = ? WHERE id = ?",
                (new_title, task_id)
            )
            conn.commit()
        conn.close()
        return redirect(url_for("main.home"))

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    conn.close()

    return render_template("edit_task.html", task=task)
