"""Half-open page bounds for list pagination."""


def page_bounds(page, per_page):
    """Return ``(start, end)`` for a 1-based page, both half-open.

    ``items[start:end]`` must yield ``per_page`` items for every full page, and the
    remainder on the last one. ``end`` is the exclusive bound, so a full page keeps
    its final item.
    """
    if not isinstance(page, int) or isinstance(page, bool):
        raise ValueError("page must be an integer")
    if not isinstance(per_page, int) or isinstance(per_page, bool):
        raise ValueError("per_page must be an integer")
    if page < 1:
        raise ValueError("page must be 1 or greater")
    if per_page < 1:
        raise ValueError("per_page must be 1 or greater")
    start = (page - 1) * per_page
    end = page * per_page
    return start, end
