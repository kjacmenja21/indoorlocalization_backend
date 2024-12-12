from sqlalchemy.orm import Session


class FloormapService:
    def __init__(self, session: Session) -> None:
        self.session = session
