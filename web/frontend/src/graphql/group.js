import { gql } from '@apollo/client'

export const QUERY_GROUP = gql`
query listAllGroup{
    name
    group_desc
}
`

export const MUTATION_CREATE_GROUP = gql`
mutation createGroup($record: CreateOneGroupInput!){
    createGroup(record: $record){
        record{
            _id
            name
            group_desc
        }
    }
}
`