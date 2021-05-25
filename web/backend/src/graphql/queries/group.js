import { groupTC } from '../../models'

export const listAllGroup = groupTC.getResolver('findMany')
export const findGroupById = groupTC.getResolver('findById')
export const findOneGroup = groupTC.getResolver('findOne')