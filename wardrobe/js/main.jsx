import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [nextLink, setNextLink] = useState(null);

  const loadMorePosts = () => {
    if (nextLink) {
      fetch(nextLink)
        .then((response) => response.json())
        .then((data) => {
          if (data.results && data.results.length > 0) {
            // Append the new posts to the existing posts
            setPosts([...posts, ...data.results]);
            setNextLink(data.next);
          }
        })
        .catch((error) => console.error(error));
    }
  };

  useEffect(() => {
    // Fetch posts from your API endpoint
    fetch("/api/v1/clothing/?size=10&page=0") // Adjust the URL parameters as needed
      .then((response) => response.json())
      .then((data) => {
        if (data.results && data.results.length > 0) {
          setPosts(data.results);
          setNextLink(data.next);
        }
      })
      .catch((error) => console.error(error));
  }, []);

  return (
    <div className="feed">
      <InfiniteScroll
        dataLength={posts.length}
        next={loadMorePosts}
        hasMore={nextLink !== null}
        loader={<h4>Loading...</h4>}
      >
        {posts.map((post) => (
          <div key={post.clothesid}>
            <p>{`Owner: ${post.owner}`}</p>
            <p>{`Article: ${post.article}`}</p>
            <p>{`Confidence: ${post.confidence}`}</p>
          </div>
        ))}
      </InfiniteScroll>
    </div>
  );
}
