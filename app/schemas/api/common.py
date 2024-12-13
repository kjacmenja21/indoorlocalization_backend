from pydantic import BaseModel


class PaginationBase(BaseModel):
    current_page: int
    total_pages: int
    page_limit: int
