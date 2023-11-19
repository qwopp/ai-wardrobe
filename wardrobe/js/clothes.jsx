import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";

export default function Clothes() {
  const [clothesData, setClothesData] = useState([]);
  const [nextLink, setNextLink] = useState(null);
  const [selectedClothing, setSelectedClothing] = useState(null);

  const loadMoreClothes = () => {
    if (nextLink) {
      fetch(nextLink)
        .then((response) => response.json())
        .then((data) => {
          if (data.results && data.results.length > 0) {
            setClothesData([...clothesData, ...data.results]);
            setNextLink(data.next);
          }
        })
        .catch((error) => console.error(error));
    }
  };

  const handleClothingClick = (clothing) => {
    setSelectedClothing(clothing === selectedClothing ? null : clothing);
  };

  useEffect(() => {
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
        loader={<h4>Add more clothes to your wardrobe!</h4>}
      >
        {clothesData.map((clothing) => (
          <div
            key={clothing.clothesid}
            onClick={() => handleClothingClick(clothing)}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                handleClothingClick(clothing);
              }
            }}
            role="button"
            tabIndex={0}
          >
            <img
              src={clothing.filename}
              alt="filename"
              height={300}
              width={300}
              style={{ cursor: "pointer" }}
            />
            {selectedClothing === clothing && (
              <div>
                <p>{`Article: ${clothing.article}`}</p>
                <p>{`Clothes ID: ${clothing.clothesid}`}</p>
                <p>{`Confidence: ${clothing.confidence}`}</p>
                <p>{`Owner: ${clothing.owner}`}</p>
                <p>{`URL: ${clothing.url}`}</p>
              </div>
            )}
          </div>
        ))}
      </InfiniteScroll>
    </div>
  );
}
