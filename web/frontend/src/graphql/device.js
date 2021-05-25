import { gql } from '@apollo/client'

export const QUERY_ALL_DEVICE = gql`
query findManyDevice{
    username
    password
    ipv4
    ipv6
    type
    configData{
        hostname
        interfaces{
            name
            ip_address
            vlan
            enabled
        }
    }
    groupData{
        name
        group_desc
    }

}
`
// export const QUERY_DEVICE_WITH_FILTER = gql`
// query device($groupName: String!){
//     findManyDevice(filter:{
//         groupData{
//             name: $groupName
//         }
//     },)
// }
// `

export const QUERY_DEVICE_WITH_FILTER = gql`
    query device($group_id: String!){
        findManyDevice(filter: {
        group_id: $group_id
        }){
        _id
        ip_address
        type
        retrieved
        groupData{
            name
        }
        configData{
            hostname
        }
        }
    }
`


export const MUTATION_CREATE_DEVICE = gql`
mutation createDevice($record: CreateOnedeviceInput!){
    createDevice(record: $record){
        record{
            _id
            username
            password
            ip_address
            type
            group_id
            config_id
        }
    }
}
`

export const CREATE_CONFIG_DATA = gql`
    mutation createConfig{
        createConfig(record:{
        hostname: "",
        interfaces: [],
        }){
        record{
            _id
        }
        }
    }
`

export const QUERY_DEVICE_BY_ID = gql`
    query findDeviceById($_id: MongoID!){
        findDeviceById(_id: $_id){
        ip_address
        type
        retrieved
        group_id
        config_id
        groupData{
            name
        }
        configData{
            hostname
            interfaces{
            name
            ipv4
            ipv6
            mode
            vlan
            enabled
            }
        }
        }
    }
`

export const QUERY_ONLY_HOSTNAME = gql`
    query findDeviceById($_id: MongoID!){
        findDeviceById(_id: $_id){
        configData{
            hostname
        }}
    }
`