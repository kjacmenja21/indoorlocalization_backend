from sqlalchemy.orm import Session


class AssetPositionService:
    def __init__(self, session: Session) -> None:
        self.session = session
