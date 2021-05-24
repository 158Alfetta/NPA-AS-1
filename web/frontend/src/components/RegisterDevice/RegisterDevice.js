import "./registerdevice.css";
import { Card, Button, ListGroup, Form } from "react-bootstrap";

const RegisterDevice = () => {
  return (
    <>
      <div className="regisDevice-plane">
        <Card body className="regisDevice-Name">
          Register Device
        </Card>
        <section className="regisDevice-form">
          <Form>
            <Form.Group>
              <Form.Label>
                <b>IP Address</b>
              </Form.Label>
              <Form.Control
                type="ip_address"
                placeholder="Management IP Address of device"
                
              />
              <Form.Label>
                <b>Device Type</b>
              </Form.Label>
              <Form.Control as="select" >
                <option>Switch</option>
                <option>Router</option>
              </Form.Control>
              <Form.Label>
                <b>Group</b>
              </Form.Label>
              <Form.Control as="select" >
                <option>Default</option>
                <option>BRANCH 4</option>
              </Form.Control>
              <Form.Label>
                <b>SSH Username</b>
              </Form.Label>
              <Form.Control
                type="username"
                placeholder="Username use to connect via SSH"
                
              />
              <Form.Label>
                <b>SSH Password</b>
              </Form.Label>
              <Form.Control
                type="password"
                placeholder="Password use to connect via SSH"
                
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Register Device
            </Button>
          </Form>
        </section>
      </div>
    </>
  );
};

export default RegisterDevice;
