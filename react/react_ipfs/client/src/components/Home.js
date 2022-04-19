import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col'

export const Home = () => {
    const styles ={
        width: '80%',
        height: '100%',
        marginLeft: '10%',
        marginRight: '10%',
        border: '1px solid'
    }
  return (
    <div >
        <Container fluid="md" >
  <Row>
    <Col className="md-3">1 of 4</Col>
    <Col className="md-3">2 of 4</Col>
    <Col className="md-3">3 of 4</Col>
    <Col>4 of 4</Col>
  </Row>
</Container>
    </div>
  )
}

export default Home