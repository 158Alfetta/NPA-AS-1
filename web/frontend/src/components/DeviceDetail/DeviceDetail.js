import { useParams } from "react-router-dom";
import { Card, Col, Row, Table } from "react-bootstrap";
import { QUERY_DEVICE_BY_ID } from "../../graphql/device";
import "./DeviceDetail.css";
import { useQuery } from "@apollo/client";

const DeviceDetail = () => {
  let { deviceId } = useParams();

  const { data } = useQuery(QUERY_DEVICE_BY_ID, {variables: 
    {_id: deviceId}, });

    const {data: dataDevices} = useQuery(QUERY_DEVICE_WITH_FILTER, {
      variables: {
          group_id: props.value
      }
  })

  let findDeviceById = data?.findDeviceById

  console.log(findDeviceById)
  

  return (
    <>
      <div className="device-detail-plane">
        <Card>
          <Card.Header as="h4">Device Detail</Card.Header>
          <Card.Body>
            <Card.Title>{findDeviceById?.configData?.hostname}</Card.Title>
            <Card.Text>
              <Row>
                <Col>Device Type: {findDeviceById?.type}</Col>
                <Col>Group: {findDeviceById?.groupData?.name}</Col>
                <Col>Management IP Address: {findDeviceById?.ip_address}</Col>
                <Col></Col>
              </Row>
              <Row>
                <Col><Card.Link href="#">Download VLAN Config</Card.Link></Col>
              </Row>
            </Card.Text>
            <Card.Footer
              className="text-center m-0"
              style={{ fontSize: "1.25em" }}
            >
              <b>List of Interfaces</b>
            </Card.Footer>
          </Card.Body>
        </Card>
        <section className="infDetail">
          <Table striped bordered hover size="sm">
            <thead>
              <tr className="text-center">
                <th>Interface</th>
                <th>VLAN</th>
                <th>Enabled</th>
                <th>Mode</th>
                <th>IPv4 Address</th>
                <th>IPv6 Address</th>
              </tr>
            </thead>
            <tbody>
             {findDeviceById?.configData?.interfaces.map((inf) => {
               return(
                 <tr>
                   <td>{inf?.name}</td>
                   <td>{inf?.vlan}</td>
                   <td>{inf?.enabled}</td>
                   <td>{inf?.mode}</td>
                   <td>{inf?.ipv4}</td>
                   <td>{inf?.ipv6}</td>
                 </tr>
               )
             })}
            </tbody>
          </Table>
        </section>
      </div>
    </>
  );
};

export default DeviceDetail;
