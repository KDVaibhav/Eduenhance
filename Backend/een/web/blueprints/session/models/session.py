from flask_socketio import emit

from een.db import sessions, proposals
from een.web.app.flow import ProposalFlow
from .chat import SessionChat
from .quorum import SessionQuorum
from .stages import SessionStages
from .users import SessionUsers


class Session:
    """Represents Session."""

    def __init__(self, session_id, connections):
        """Initializes new instance of the Session class.
        :param session_id: Session Id"""
        self.__session_id = session_id
        self.__stages = SessionStages(self)
        self.__users = SessionUsers(self)
        self.__chat = SessionChat(self)
        self.__quorum = SessionQuorum(self)
        self.connections = connections

        # subscribe for aspects' events
        self.__users.changed.subscribe(self.__on_user_state_changed)
        self.__stages.changed.subscribe(self.__on_stage_changed)

    @property
    def session_id(self):
        return self.__session_id

    @property
    def chat(self):
        return self.__chat

    @property
    def stages(self):
        return self.__stages

    @property
    def users(self):
        return self.__users

    @property
    def quorum(self):
        return self.__quorum

    @property
    def presence_roles(self):
        session = sessions.get(self.session_id)
        return session["permissions"]["presence"]

    @property
    def vote_roles(self):
        session = sessions.get(self.session_id)
        return session["permissions"]["vote"]

    def close(self):
        session = sessions.get(self.session_id)
        for proposal_id in session.proposals:
            proposal = proposals.get(proposal_id)
            ProposalFlow(proposal).move_next()
            proposals.save(proposal)

        session.status = "closed"
        sessions.save(session)

    def manage(self, data, user):
        if data["command"] == "set_quorum" and "codes" not in data:
            return self.__quorum.request_change(data["value"])
        if data["command"] == "set_quorum" and "codes" in data:
            result = self.__quorum.change(data["codes"])
            self.stages.changed.notify(self.stages.current)
            return result

    def notify(self, event, data, room=None):
        emit(event, data, room=room or self.__session_id)

    def __on_user_state_changed(self, socket_id, user, joined):
        stage_view = self.__stage_view(self.__stages.current)
        self.notify("stage", stage_view, room=socket_id)

    def __on_stage_changed(self, stage):
        self.notify("stage", self.__stage_view(stage))

    def __stage_view(self, stage):
        stages_count = self.__stages.count
        stage_index = self.__stages.index

        result = {
            "stage": {
                "type": stage.name
            },
            "progress": {
                "index": stage_index + 1,
                "total": stages_count
            }
        }

        if stage.proposal:
            result["proposal_id"] = str(stage.proposal.id)

        result.update(stage.view)
        return result
