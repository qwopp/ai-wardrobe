import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";

export default function Clothes() {
  const [clothesData, setClothesData] = useState([]);
  const [nextLink, setNextLink] = useState(null);

  const loadMoreClothes = () => {
    if (nextLink) {
      fetch(nextLink)
        .then((response) => response.json())
        .then((data) => {
          if (data.results && data.results.length > 0) {
            // Append the new clothes to the existing clothesData
            setClothesData([...clothesData, ...data.results]);
            setNextLink(data.next);
          }
        })
        .catch((error) => console.error(error));
    }
  };

  useEffect(() => {
    // Fetch clothes from the API endpoint
    fetch("/api/v1/clothing/")
      .then((response) => response.json())
      .then((data) => {
        if (data.results && data.results.length > 0) {
          setClothesData(data.results);
          setNextLink(data.next);
        }
      })
      .catch((error) => console.error(error));
  }, []);

  return (
    <div className="clothes">
      <InfiniteScroll
        dataLength={clothesData.length}
        next={loadMoreClothes}
        hasMore={nextLink !== null}
        loader={<h4>Loading...</h4>}
      >
        {clothesData.map((clothing) => (
          <div key={clothing.clothesid}>
            <p>{`Article: ${clothing.article}`}</p>
            <p>{`Clothes ID: ${clothing.clothesid}`}</p>
            <p>{`Confidence: ${clothing.confidence}`}</p>
            <img
              src={clothing.filename}
              alt="filename"
              height={100}
              width={100}
            />
            <p>{`Filename: ${clothing.filename}`}</p>
            <p>{`Owner: ${clothing.owner}`}</p>
            <p>{`URL: ${clothing.url}`}</p>
            {/* Add other details or formatting as needed */}
          </div>
        ))}
      </InfiniteScroll>
    </div>
  );
}
