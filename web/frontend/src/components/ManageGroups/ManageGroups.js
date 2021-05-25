import "./managegroups.css";
import { Card, Button, ListGroup, Form, Alert } from "react-bootstrap";
import {useState} from 'react'

const ManageGroups = () => {

  const [groupData, setGroupData] = useState(
    {'name': '', 'desc': ''}
  )

  function handleSubmit(event) {
    event.preventDefault()
    console.log(groupData);
  }

  function handleChangeName(event) {
    event.preventDefault()
    setGroupData({...groupData, name: event.target.value})
  }

  function handleChangeDesc(event) {
    event.preventDefault()
    setGroupData({...groupData, desc: event.target.value})
  }


  return (
    <>
      <div className="mgnGroup-plane">
        <Card body className="mgnGroup-Name">
          Register Group
        </Card>
        <section className="regisGroup">
          <Form onSubmit={handleSubmit}>
            <Form.Group>
              <Form.Label><b>Name</b></Form.Label>
              <Form.Control type="name" placeholder='"BRANCH 754, SOI SUKUMVIT 50"' onChange={handleChangeName} value={groupData.name}/>
              <Form.Label><b>Description</b></Form.Label>
              <Form.Control type="desc" value={groupData.desc} onChange={handleChangeDesc} placeholder='"This branch including with 3 routers and 2 switches, both are cisco 2901"' />
            </Form.Group>
            <Button variant="primary" type="submit" >
              Create Group
            </Button>
          </Form>
        </section>

        <Card className="listofGroup">
          <Card.Header>
            <b>List of Group(s) in system</b>
          </Card.Header>
          <ListGroup variant="flush">
            <ListGroup.Item>Cras justo odio</ListGroup.Item>
            <ListGroup.Item>Dapibus ac facilisis in</ListGroup.Item>
            <ListGroup.Item>Vestibulum at eros</ListGroup.Item>
          </ListGroup>
        </Card>
      </div>
    </>
  );
};

export default ManageGroups;
