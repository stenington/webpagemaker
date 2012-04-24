The WebPageMakerAPI Stub
========================

The API is a two-endpoint HTTP API that accepts (via POST) HTML documents and 
serves those documents via a short url. The HTML documents are cleaned by 
Bleach before being served. Playdoh is the planned implementation framework.

API Methods:
------------

<table>
  <thead>
    <tr>
      <td>Name</td>
      <td>Endpoint</td>
      <td>HTTP Method</td>
      <td>Parameters</td>
      <td>Return</td>
   </tr> 
  </thead>
  <tbody>
    <tr>
      <td>Create Page</td>
      <td>/page</td>
      <td>POST</td>
      <td>Raw Post Data (HTML)</td>
      <td>Relative Short URL KEY id (eg. "ja5bn") which can be appended to the app index (eg. "http://webpagemakerapi.vcap.mozillalabs.com/ja5bn")</td>
    </tr>
    <tr>
      <td>Read Page</td>
      <td>/{short url id}</td>
      <td>GET</td>
      <td>short url id (in path)</td>
      <td>Sanitized (<a href="http://pypi.python.org/pypi/bleach" class="external text" rel="nofollow">Bleach</a>)</td>
    </tr>
  </tbody>
</table>
