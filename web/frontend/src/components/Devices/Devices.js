import { Card, Button } from "react-bootstrap";
import "./devices.css";
import { useHistory } from "react-router-dom";
import { useQuery } from "@apollo/client";
import { QUERY_GROUP } from "../../graphql/group";
import DeviceSubCard from './DeviceSubCard';

const Devices = () => {
  const { data: dataGroup } = useQuery(QUERY_GROUP);


  let history = useHistory();

  return (
    <>
      <div className="device-plane">
        <section className="device1">
          <Card>
            <Card.Body>
              All devices are here. If it not, Press{" "}
              <Button
                onClick={() => history.push("registerdevice/")}
                variant="primary"
              >
                ADD DEVICE
              </Button>
            </Card.Body>
          </Card>
        </section>

        <section className="device2">
          {dataGroup?.listAllGroup.map((group) => {
            return(
            <>
                <div className="groupCard">
                    <Card>
                        <Card.Body className="groupName">
                        {group?.name} <span className="groupDesc">{group?.group_desc}</span>
                        </Card.Body>
                    </Card>
                    <section className="groupDisplayCard grid grid-col-3">
                        <DeviceSubCard value={group?._id} />
                    </section>
                </div>;
            </>
            );
          })}
        </section>
      </div>
    </>
  );
};

export default Devices;
