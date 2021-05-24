import { useParams } from "react-router-dom";
import { Card, Col, Row, Table } from "react-bootstrap";
import "./DeviceDetail.css";

const DeviceDetail = () => {
  let { deviceId } = useParams();

  return (
    <>
      <div className="device-detail-plane">
        <Card>
          <Card.Header as="h4">Device Detail</Card.Header>
          <Card.Body>
            <Card.Title>Hostname</Card.Title>
            <Card.Text>
              <Row>
                <Col>Device Type: </Col>
                <Col>Group: </Col>
                <Col>IP Address: </Col>
              </Row>
            </Card.Text>
            <Card.Footer
              className="text-center m-0"
              style={{ fontSize: "1.25em" }}
            >
              <b>List of Interfaces Asscociate In This Host</b>
            </Card.Footer>
          </Card.Body>
        </Card>
        <section className="infDetail">
          <Table striped bordered hover size="sm">
            <thead>
              <tr className="text-center">
                <th>Interface</th>
                <th>VLAN</th>
                <th>Enable</th>
                <th>IP Address</th>
              </tr>
            </thead>
            <tbody>
            </tbody>
          </Table>
        </section>
      </div>
    </>
  );
};

export default DeviceDetail;
