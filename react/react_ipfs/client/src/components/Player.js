import React, { useState,SetState } from 'react';
import Card from "./ShowCard"

 
const Player = ({songs}) => {
  
    const theSongs = songs.map((song, idx) => {
    return (<div style={{margin:"5%", paddingTop:"1em", border: "0.05px dashed"}} key={idx}>
        <audio src={song.URI} controls type="audio"></audio>
        <div>{song.title}</div>
    </div>)
    }
);
  return (
    <div >
        {theSongs}
    </div>
  )
}
 
export default Player