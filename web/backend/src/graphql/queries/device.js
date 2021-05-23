import { deviceTC } from '../../models'

export const findDeviceById = deviceTC.getResolver('findById')
export const findOneDevice = deviceTC.getResolver('findOne')
export const findManyDevice = deviceTC.getResolver('findMany')