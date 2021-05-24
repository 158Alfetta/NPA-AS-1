import { deviceTC } from '../../models'


export const createDevice = deviceTC.getResolver('createOne')
export const removeDevice = deviceTC.getResolver('removeById')
export const updateDevice = deviceTC.getResolver('updateById')