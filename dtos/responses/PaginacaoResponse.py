from typing import Generic, TypeVar, List

T = TypeVar('T')

class PaginacaoResponse(Generic[T]):
    def __init__(self, hasNextPage: bool, page: int, totalPage: int, qtdItens: int, items: List[T]):
        self.hasNextPage = hasNextPage
        self.page = page
        self.totalPage = totalPage
        self.qtdItens = qtdItens
        self.items = items

    def to_dict(self):
        return {
            "items": self.items,
            "hasNextPage": self.hasNextPage,
            "page": self.page,
            "totalPage": self.totalPage,
            "qtdItens": self.qtdItens
        }