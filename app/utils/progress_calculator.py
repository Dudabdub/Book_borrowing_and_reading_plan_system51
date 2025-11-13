from app.models import Task
from datetime import datetime

def calculate_course_progress(course):
    tasks = Task.query.filter_by(course_id=course.id).all()
    homework_tasks = [t for t in tasks if t.task_type == 'homework']
    experiment_tasks = [t for t in tasks if t.task_type == 'experiment']
    exam_tasks = [t for t in tasks if t.task_type == 'exam']

    homework_progress = _calculate_task_type_progress(homework_tasks)
    experiment_progress = _calculate_task_type_progress(experiment_tasks)
    exam_progress = _calculate_task_type_progress(exam_tasks)

    total_progress = (
        homework_progress * course.homework_weight +
        experiment_progress * course.experiment_weight +
        exam_progress * course.exam_weight
    )

    return {
        'total': round(total_progress * 100, 2),
        'homework': round(homework_progress * 100, 2),
        'experiment': round(experiment_progress * 100, 2),
        'exam': round(exam_progress * 100, 2),
        'next_deadline': _get_next_deadline(tasks)
    }

def _calculate_task_type_progress(tasks):
    if not tasks:
        return 0
    completed_tasks = [t for t in tasks if t.status == 'completed']
    scored_tasks = [t for t in completed_tasks if t.score is not None and t.max_score is not None]
    if scored_tasks:
        total_score = sum(t.score for t in scored_tasks)
        total_max_score = sum(t.max_score for t in scored_tasks)
        if total_max_score > 0:
            return total_score / total_max_score
    return len(completed_tasks) / len(tasks)

def _get_next_deadline(tasks):
    pending_tasks = [t for t in tasks if t.status == 'pending' and t.due_date]
    if not pending_tasks:
        return None
    next_task = min(pending_tasks, key=lambda x: x.due_date)
    return next_task.due_date
