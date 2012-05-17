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
        
        # TODO: Do we want to reject documents w/o DOCTYPE
        # definitions outright, or modify them to contain proper
        # DOCTYPE definitions if possible?
        
        raise SkipTest()

    def test_documents_require_correct_html(self):
        # To mitigate the risk "Copyrighted work can be stored and
        # distributed through the API", we require that documents
        # require syntactically correct HTML.

        # TODO: Do we want to reject invalid HTML outright, or 
        # fix them up to have syntactically correct HTML? It looks
        # like bleach tends to do the latter.

        raise SkipTest()

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
        
        # TODO: How do we want to do the rate limiting? Twitter's
        # REST API rate limiting for unauthenticated calls [1] are:
        #
        #   Unauthenticated calls are permitted 150 requests per hour.
        #   Unauthenticated calls are measured against the public facing
        #   IP of the server or device making the request.
        #
        # Twitter also returns HTTP 400 response codes if the rate limit
        # is reached. We might want to also provide ways for the front-end
        # to check the rate limit status [2].
        #
        # Note that the rate-limiting can also be done by infrastructure
        # "in front" of this app, e.g. a Zeus load balancer.
        #
        # [1] https://dev.twitter.com/docs/rate-limiting#rest
        # [2] https://dev.twitter.com/docs/rate-limiting/faq#checking

        raise SkipTest()
    
    def test_publishing_is_size_limited(self):
        # To mitigate the risks "Copyrighted work can be stored and
        # distributed through the API" and "Database insertion could be used
        # as a DOS attack vector", we require that the publish endpoint limit
        # documents to 10,000 characters.

        # This objective is satisfied by the following test, which we're
        # merely verifying the existence of here.
        from .test_api import PublishTests
        ok_(PublishTests.test_massive_content_is_rejected)
