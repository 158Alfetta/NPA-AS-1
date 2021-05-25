import { useParams } from "react-router-dom";
import { Card, Col, Row, Table } from "react-bootstrap";
import { QUERY_DEVICE_BY_ID} from "../../graphql/device";
import "./DeviceDetail.css";
import { useQuery } from "@apollo/client";

const DeviceDetail = () => {
  let { deviceId } = useParams();

  const { data } = useQuery(QUERY_DEVICE_BY_ID, {variables: 
    {_id: deviceId}, });

  let findDeviceById = data?.findDeviceById

  console.log(findDeviceById)

  const downloadHandler = () => {
    const { parse } = require('json2csv');

    const fields = ['name', 'ipv4', 'ipv6', 'mode', 'vlan', 'enabled'];
    const opts = { fields };

    try {
      const FileSaver = require('file-saver');
      const csv = parse(findDeviceById?.configData?.interfaces, opts);
      console.log(csv)
      let fileBlob = new Blob([String(csv)], {type: "text/csv;charset=utf-8"});
      FileSaver.saveAs(fileBlob, findDeviceById?.configData?.hostname+"_Config.csv");
      
    } catch (err) {
      console.error(err);
    }
  }

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
                <Col><a><Card.Link className="hover-overlay" onClick={() => downloadHandler()}>Download VLAN Config</Card.Link></a></Col>
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
                <th>Mode</th>
                <th>VLAN</th>
                <th>IPv4 Address</th>
                <th>IPv6 Address</th>
                <th>Enabled</th>
              </tr>
            </thead>
            <tbody>
             {findDeviceById?.configData?.interfaces.map((inf) => {
               return(
                 <tr>
                   <td>{inf?.name}</td>
                   <td>{inf?.mode}</td>
                   <td>{inf?.vlan}</td>
                   <td>{inf?.ipv4}</td>
                   <td>{inf?.ipv6}</td>
                   <td>{inf?.enabled}</td>
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
