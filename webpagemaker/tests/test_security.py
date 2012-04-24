import test_utils

class SecurityTests(test_utils.TestCase):
    """
    These tests are based on the following risk considerations:
    
    https://wiki.mozilla.org/Webpagemakerapi#Risk_considerations
    """
    
    def test_documents_require_doctype_definition(self):
        """
        To mitigate the risk "Copyrighted work can be stored and
        distributed through the API", we require that documents
        require DOCTYPE definitions.
        """
        
        raise NotImplementedError()

    def test_documents_require_correct_html(self):
        """
        To mitigate the risk "Copyrighted work can be stored and
        distributed through the API", we require that documents
        require syntactically correct HTML.
        """
        
        raise NotImplementedError()

    def test_nofollow_links_inserted_in_anchors(self):
        """
        To mitigate the risk "Documents hosted via the API could be used
        as link farms", we require that all links have nofollow attributes
        inserted in them.
        """
        
        raise NotImplementedError()
    
    def test_javascript_is_stripped(self):
        """
        To mitigate the risk "Javascript could be used in a multitude of
        ways to compromise client machines", we require that all JS
        be stripped before it is served.
        """
        
        raise NotImplementedError()

    def test_publishing_is_rate_limited(self):
        """
        To mitigate the risk "Database insertion could be used as a DOS
        attack vector", we require that the publish endpoint be
        rate-limited.
        """
        
        raise NotImplementedError()
    
    def test_publishing_is_size_limited(self):
        """
        To mitigate the risks "Copyrighted work can be stored and distributed
        through the API" and "Database insertion could be used as a DOS
        attack vector", we require that the publish endpoint limit
        documents to 10,000 characters.
        """
        
        raise NotImplementedError()
