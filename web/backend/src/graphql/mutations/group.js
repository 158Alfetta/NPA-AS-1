import { groupTC } from '../../models'


export const createGroup = groupTC.getResolver('createOne')
export const updateGroupById = groupTC.getResolver('updateById')