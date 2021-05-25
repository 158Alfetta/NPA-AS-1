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
            enable
        }
    }
    groupData{
        name
        group_desc
    }

}
`
export const QUERY_DEVICE_WITH_FILTER = gql`
query device($groupName: String!){
    findManyDevice(filter:{
        groupData{
            name: $groupName
        }
    },)
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