Hacker News Alternatives
========================
June 8, 2026

<!-- description: Hacker News alternatives and power-user techniques: 
     sorting extensions, Algolia search filters, and the best apps for reading 
     HN and its alternatives on iPhone. -->

While [Hacker News](https://news.ycombinator.com/) is widely regarded as the
gold standard for long-form discussion on computer science and entrepreneurship,
several other sites are highly respected within the tech community for news,
rankings, and deep-dive technical commentary. In this post we want to share some
alternatives to Hacker News that we found are good complimentary sources. We
also mention the best ways to read these sites on iPhone. But before we do it,
let us also discuss some useful techniques for navigating and filtering Hacker
News.

---

## Hacker News search

Hacker News does not have built-in, native filters for sorting by points, date,
or comment count on its standard pages. The site is designed to prioritize a
specific, proprietary ranking algorithm rather than offering a customizable
dashboard.

However, we have a few ways to achieve this:

### 1. Browser Extensions (Recommended for Sorting)

Several browser extensions exist specifically to add sorting functionality
directly to the Hacker News header. They allow us to reorder the current page's
posts by points, time, or comment count without leaving the site.

- **[Hacker News Sorted][hn-sorted]:** A popular Chrome extension that adds
  sorting buttons (Points, Time, Comments, Default) directly to the top of any
  Hacker News page. It also offers keyboard shortcuts (`P`, `T`, `C`, `D`) to
  switch views instantly.

### 2. Algolia Search (For Advanced Filtering)

The [Hacker News Search](https://hn.algolia.com/), powered by Algolia, is the
most powerful tool for custom filtering. It allows us to search through
historical data and apply specific filters.

- **How to use it:** We can use the search bar to filter by date range, post
  type (story vs. comment), and sort by "Date" or "Popularity" (which acts as a
  points-based filter).
- **Pro Tip:** If we are trying to follow a specific long-running thread, we can
  open the story on [hn.algolia.com](https://hn.algolia.com/) and sort its
  comments by "Date" to see the most recent comments at the top. (If we build
  custom queries, the underlying Algolia API also supports filtering by a
  `story_<ID>` tag.)

### 3. Native "Best" View

For a quick view of high-performing content, we can use the built-in `/best`
page, which ranks stories by point totals.

- **[Top Links](https://news.ycombinator.com/best):** This shows the
  highest-voted recent stories. The page only supports pagination (`?p=2`,
  `?p=3`, and so on), so for custom time windows use the Algolia search above.

If we are looking for more complex filtering, such as setting "minimum points"
or "minimum comment" thresholds, we may need to look for additional third-party
tools like
[Hacker News Filter & Sort](https://www.tweeks.io/t/97e72c6de5c14906a1351abd),
which adds a custom filter panel to the top of the interface.

### 4. Two more options worth knowing about:

- **[hckrnews.com](https://hckrnews.com/):** A chronological view of the Hacker
  News front page with one-click filters for the top 10/20/50% of stories by
  points or comment count.
- **[Hacker News API](https://github.com/HackerNews/API):** The official public
  API, useful if we want to build our own filtering or sorting tools.

---

## Alternatives to Hacker News

Depending on what we are looking for, whether it's breaking news, technical
depth, or community discussion, here are the most relevant alternatives:

### Community-Driven & Discussion-Oriented

- **[Lobsters](https://lobste.rs/):** If we are looking for a community that
  closely resembles Hacker News, this is often considered the closest "peer." It
  is an invite-only (though relatively easy to join) community focused on
  computer science and technology. The discussion quality is generally very
  high, and the community is highly selective about content.
- **[Slashdot](https://slashdot.org/):** A long-running community site that
  focuses on tech news and science. While it feels different from HN, it is an
  essential "OG" site where tech news is ranked, summarized, and debated through
  an extensive comment system.
- **[DEV Community](https://dev.to/):** An inclusive, community-driven space for
  software developers to share articles, discuss career paths, and stay current.
  It is much more "friendly" and collaborative than the sometimes-critical tone
  of HN, with a strong focus on professional growth and sharing personal
  technical projects.
- **[Reddit](https://www.reddit.com/):** The closest Reddit counterparts are
  **[r/programming](https://www.reddit.com/r/programming/)** for programming
  links and discussion, and
  **[r/technology](https://www.reddit.com/r/technology/)** for general tech
  news. The tone is more casual than HN, but the sheer size of these communities
  means major stories rarely slip through unnoticed.
- **[Tildes](https://tildes.net/):** An invite-only, non-profit,
  discussion-first community that is often mentioned alongside Lobsters. It is
  smaller and covers general topics beyond tech, with a strong emphasis on
  thoughtful conversation over engagement metrics.

### Curated News & Professional Aggregators

- **[Techmeme](https://techmeme.com/):** This is the definitive "news of record"
  for the tech industry. Unlike Hacker News, which is human-submitted, Techmeme
  uses a blend of algorithms and human editors to surface the most important
  tech news from across the web. It does not have a user-comment section, but it
  is the primary place to see what is trending in the industry.
- **[HackerNoon](https://hackernoon.com/):** A platform for technologists to
  read and publish long-form stories and technical insights. It is less focused
  on "breaking news" and more on community-contributed opinion, analysis, and
  tutorials.
- **[Hashnode](https://hashnode.com/):** A community built around blogging and
  knowledge sharing. If we are interested in seeing what engineers are writing
  about their personal projects, technical stacks, or career lessons, this is a
  well-regarded community.
- **[daily.dev](https://daily.dev/):** A developer news aggregator that pulls
  posts from hundreds of sources into a single personalized feed, available as a
  browser extension and as mobile apps.

### Product & Startup-Specific

- **[Product Hunt](https://www.producthunt.com/):** If our primary interest in
  Hacker News is the "Show HN" section, Product Hunt is the industry leader for
  discovering and ranking new software, apps, and hardware. It is highly
  competitive and operates on a daily upvoting cycle.
- **[Indie Hackers](https://www.indiehackers.com/):** Ideal if our focus is
  the "entrepreneurship" side of tech. It is a community for makers and startup
  founders to discuss building, marketing, and scaling bootstrapped businesses.

### Why Hacker News remains unique

It is worth noting that part of why Hacker News is in "high regard" is its
specific moderation style and lack of typical social media features (like
gamified profiles or excessive notification bells). Many of the sites above,
especially **Lobsters**, are frequently cited as the best alternatives because
they replicate this "discussion-first, bloat-second" philosophy.

---

## Reading on iPhone

Several of these platforms lack official iOS apps, as they prioritize web-based
interfaces. However, the tech community has developed highly regarded
third-party clients that provide a much better reading experience on iPhone than
using a mobile web browser.

### Hacker News

Hacker News has no official app, but it has the most robust ecosystem of
third-party readers.

- **Top Recommendations:** Apps like **[HACK for Hacker News][hack-app]** and
  **[Hacker News - Latest in Tech][hn-latest-app]** are widely praised for their
  clean design, dark modes, threaded comment support, and "readability"
  modes that strip away clutter from linked articles.
- **Pro Tip:** If we prefer not to install a dedicated app, we can use
  **Safari's "Reader View"** (tap the 'AA' icon in the URL bar) when browsing
  the site. It makes the text much easier to read on a small screen.

### Lobsters & Slashdot

- **Lobsters:** There is no dedicated iOS app. Because it is highly text-centric
  and minimalist, it is best enjoyed through a mobile browser.
- **Slashdot:** Slashdot does not have a native iOS app. Their mobile website is
  designed to be responsive, which is the officially recommended way to view it
  on an iPhone.

### DEV Community

- **DEV Community:** There is an official **[DEV Community app][dev-app]**
  (often listed as "dev.to" or "DEV Community") available on the App Store. It
  allows us to browse posts, manage our account, and engage with the community.

### Techmeme & HackerNoon

- **Techmeme:** There is a third-party app called
  **[Techmemer][techmemer-app]** which is designed to provide a native reader
  experience for the Techmeme feed.
- **HackerNoon:** HackerNoon has an official
  **[HackerNoon app][hackernoon-app]** on the App Store for reading their tech
  news and guides on the go.

### Hashnode

- **Hashnode:** Hashnode does not have an official iOS app. While we may find
  third-party wrappers or community-built projects on GitHub, these are not
  official and often offer limited functionality. For the best experience, it is
  recommended to use the Hashnode website through Safari or another mobile
  browser.

### Product Hunt

- **Product Hunt:** Unlike the others, Product Hunt has a fully featured,
  **[official iOS app][ph-app]** available for download, which is generally the
  best way to browse and upvote new products.

### Indie Hackers

- **Indie Hackers:** Indie Hackers does not have an official iOS app. Like
  Hashnode, it is designed to be accessed via the web, and the mobile-responsive
  version of their site is the officially intended way to read and participate
  in discussions on an iPhone.

### Reddit, Tildes & daily.dev

- **Reddit:** Reddit has a fully featured official iOS app, which is the most
  practical way to follow r/programming and r/technology on an iPhone.
- **Tildes:** There is no official app; the lightweight, text-centric site works
  well in a mobile browser.
- **daily.dev:** daily.dev offers an official mobile app in addition to its
  browser extension and web feed.

### Pro Tip for Mobile Access

If we want a "native-like" experience for sites without an app (like Hashnode or
Indie Hackers), we can easily create our own "web app" on our iPhone:

1. Open the site in **Safari**.
2. Tap the **Share** button at the bottom of the screen.
3. Scroll down and select **"Add to Home Screen."** This will add an icon to our
   home screen that opens the site in its own window, effectively giving us a
   dedicated shortcut that acts much like a standalone app.

### Best General Strategy for iPhone

If we find ourselves juggling many of these sites, the most efficient "pro"
method is to use a **dedicated RSS reader app** like
**[NewsBlur](https://www.newsblur.com/)** or **[Feedly](https://feedly.com/)**.

1. **Centralize:** Add the RSS feeds for these sites (most have a standard
   `/rss` or `/feed` URL) into one reader.
2. **Clean Experience:** These apps will automatically format the articles into
   a clean, readable layout, often allowing us to save articles for offline
   reading or sync our progress across devices.

[hn-sorted]: https://chromewebstore.google.com/detail/hacker-news-sorted/djkcnbncofmjekhlhemlkinfpkamlkaj

[hack-app]: https://apps.apple.com/us/app/hack-for-hacker-news-yc-reader/id1464477788

[hn-latest-app]: https://apps.apple.com/us/app/hacker-news-latest-in-tech/id1573004386

[dev-app]: https://apps.apple.com/us/app/dev-to/id1536933197

[techmemer-app]: https://apps.apple.com/us/app/techmemer/id6748340148

[hackernoon-app]: https://apps.apple.com/us/app/hackernoon/id6447998105

[ph-app]: https://help.producthunt.com/en/articles/6494278-are-ios-and-android-available
