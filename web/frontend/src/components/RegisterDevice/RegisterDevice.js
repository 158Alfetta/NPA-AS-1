import "./registerdevice.css";
import { Card, Button, Form } from "react-bootstrap";
import {useState} from 'react'
import { useQuery, useMutation } from "@apollo/client";
import { QUERY_GROUP } from "../../graphql/group";
import { MUTATION_CREATE_DEVICE, CREATE_CONFIG_DATA } from "../../graphql/device";


const RegisterDevice = () => {

  const [createDevice] = useMutation(MUTATION_CREATE_DEVICE);
  const { data } = useQuery(QUERY_GROUP);
  const [createConfig] = useMutation(CREATE_CONFIG_DATA)

  const [deviceData, setDeviceData] = useState(
    {'ip_address': '',
    'type': '',
    'group_id': '',
    'username': '',
    'password': '',
    'retrieved': 'False',
    'config_id': '',
  })

  async function createConfigToDevice() {
    let dataCreateConfig = await createConfig()
    deviceData.config_id = dataCreateConfig?.data?.createConfig?.record?._id;
    createDevice({variables: {
      record: deviceData
    }})
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    console.log(deviceData)
    createConfigToDevice()
  }

  const handleChangeIPA = (e) => setDeviceData({...deviceData, ip_address: e.target.value})
  const handleChangeType = (e) => setDeviceData({...deviceData, type: e.target.value})
  const handleChangeGroup = (e) => setDeviceData({...deviceData, group_id: e.target.value})
  const handleChangeUser = (e) => setDeviceData({...deviceData, username: e.target.value})
  const handleChangePass = (e) => setDeviceData({...deviceData, password: e.target.value})

  return (
    <>
      <div className="regisDevice-plane">
        <Card body className="regisDevice-Name">
          Register Device
        </Card>
        <section className="regisDevice-form">
          <Form onSubmit={handleSubmit}>
            <Form.Group>
              <Form.Label>
                <b>IP Address</b>
              </Form.Label>
              <Form.Control
                type="ip_address"
                placeholder="Management IP Address of device"
                onChange = {handleChangeIPA}
                value={deviceData.ip_address}
              />
              <Form.Label>
                <b>Device Type</b>
              </Form.Label>
              <Form.Control as="select" onChange={handleChangeType} >
                <option value="">- SELECT DEVICE TYPE - </option>
                <option value="Switch">Switch</option>
                <option value="Router">Router</option>
              </Form.Control>
              <Form.Label>
                <b>Group</b>
              </Form.Label>
              <Form.Control as="select" onChange={handleChangeGroup}>
                <option value="">- SELECT GROUP -</option>
                {data?.listAllGroup.map((group) => <option value={group?._id}>{group?.name}</option>)}
              </Form.Control>
              <Form.Label>
                <b>SSH Username</b>
              </Form.Label>
              <Form.Control
                type="username"
                placeholder="Username use to connect via SSH"
                onChange={handleChangeUser}
              />
              <Form.Label>
                <b>SSH Password</b>
              </Form.Label>
              <Form.Control
                type="password"
                placeholder="Password use to connect via SSH"
                onChange={handleChangePass}
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
