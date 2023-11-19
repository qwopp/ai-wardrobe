import { useState } from 'react';
import './OutfitInput.css';


export default function OutfitInput({outfitBlocks, setBlock, id_value}){
    const [text, setText] = useState('')
    return(
        <div onSubmit={(e) =>{
            e.preventDefault();
            const newbBlock = {
                id: 0,
                owner: "Bob",
                color: "white",
                type: "pants",
                percentage: 72.3
            }
            setBlock([...outfitBlocks, newbBlock])
            }}>
            <form>
                <input type = "text" placeholder='Example: outfit for summer' name = "block" value = {text} onChange={(e) =>
                {
                    setText(e.target.value)
                }}/>
                <button type = "submit">
                    Ask!
                </button>

            </form>
        </div>


    );

}