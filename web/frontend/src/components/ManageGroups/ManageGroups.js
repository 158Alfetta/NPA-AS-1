import "./managegroups.css";
import { Card, Button, ListGroup, Form } from "react-bootstrap";

const ManageGroups = () => {
  return (
    <>
      <div className="mgnGroup-plane">
        <Card body className="mgnGroup-Name">
          Register Group
        </Card>
        <section className="regisGroup">
          <Form>
            <Form.Group>
              <Form.Label><b>Name</b></Form.Label>
              <Form.Control type="text" placeholder='"BRANCH 754, SOI SUKUMVIT 50"' />
              <Form.Label><b>Description</b></Form.Label>
              <Form.Control type="text" placeholder='"This branch including with 3 routers and 2 switches, both are cisco 2901"' />
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
