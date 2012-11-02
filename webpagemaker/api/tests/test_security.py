import test_utils
from nose.tools import ok_
from nose.plugins.skip import SkipTest

class SecurityTests(test_utils.TestCase):
    """
    These tests are based on the following risk considerations:
    
    https://wiki.mozilla.org/Webpagemakerapi#Risk_considerations
    """
    
    def test_documents_require_doctype_definition(self):
        # To mitigate the risk "Copyrighted work can be stored and
        # distributed through the API", we require that documents
        # require DOCTYPE definitions.
        
        # This objective is satisfied by the following tests, which we're
        # merely verifying the existence of here.
        from . import test_sanitize
        ok_(getattr(test_sanitize, 'test_no_doctype'))

    def test_documents_require_correct_html(self):
        # To mitigate the risk "Copyrighted work can be stored and
        # distributed through the API", we require that documents
        # require syntactically correct HTML.

        # This objective is satisfied by the following tests, which we're
        # merely verifying the existence of here. Obviously these aren't
        # exhaustive, but they're really just integration tests to make
        # sure that we're properly configuring and talking to bleach.
        from . import test_sanitize
        ok_(getattr(test_sanitize, 'test_no_doctype'))

    def test_nofollow_links_inserted_in_anchors(self):
        # To mitigate the risk "Documents hosted via the API could be used
        # as link farms", we require that published pages be delivered
        # with an "X-Robots-Tag: noindex, nofollow" header.

        # This objective is satisfied by the following tests, which we're
        # merely verifying the existence of here. Obviously these aren't
        # exhaustive, but they're really just integration tests to make
        # sure that we're properly configuring and talking to bleach.
        from . import test_api
        ok_(test_api.PublishTests.test_retrieving_page_delivers_x_robots_tag)
    
    def test_javascript_is_stripped(self):
        # To mitigate the risk "Javascript could be used in a multitude of
        # ways to compromise client machines", we require that all JS
        # be stripped before it is served.
        
        # This objective is satisfied by the following tests, which we're
        # merely verifying the existence of here. Obviously these aren't
        # exhaustive, but they're really just integration tests to make
        # sure that we're properly configuring and talking to bleach.
        from . import test_sanitize
        ok_(test_sanitize.test_onclick_attr)
        ok_(test_sanitize.test_javascript_href)
        ok_(test_sanitize.test_script_tag)

    def test_publishing_is_rate_limited(self):
        # To mitigate the risk "Database insertion could be used as a DOS
        # attack vector", we require that the publish endpoint be
        # rate-limited.
        
        # This objective is satisfied by the following tests, which we're
        # merely verifying the existence of here.
        from . import test_api
        ok_(test_api.PublishTests.test_publishing_is_rate_limited)
    
    def test_publishing_is_size_limited(self):
        # To mitigate the risks "Copyrighted work can be stored and
        # distributed through the API" and "Database insertion could be used
        # as a DOS attack vector", we require that the publish endpoint limit
        # documents to 10,000 characters.

        # This objective is satisfied by the following test, which we're
        # merely verifying the existence of here.
        from .test_api import PublishTests
        ok_(PublishTests.test_massive_content_is_rejected)
