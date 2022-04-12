import React, { useState } from "react";
import { useSelector, useDispatch } from 'react-redux';
import { updateAlbum, updateCoverHash, updateAlbumTitle, reset,addSongs , removeSong } from "../features/album/albumSlice";
import ipfs from "../ipfs";
import Player from "./Player";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import SongList from './SongList';




const CreateAlbum = ()=> {
  const [ coverHash, setCoverHash] = useState("")
  const [ coverPreview, setCoverPreview ]= useState("")
  const [ albumTitle, setAlbumTitle] = useState("")
  const [ artist, setArtist] = useState("")
  const [ genre, setGenre] = useState("")
  const [ albumURI, setAlbumURI] = useState("")
  const [ songs, setSongs] = useState([])
  const [validated, setValidated] = useState(false);

  
  const album = useSelector((state)=> state.album)
  const dispatch  = useDispatch()
  // dispatch(reset())

  // console.log(album.album.coverHash)

    const dispatchAll = (e) =>{
      const form = e.currentTarget;
      e.preventDefault()
      if (form.checkValidity() === false) {
        e.preventDefault();
        e.stopPropagation();
      }
      
      setValidated(true);
      console.log("In dispatch all")
      let payload = {}
      if(coverHash) payload.coverHash = coverHash
      if(albumTitle) payload.albumTitle = albumTitle
      if(artist) payload.artist = artist
      if(genre) payload.genre = genre
      if(songs.length > 0) payload.songs = songs

      console.log(payload)
      // if(cover && albumTitle && artist && genre && songs) 
      dispatch(updateAlbum(payload))
      // dispatch(updateAlbum({albumTitle,artist,year:"1972", genre}))
 

    }
    const processFilesToIpfs = (buffer) =>{
     ipfs.files.add(buffer,(error, result) => {
        console.log('in ipfs...')
        if(error){
          return console.log(error)
        }
        else {
          return result[0].hash

            }
          }
        )  

    }
    const handleAlbumCover = ( e )=> {
      const files = e.target.files
      setCoverPreview(URL.createObjectURL(e.target.files[0]))
      if(files[0]['name'].split(".")[1] === "jpg"){
        const reader = new window.FileReader();
        reader.readAsArrayBuffer(files[0])
        reader.onloadend = () => {
         let hash = processFilesToIpfs(Buffer(reader.result))
         setCoverHash(hash)
         dispatch(updateAlbum({coverHash: hash}))
        }
    
  }
}
   
  const handleSongs  = async (e) =>{
    const files = e.target.files
    let i = 0
    for await (let file of files){
      i++
      let song = {}, hash
      const title = file['name'].split(".")[0]
      song.id = i
      song.title = title
      song.artist = artist || album.album.artist
      song.album = albumTitle || album.album.albumTitle
      const reader = new window.FileReader();
      reader.readAsArrayBuffer(file);
      reader.onloadend = async () => {
        await ipfs.files.add(Buffer(reader.result),(error, result) => error ? console.log(error) : 
         song.hash = result[0].hash)
         setSongs(songs => [...songs, song])
       }

    }

  }
 const removeSong = (id) =>{
   let updatedSongs = songs.filter(s => s.id !== id)
   setSongs(updatedSongs)
 }
  
  return (
    <div style={{padding:"5%", width:"70%", marginLeft:"15%"}}>
      <Card style={{ padding: "5%" }} >
        {album.album.artist && album.album.albumTitle && <Card.Header as="h5" className="text-center"><b>{album.album.artist}: </b>{album.album.albumTitle} </Card.Header>}
        <Card.Body>
          <Card.Img variant="top" src={`https://ipfs.io/ipfs/${album.album.coverHash}` || coverPreview } />
          {songs && <SongList songs={songs} removeSong={removeSong}/>}
            <Form noValidate validated={validated} onSubmit={(e)=> dispatchAll(e)}>
            <br></br>
            <Form.Control type="file" className="custom-file-input" id="cover" onChange={(e)=> handleAlbumCover(e)}/>
            <br></br>
            <Form.Group className="mb-3" controlId="albumTitle" onChange={(e)=> {
              setAlbumTitle(e.target.value)
              setValidated(!validated)}}>
            <Form.Label>Title</Form.Label>
            <Form.Control type="text" placeholder={ album.album.albumTitle } onChange={(e)=> {setAlbumTitle(e.target.value)}}/>
            <Form.Text className="text-muted">
            <Form.Control.Feedback type={!validated && "invalid"}>
              {/* Please enter artist. */}
            </Form.Control.Feedback>
            </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3" controlId="artist" onChange={(e) => {
              setArtist(e.target.value) 
              setValidated(!validated)}}>
            <Form.Label>Artist</Form.Label>
            <Form.Control type="text" placeholder={album.album.artist}  />
            <Form.Text className="text-muted">
            <Form.Control.Feedback type={!validated && "invalid" }>
              {/* Please enter artist or group name. */}
            </Form.Control.Feedback>
            </Form.Text>
           </Form.Group>
            <Form.Group className="mb-3" controlId="genre" >
            <Form.Label >Genre</Form.Label>
            <Form.Select id="genre"  onChange={(e) => {
              setGenre(e.target.value)}}>
            <option value={null}> {`${album.album.genre}` || "Select a genre..."}</option>
            <option value="Hip-Hop">Hip-Hop</option>
            <option value="R&B">R&B</option>
            <option value="Rock">Rock</option>
            </Form.Select>
            <Form.Control.Feedback type={ validated ? "" : "invalid"} >
              {/* Please enter album genre. */}
            </Form.Control.Feedback>
            </Form.Group>
            <Form.Text id="" muted>
              Upload your music files here. Want to upload your <b>Album Cover?</b> Use upload button <b>Above ⬆</b>.
            </Form.Text>
            <div className="custom-file">
              <Form.Control type="file"  className="custom-file-input" id="audioFiles" multiple="multiple" onChange={(e)=> handleSongs(e)}/>
            </div>
            <br></br>
            <Button variant="secondary" type="submit" style={{marginRight:"2%"}}>
             Submit
            </Button>
            <Button variant="secondary" type="button" onClick={()=> dispatch(reset())}>
             Reset State
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </div>)
  // }


}

export default CreateAlbum