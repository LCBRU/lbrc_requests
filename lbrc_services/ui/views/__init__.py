__all__ = [
    "task",
    "todo",
    "user",
    "reports",
]


from datetime import timedelta
from lbrc_flask.security import current_user_id
from sqlalchemy.orm import joinedload
from lbrc_services.model import Service, Task, TaskStatusType, User
from flask_security import current_user
from sqlalchemy import or_


def _get_tasks_query(search_form, owner_id=None, requester_id=None, sort_asc=False):

    q = Task.query.options(
        joinedload(Task.data),
        joinedload(Task.files),
        joinedload(Task.current_status_type),
    )
    if search_form.search.data:
        q = q.filter(Task.name.like("%{}%".format(search_form.search.data)))

    if search_form.data.get('service_id', 0) not in (0, "0", None):
        q = q.filter(Task.service_id == search_form.data['service_id'])

    if search_form.data.get('organisation_id', 0) not in (0, "0", None):
        q = q.filter(Task.organisation_id == search_form.data['organisation_id'])

    if search_form.data.get('requestor_id', 0) not in (0, "0", None):
        q = q.filter(Task.requestor_id == search_form.data['requestor_id'])

    if search_form.data.get('created_date_from', None):
        q = q.filter(Task.created_date >= search_form.data['created_date_from'])

    if search_form.data.get('created_date_to', None):
        q = q.filter(Task.created_date < search_form.data['created_date_to'] + timedelta(days=1))

    assigned_user_id = search_form.data.get('assigned_user_id', 0)

    if assigned_user_id == -2:
        q = q.filter(or_(
            Task.current_assigned_user_id == 0,
            Task.current_assigned_user_id == None,
            Task.current_assigned_user_id == current_user_id(),
        ))
    elif assigned_user_id == -1:
        pass
    elif assigned_user_id in (0, "0", None):
        q = q.filter(or_(
            Task.current_assigned_user_id == 0,
            Task.current_assigned_user_id == None,
        ))
    else:
        q = q.filter(Task.current_assigned_user_id == assigned_user_id)

    if 'task_status_type_id' in search_form.data:
        option = search_form.data.get('task_status_type_id', 0) or 0

        q = q.join(Task.current_status_type)

        if option == 0:
            q = q.filter(TaskStatusType.is_complete == False)
        elif option == -1:
            q = q.filter(TaskStatusType.is_complete == True)
        elif option != -2:
            q = q.filter(TaskStatusType.id == option)

    if owner_id is not None:
        q = q.join(Task.service)
        q = q.join(Service.owners)
        q = q.filter(User.id == owner_id)

    if requester_id is not None:
        q = q.filter(Task.requestor_id == requester_id)

    if sort_asc:
        q = q.order_by(Task.created_date.asc())
    else:
        q = q.order_by(Task.created_date.desc())

    return q
