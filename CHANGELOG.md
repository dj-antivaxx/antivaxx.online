# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-04-03

### Added

- minimal imageboard functionality:
   - creating threads with an attached image(s) and a thread name. threads populate dynamic urls. the main page lists threads ordered by the most recent postings. threads on the main page preview 3 posts
   - adding posts to threads; each post displays attached images, timestamp, and a post id; posts text support markdown and has max/min characters constraints as well as image dimensions constraints
   - post replies and nested reply previews
   - image preview on upload
   - image pop up on click
