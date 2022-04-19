import React, { useState, useEffect} from 'react';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Spinner from 'react-bootstrap/Spinner'
import { getAlbumFromHash } from "../utils/GetAlbumHash";
import SongList from './SongList';


export const ShowCard  = ({ songs, showPlayer}) => {
  const [album, setAlbum] = useState("")
  const [contentLoaded, setContentLoaded] = useState(false)
  
  useEffect(() =>
  {getAlbumFromHash().then(r => setAlbum(r)).then(() => setContentLoaded(true))},[])
  const thesongs = album.attributes
  console.log(thesongs)
  return (
    <div style={{width: '50%', height: '50%', marginLeft:"25%", padding:"5%"}}>
<Card className="text-center" >
<Card.Header as="h5" className="text-center"><b>{album.name}</b></Card.Header>
<Card.Text>{}</Card.Text>
  <Card.Body>
  <Card.Img  src={album.image} />
    <Card.Text>
    <Container>
  <Row>
    <Col>
    <>
     { !contentLoaded && <Spinner animation="grow" />
}
      </>
    {contentLoaded && <SongList songs={album.attributes} experience={true}/>}
    </Col>
  </Row>
</Container>
    </Card.Text>
  </Card.Body>
  <Card.Footer className="text-muted" as="h3">{album.artist}</Card.Footer>
</Card>
</div>
  )
}

export default ShowCard
