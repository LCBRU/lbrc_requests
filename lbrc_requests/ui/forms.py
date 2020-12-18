from lbrc_flask.forms import SearchForm, FlashingForm
from flask_login import current_user
from wtforms import SelectField, BooleanField, TextAreaField
from wtforms.fields.simple import HiddenField 
from wtforms.validators import DataRequired, Length
from lbrc_requests.model import RequestStatusType, RequestType, Request, User


class MyJobsSearchForm(SearchForm):
    show_completed = BooleanField('Completed')
    request_type_id = SelectField('Request Type', coerce=int, choices=[])
    requestor_id = SelectField('Requesterd By', coerce=int, choices=[])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.requestor_id.choices = self._get_requestor_choices()
        self.request_type_id.choices = self._get_request_type_choices()

    def _get_requestor_choices(self):
        request_type_ids = RequestType.query.with_entities(RequestType.id.distinct()).join(RequestType.owners).filter(User.id == current_user.id).subquery()
        requestor_ids = Request.query.with_entities(Request.requestor_id.distinct()).filter(Request.request_type_id.in_(request_type_ids)).subquery()
        submitters = sorted(User.query.filter(User.id.in_(requestor_ids)).all(), key=lambda u: u.full_name)

        return [(0, 'All')] + [(u.id, u.full_name) for u in submitters]

    def _get_request_type_choices(self):
        request_types = RequestType.query.join(RequestType.owners).filter(User.id == current_user.id).all()

        return [(0, 'All')] + [(rt.id, rt.name) for rt in request_types]


class RequestUpdateStatusForm(FlashingForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.status.choices = self._get_status_choices()

    def _get_status_choices(self):
        request_statuses = RequestStatusType.query.order_by(RequestStatusType.name.asc()).all()

        return [(rt.id, rt.name) for rt in request_statuses]

    request_id = HiddenField()
    status = SelectField("New Status", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Length(max=500)])