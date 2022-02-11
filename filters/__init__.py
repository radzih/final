from filters.adminfilter import IsAdmin
from filters.ashareitem import ShareItem
from filters.queryisnone import QueryIsNone
from filters.querynotnone import TextIsNotNone
from filters.groupfilter import IsGroup
from filters.notregistered import NotRegistered
from handlers.users.menu import IsRegistered
from loader import dp

# from .is_admin import AdminFilter




if __name__ == "filters":
    # dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(NotRegistered)
    dp.filters_factory.bind(IsRegistered)
    dp.filters_factory.bind(ShareItem)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(TextIsNotNone)
    dp.filters_factory.bind(QueryIsNone)
