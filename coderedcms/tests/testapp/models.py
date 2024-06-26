from modelcluster.fields import ParentalKey

from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedStreamFormPage
from coderedcms.models import CoderedWebPage
from coderedcms.models.page_models import CoderedPage


class ArticlePage(CoderedArticlePage):
    class Meta:
        verbose_name = "Article"
        ordering = [
            "-first_published_at",
        ]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["testapp.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    class Meta:
        verbose_name = "Article Landing Page"

    index_order_by_default = ""

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "testapp.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["testapp.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


class FormPage(CoderedFormPage):
    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    page = ParentalKey("FormPage", related_name="confirmation_emails")


class WebPage(CoderedWebPage):
    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["testapp.EventIndexPage"]
    subpage_types = []
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "testapp.EventPage"
    index_order_by_default = ""

    # Only allow EventPages beneath this page.
    subpage_types = ["testapp.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class LocationPage(CoderedLocationPage):
    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["testapp.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "testapp.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["testapp.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class StreamFormPage(CoderedStreamFormPage):
    class Meta:
        verbose_name = "Stream Form"

    template = "coderedcms/pages/stream_form_page.html"


class StreamFormConfirmEmail(CoderedEmail):
    page = ParentalKey("StreamFormPage", related_name="confirmation_emails")


"""
--------------------------------------------------------------------------------
CUSTOM PAGE TYPES for testing specific features. These should be based on
CoderedPage when testing CoderedPage-specific functionality (which is where most
of our logic lives).
--------------------------------------------------------------------------------
"""


class IndexTestPage(CoderedPage):
    """
    Tests indexing features (show/sort/filter child pages).
    """

    class Meta:
        verbose_name = "Index Test Page"

    index_query_pagemodel = "testapp.WebPage"

    template = "coderedcms/pages/base.html"
