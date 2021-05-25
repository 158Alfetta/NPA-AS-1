import { gql } from '@apollo/client'

export const QUERY_GROUP = gql`
query{
    listAllGroup{
      name
      group_desc
      _id
    }
  }
`

export const MUTATION_CREATE_GROUP = gql`
mutation createGroup(
    $name: String!,
    $group_desc: String,
){
    createGroup(record: {
        name: $name,
        group_desc: $group_desc,
    }){
        record{
            _id
            name
            group_desc
        }
    }
}
`