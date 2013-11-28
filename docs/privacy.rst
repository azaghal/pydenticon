Privacy
=======

It is fundamentally important to understand the privacy issues if using
Pydenticon in order to generate uniquelly identifiable avatars for users leaving
the comments etc.

The most common way to expose the identicons is by having a web application
generate them on the fly from data that is being passed to it through HTTP GET
requests. Those GET requests would commonly include either the raw data, or data
as hex string that is then used to generate an identicon. The URLs for GET
requests would most commonly be made as part of image tags in an HTML page.

The data passed needs to be unique in order to generate distinct identicons. In
most cases the data used will be either name or e-mail address that the visitor
posting the comment fills-in in some field. That being said, e-mails usually
provide a much better identifier than name (especially if the website verifies
the comments through by sending-out e-mails).

Needless to say, in such cases, especially if the website where the comments are
being posted is public, using raw data can completely reveal the identity of the
user. If e-mails are used for generating the identicons, the situation is even
worse, since now those e-mails can be easily harvested for spam purposes. Using
the e-mails also provides data mining companies with much more reliable user
identifier that can be coupled with information from other websites.

Therefore, it is highly recommended to pass the data to web application that
generates the identicons using **hex digest only**. I.e. **never** pass the raw
data.

Although passing hash instead of real data as part of the GET request is a good
step forward, it can still cause problems since the hashses can be collected,
and then used in conjunction with rainbow tables to identify the original
data. This is particularly problematic when using hex digests of e-mail
addresses as data for generating the identicon.

There's two feasible approaches to resolve this:

* Always apply *salt* to user-identifiable data before calculating a hex
  digest. This can hugely reduce the efficiency of brute force attacks based on
  rainbow tables (althgouh it will not mitigate it completely).
* Instead of hashing the user-identifiable data itself, every time you need to
  do so, create some random data instead, hash that random data, and store it
  for future use (cache it), linking it to the original data that it was
  generated for. This way the hex digest being put as part of an image link into
  HTML pages is not derived in any way from the original data, and can therefore
  not be used to reveal what the original data was.

Keep in mind that using identicons will inevitably still allow people to track
someone's posts across your website. Identicons will effectively automatically
create pseudonyms for people posting on your website. If that may pose a
problem, it might be better not to use identicons at all.

Finally, small summary of the points explained above:

* Always use hex digests in order to retrieve an identicon from a server.
* Instead of using privately identifiable data for generating the hex digest,
  use randmoly generated data, and associate it with privately identifiable
  data. This way hex digest cannot be traced back to the original data through
  brute force or rainbow tables.
* If unwilling to generate and store random data, at least make sure to use
  salt when hashing privately identifiable data.

