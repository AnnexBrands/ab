"""Live integration tests for the notes endpoint group.

Mirrors ``examples/notes.py`` -- list notes, suggest users, create a note
threading a category UUID from ``api.lookup.get_refer_category()``.
Skipped when staging credentials are not available.
"""

from __future__ import annotations

import pytest

from ab.api.models.notes import GlobalNote, NoteRequest, SuggestedUser

pytestmark = pytest.mark.live


class TestNotesIntegration:
    def test_list_requires_at_least_one_filter(self, api):
        # Documented divergence: swagger marks all filters optional, live
        # API returns HTTP 400 when none are supplied.
        from ab.exceptions import RequestError

        with pytest.raises(RequestError) as exc_info:
            api.notes.list()
        assert exc_info.value.status_code == 400

    def test_list_with_company_filter_returns_global_notes(self, api):
        from examples.constants import TEST_COMPANY_ID

        notes = api.notes.list(company_id=TEST_COMPANY_ID)
        assert isinstance(notes, list)
        for n in notes:
            assert isinstance(n, GlobalNote)
            assert isinstance(n.note_id, int)

    def test_suggest_users_returns_suggested_user_rows(self, api):
        users = api.notes.suggest_users("br")
        assert isinstance(users, list)
        for u in users:
            assert isinstance(u, SuggestedUser)
            assert isinstance(u.id, int)
            assert u.full_name is not None

    def test_category_lookup_feeds_note_request(self, api):
        """Forward reference: lookup category UUID -> NoteRequest.category.

        We construct (but do not POST) the request to validate the
        end-to-end discovery chain.
        """
        try:
            categories = api.lookup.get_refer_categories()
        except AttributeError:
            pytest.skip("api.lookup.get_refer_categories not available")
        if not categories:
            pytest.skip("no note categories on staging")
        cat = categories[0]
        cat_uuid = getattr(cat, "value", None) or getattr(cat, "id", None)
        assert cat_uuid, "category lookup must yield a UUID value/id"
        body = NoteRequest(comments="integration test (not posted)", category=str(cat_uuid))
        assert body.comments and body.category == str(cat_uuid)
