from typing import Set, Dict


class Gems:
    def __init__(self, queryset):
        self.queryset = queryset
        # self.unique: list = self._gem_set()
        self.count = self.total()

    def _gem_iter(self):
        return map(lambda item: item.gems, self.queryset.iterator())

    def _gem_set(self) -> Set[str]:
        gem_set: Set[str] = set()
        for item_set in self._gem_iter():
            gem_set = gem_set.union(gem_set, item_set)
        return gem_set

    def total(self) -> Dict:
        result: Dict[str, int] = {}
        for gem_list in self._gem_iter():
            for item in gem_list:
                if item in result.keys():
                    result[item] += 1
                else:
                    result[item] = 1
        return result

    def _more_two(self, queryitem):
        return [item for item in queryitem.gems if self.count[item] > 1]

    def _item(self, queryitem):
        return {
            "username": queryitem.username,
            "spent_money": queryitem.spent_money,
            "gems": self._more_two(queryitem),
        }

    def result(self):
        return {"response": [self._item(queryitem) for queryitem in self.queryset]}
