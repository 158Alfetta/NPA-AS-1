import { QUERY_DEVICE_WITH_FILTER} from "../../graphql/device";
import { useHistory } from "react-router-dom";
import { useQuery } from "@apollo/client";
import { Card } from "react-bootstrap";
import "./devices.css";

const DeviceSubCard = (props) => {

    let history = useHistory();

    const {data: dataDevices} = useQuery(QUERY_DEVICE_WITH_FILTER, {
        variables: {
            group_id: props.value
        }
    })

    function handleViewDetailBtn(device_id) {
        history.push("devices/" + device_id);
    }

    
    return(
        <>
        {dataDevices?.findManyDevice.map((device) => {
            return(
                <Card className="deviceCard">
                <Card.Body>
                    <Card.Title>{device?.type}: {device?.ip_address}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">
                    {device?.configData?.hostname ?? '-'}
                    </Card.Subtitle>
                    <Card.Link href="" onClick={() => handleViewDetailBtn(device?._id)}>View Detail</Card.Link>
                </Card.Body>
                </Card>
            )})}
        </>
    )
}

export default DeviceSubCard