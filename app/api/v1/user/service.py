from sqlalchemy.orm import Session
from typing import Dict

from app.models import User, Solved, Puzzle
from .exception import AlreadySolvedPuzzleExepction


class ProfileService:
    def __init__(self, user: dict, db: Session):
        self.db = db
        self.user = user

    async def update_solved_count(self, puzzle_id: int) -> Dict:
        is_solved = (
            self.db.query(Solved)
            .filter(Solved.user_id == self.user["id"], Solved.puzzle_id == puzzle_id)
            .first()
        )
        if is_solved:
            raise AlreadySolvedPuzzleExepction()
        else:
            solved_row = Solved(user_id=self.user["id"], puzzle_id=puzzle_id)
            puzzle_row = self.db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
            user_row = self.db.query(User).filter(User.id == self.user["id"]).first()
            user_row.solved += 1
            puzzle_row.solved += 1

            self.db.add(solved_row)
            self.db.commit()

            return {"solved": user_row.solved}
