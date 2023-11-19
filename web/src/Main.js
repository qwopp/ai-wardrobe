import React, {useState} from 'react';
import OutfitInput from "./components/OutfitInput";
import OutfitBlock from "./components/OutfitBlock";
import Upload from "./components/Upload"
import './default.css'
export default function Main( {outfitBlock} ) {
    var id_value = 2
    const [outfitBlocks, setBlock] = useState([
      {
        id: 0,
        owner: "Bob",
        color: "white",
        type: "pants",
        percentage: 72.3
  
      },
      {
        id: 1,
        owner: "Daniel",
        color: "black",
        type: "shirt",
        percentage: 72.3
      }    
    ])
    return (
      <>
        <div className='logoContainer'>
          <img className = 'logo' src='/VirtuWear.png'/>

        </div>
        <div className='upload'>
          <Upload/>
        </div>

        <div className="blockContainer">
          <div className='blockInput'>
            <OutfitInput outfitBlocks = {outfitBlocks} setBlock = {setBlock} id_value = {id_value}/>
          </div>
    
          <div className = "blockDisplay">
            {outfitBlocks.map((outfitBlock) =>(
              <OutfitBlock outfitBlock = {outfitBlock}/>
    
            ))}
          </div>
        </div>
      </>      
    )
}