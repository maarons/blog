Title: Web browsers and cache revalidation
Date: 2012-08-17 14:15
Tags: software web caching

Browser caching is essential if you want your web page to load quickly.  [Google
Developers][GD] has a good article showing a basic caching set-up.  If that
article satisfied your needs you do not have to read further.  I was not
satisfied though, not by this article and not by many others that tell you the
same thing — add some headers for CSS, JS and images and congratulations, you
have successfully leveraged browser caching!  Well, that is not exactly true.
Google Developers article is much more in-depth than this, but it still does not
tackle an important issue: how do I use caching and make sure my web page/web
application looks consistently for different users at the same time?  By
consistently I mean, what if I update my web page, change some ids and classes
in HTML and publish a new CSS style sheet?  Some users may have cached the old
CSS and their browsers will try to use it with the new HTML, probably with
disastrous results.  You may think that if you updated your CSS your web server
will send an updated “`Last-Modified`” or “`ETag`” header so browsers will
detect the change and pull the updated file.  Depending on other set headers
this might be true, but generally (source: [Google Developers][GD]):

> `Expires` and `Cache-Control: max-age`. These specify the “freshness lifetime”
> of a resource, that is, the time period during which the browser can use the
> cached resource without checking to see if a new version is available from the
> web server. They are “strong caching headers” that apply unconditionally; that
> is, once they’re set and the resource is downloaded, the browser will not
> issue any GET requests for the resource until the expiry date or maximum age
> is reached.

So how can you use caching and make sure everyone is using the latest version of
your files at the same time?  There are a couple of possibilities:

- Change the URL if the file changed, for example by including hash of the data
  in the file name.  This way browsers will be forced to reload the resource for
  each new version.  This works well for URLs that are not meant to be seen by
  the user directly such as CSS or JS files, but is not suitable for HTML files
  that may be bookmarked, etc.  Side note: some web frameworks do this for you
  by default — Ruby on Rails would be one of them.

- Use “`Cache-Control: no-cache`” header.  Despite the name it does not stop
  browser caching but instead it forces browsers to revalidate the cache on each
  request.  See [rfc2616][rfc2616.14.9.1] for the explanation of this header.
  Be aware that while the specification does not prevent browsers from caching
  resources with this header some browsers still choose to do so.  At the time
  of writing IE will not cache resources with this header at all
  ([source][SO:IE]).

- Set the “`Cache-Control: must-revalidate`” header and the “`Expires`” header
  (alternatively “`Cache-Control: max-age`” header) in the past or to an invalid
  value which will have the same result (see [rfc2616][rfc2616.14.21]) — “`0`”
  and “`-1`” seem to be popular choices.  This will mark the resource as already
  expired and will force revalidation.  You can also drop the “`Cache-Control:
  must-revalidate`” to tell browsers that they should revalidate, instead of
  having to do so.  Quick empirical test reveals that Google Chrome works as
  described above only when “`Cache-Control: max-age`” is set — “`Expires`”
  header alone does not enforce revalidation and when used with “`Cache-Control:
  must-revalidate`” it only revalidates HTML pages and gets CSS from the cache.
  Look [here][SO:cache] for more information about the differences between this
  method and the previous one.

- Use both “`Expires`” in the past and “`Cache-Control: no-cache`” for good
  measure.  This is what Nginx does when you use “`expires epoch`” in
  “`nginx.conf`”.  Be advised that even with both of these present some browsers
  will not revalidate certain resources.  For example Google Chrome will not
  revalidate fonts downloaded with the “`@font-face`” CSS directive.

I personally use “`Cache-Control: public, must-revalidate, max-age=0`” because
it seems to work as intended in most browsers.  This configuration will make
sure HTML, CSS and JS are kept in sync but it is suboptimal for resources that
will not change or ones that will not break the web page even if they change —
fonts downloaded with “`@font-face`” are a good example.  For such files you
should set a positive “`Cache-Control: max-age`” header so browsers do not waste
time on revalidating and can render pages faster.

[GD]: https://developers.google.com/speed/docs/best-practices/caching
[rfc2616.14.9.1]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9.1
[rfc2616.14.21]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.21
[SO:IE]: http://stackoverflow.com/q/5017454/506367
[SO:cache]: http://stackoverflow.com/a/1383359/506367
