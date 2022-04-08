import React, { Component} from "react";
import Player from "./Player";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';




class  CreateAlbum extends Component {

  constructor(props) {
    super(props)
    
    this.state = {
      cover:"",
      title: "",
      artist:"" ,
      album : "",
      media: "",
      songs: [],
      previewSongs:[],
      albumURI: "",
      metaData: {}
    }
  }
    // Add album cover
    addAlbumCover = (e) =>{
      if(e.target.files.length !== 0){
        this.setState({cover: URL.createObjectURL(e.target.files[0])})
      }
    }

    // Add songs in queue to be uploaded
    addSongs = (e) => {
      e.preventDefault();
      const theFiles = e.target.files
      console.log(theFiles)
      // for(let i = 0; i < theFiles.length; i++){
      //   return (<audio src={URL.createObjectURL(theFiles[i])} controls type="audio"></audio>)

      // }
      
    }
    render() {
  return (
    <div style={{padding:"5%", width:"70%", marginLeft:"15%"}}>
<Card style={{ padding: "5%" }}>
<Card.Body>
   {this.state.cover && <Card.Img variant="top" src={this.state.cover} />}
   {(e)=> this.addSongs(e)}
<Form onSubmit={(e)=> this.createdFiles(e)}>
<div className="custom-file">
<br></br>
  <Form.Control type="file" className="custom-file-input" id="albumCoverFile" onChange={(e)=> this.addAlbumCover(e)}/>
  </div>
  <br></br>
  <Form.Group className="mb-3" controlId="albumTitle">
    <Form.Label>Title</Form.Label>
    <Form.Control type="text" placeholder="Album Title" />
    <Form.Text className="text-muted">
    </Form.Text>
  </Form.Group>

  <Form.Group className="mb-3" controlId="artist">
    <Form.Label>Artist</Form.Label>
    <Form.Control type="text" placeholder="Artist" />
    <Form.Text className="text-muted">
    </Form.Text>
  </Form.Group>
  <Form.Group className="mb-3" controlId="genre">
  <Form.Label >Genre</Form.Label>
  <Form.Select id="genre">
  <option value=""> Select a genre...</option>
  <option value="Hip-Hop">Hip-Hop</option>
  <option value="r_and_b">R&B</option>
  <option value="rock">Rock</option>
  </Form.Select>
  </Form.Group>
  <Form.Text id="passwordHelpBlock" muted>
    Upload your music files here. Want to upload your <b>Album Cover?</b> Use upload button <b>Above ⬆</b>.
  </Form.Text>
  <div className="custom-file">
  <Form.Control type="file" className="custom-file-input" id="audioFiles" multiple="multiple" onChange={e => this.addSongs(e)}/>
  </div>
  <br></br>
  <Button variant="secondary" type="submit">
    Submit
  </Button>
</Form>
</Card.Body>
</Card>
    </div>)
  }


}

export default CreateAlbum