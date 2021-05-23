import { deviceTC } from '../../models'


export const createDevice = deviceTC.getResolver('createOne')
export const removeDevice = deviceTC.getResolver('removeOne')
export const updateDeviceById = deviceTC.getResolver('updateById')