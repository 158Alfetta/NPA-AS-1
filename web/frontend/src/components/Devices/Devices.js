import {Card, Button } from 'react-bootstrap'
import './devices.css'
import { useHistory } from "react-router-dom";

const Devices = () => { 

    let history = useHistory();

    return(
        <>
            <div className="device-plane">
                <section className="device1">
                    <Card>
                        <Card.Body>All devices are here. If it not, Press <Button onClick={() => history.push("registerdevice/")} variant="primary">ADD DEVICE</Button></Card.Body>
                    </Card>
                </section>

                <section className="device2">

                    <div className="groupCard">
                        <Card>
                            <Card.Body className="groupName">Group Name <span className="groupDesc">descitpntion</span></Card.Body>
                        </Card>
                        <section className="groupDisplayCard grid grid-col-3">
                            <Card className="deviceCard">
                                <Card.Body>
                                    <Card.Title>Router: IP Address</Card.Title>
                                    <Card.Subtitle className="mb-2 text-muted">Hostname</Card.Subtitle>
                                    <Card.Link href="#">View Detail</Card.Link>
                                    <Card.Link href="#">Download VLAN Config</Card.Link>
                                </Card.Body>
                            </Card>
                        </section>
                    </div>
            

                </section>
            </div>
        </>
    );
}

export default Devices