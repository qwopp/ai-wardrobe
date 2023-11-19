import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";

const containerStyle = {
  display: "flex",
  flexWrap: "wrap",
  justifyContent: "space-between",
  gap: "20px",
};

const itemStyle = {
  flex: "0 0 calc(25% - 20px)",
  marginBottom: "20px",
};

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
    <div style={containerStyle}>
      {clothesData.map((clothing) => (
        <div
          key={clothing.clothesid}
          style={itemStyle}
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
            style={{ cursor: "pointer", width: 200, height: 300 }}
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
      <InfiniteScroll
        dataLength={clothesData.length}
        next={loadMoreClothes}
        hasMore={nextLink !== null}
        loader={<h4>Add more clothes to your wardrobe!</h4>}
      />
    </div>
  );
}
