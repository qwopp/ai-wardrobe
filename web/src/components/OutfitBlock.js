
export default function OutfitBlock( {outfitBlock} ) {
    return (
    <div className="outfitBlock">
        <b>{outfitBlock.color}</b>
        <p>{outfitBlock.type}</p>
    </div>
    )
}